from flask import render_template,flash,request,redirect,url_for
from test import bcrypt,app,db,scheduler
from selenium import webdriver
import csv
from prettytable import PrettyTable
from test.froms import RegistrationForm,LoginForm
from test.models import User,Cart_items
from flask_login import login_user,login_manager,current_user,logout_user,login_required
from test import options





@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        user=User.query.filter_by(id=current_user.id).first()
        if scheduler.running==True:
            print("f")
            scheduler.shutdown()
            #scheduler.add_job(func=job, trigger='interval', args=[current_user.username, current_user.password], id='job',
             #             seconds=15)
        else:
            print("t")
            scheduler.add_job(func=job, trigger='interval', args=[current_user.username, current_user.password],
                              id='job',
                              seconds=15)
            scheduler.start()
        for item in user.cart_items:
            if item.threshold_price!=0 and float(item.price.replace('\n','').replace(' ',''))< int(item.threshold_price):
                flash(str(item.name) +"can be purchased",'success')
    return render_template("home.html" ,title='home')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    return render_template("register.html",form=form,title='register')

@app.route("/validate",methods=['GET','POST'])
def validate():
    if request.method=='POST':
        result=request.form
    for key,value in result.items():
        if key == "username":
            username = value
        if key == "password":
            password = value

    driver = webdriver.Chrome(executable_path="D:\driver\chromedriver",options=options)
    driver.get("https://www.amazon.in/gp/cart/view.html?ref_=nav_cart")
    driver.find_element_by_id("a-autoid-0-announce").click()
    driver.find_element_by_id("ap_email").send_keys(username)
    driver.find_element_by_id("continue").click()
    if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
        print(driver.find_element_by_id("auth-error-message-box").text)
        return render_template('username.html')
    else:
        driver.find_element_by_id("ap_password").send_keys(password)
        driver.find_element_by_id("signInSubmit").click()
        if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
            return render_template('password.html')
        else:
            form = RegistrationForm()
            user=User.query.filter_by(username=form.username.data).first()
            if user:
                return render_template('registereduser.html')
            form.validate_on_submit(form.username.data, form.password.data)
            return render_template("successfull_register.html",title='Successfully registered')






@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password==form.password.data:
            login_user(user, remember=form.remember.data)
            print('works')
            driver = webdriver.Chrome(executable_path="D:\driver\chromedriver",options=options)

            # driver.implicitly_wait(10)
            driver.get("https://www.amazon.in/gp/cart/view.html?ref_=nav_cart")
            driver.find_element_by_id("a-autoid-0-announce").click()
            driver.find_element_by_id("ap_email").send_keys(form.username.data)
            driver.find_element_by_id("continue").click()
            if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
                print(driver.find_element_by_id("auth-error-message-box").text)
                return render_template('username.html')
            else:
                driver.find_element_by_id("ap_password").send_keys(form.password.data)
                driver.find_element_by_id("signInSubmit").click()
                if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
                    return render_template('password.html')
                else:
                    name = driver.find_elements_by_css_selector(
                        "div.sc-list-item-content > div > div.a-column.a-span10 > div > div > div.a-fixed-left-grid-col.a-col-right > ul > li:nth-child(1) > span > a > span.a-size-medium.sc-product-title.a-text-bold")
                    price = driver.find_elements_by_css_selector(
                        " div.sc-list-item-content > div > div.a-column.a-span2.a-text-right.sc-item-right-col.a-span-last > p > span")
                    with open('file.csv', 'w', newline='') as f:
                        fieldnames = ['name', 'price']
                        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                        thewriter.writeheader()
                        for i in range(len(name)):
                            thewriter.writerow(
                                {'name': name[i].text.replace(',', ''), 'price': price[i].text.replace(',', '')})
                    file = open("file.csv", 'r')
                    file = file.readlines()
                    head = file[0]
                    head = head.split(',')
                    # for headings
                    table = PrettyTable([head[0], head[1]])
                    for i in range(1, len(file)):
                        table.add_row(file[i].split(','))
                        f = file[i].split(',')
                        item = Cart_items.query.filter_by(name=f[0]).first()
                        print(f[0])
                        print(item)
                        if item and f[0] != item.name:
                            print(False)
                            cart_item = Cart_items(name=f[0], price=f[1], user=current_user)
                            db.session.add(cart_item)
                            db.session.commit()
                        else:
                            if not item:
                                print(True)
                                cart_item = Cart_items(name=f[0], price=f[1], user=current_user)
                                db.session.add(cart_item)
                                db.session.commit()
            return redirect(url_for('selscript'),code=307)
        else:
            flash("check Username or password",'danger')
    return render_template("login1.html",form=form,title='login')


@app.route("/cart_display",methods=['POST','GET'])
def selscript():
    file = open("file.csv", 'r')
    file = file.readlines()
    return render_template('cartdisplay.html',file=file,len=len(file),cart_item=Cart_items,title='Cart items')
@app.route("/set_threshhold",methods=['GET','POST'])
def set_Threshold():
    file=open('file.csv','r')
    file=file.readlines()
    if request.method=='POST':
        result=request.form
        for i in range(1,len(file)):
            c = "cart_item" + str(int(i))
            print(c)
            print(request.form.get(c))
            print(current_user.id)
            item=Cart_items.query.filter_by(name=file[i].split(',')[0]).first()
            item.threshold_price=request.form.get(c)
            db.session.commit()
    return render_template("get_value.html",len=len(file),file=file,title='Set your Budget')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')


def job(username,password):
    from selenium import webdriver
    import csv
    driver = webdriver.Chrome(executable_path="D:\driver\chromedriver",options=options)


    driver.get("https://www.amazon.in/gp/cart/view.html?ref_=nav_cart")
    driver.find_element_by_id("a-autoid-0-announce").click()
    driver.find_element_by_id("ap_email").send_keys(username)
    driver.find_element_by_id("continue").click()
    if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
        print(driver.find_element_by_id("auth-error-message-box").text)
    else:
        driver.find_element_by_id("ap_password").send_keys(password)
        driver.find_element_by_id("signInSubmit").click()
    if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
        print('ERROR PASS')
    name = driver.find_elements_by_css_selector("div.sc-list-item-content > div > div.a-column.a-span10 > div > div > div.a-fixed-left-grid-col.a-col-right > ul > li:nth-child(1) > span > a > span.a-size-medium.sc-product-title.a-text-bold")

    price = driver.find_elements_by_css_selector(" div.sc-list-item-content > div > div.a-column.a-span2.a-text-right.sc-item-right-col.a-span-last > p > span")
    with open('demo.csv', 'w', newline='') as f:
        fieldnames = ['name', 'price']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
        for i in range(len(name)):
            thewriter.writerow({'name': name[i].text, 'price': price[i].text})
            print(name[i].text+price[i].text)
