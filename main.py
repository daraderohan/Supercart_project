from flask import Flask,render_template,flash,request
from selenium import webdriver
from froms import LoginForm
import csv
from prettytable import PrettyTable

app=Flask(__name__)
app.config['SECRET_KEY']='992a1aced4a729c428a4c94ee7f0fbd1'
@app.route("/",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash(f'Login Successful')
    return render_template("login.html",form=form)

##@app.route("authentication",methods=['GET','POST'])
def authenti():
    if request.method=='POST':
        result=request.form
        for key,value in result.items():
            if key=="username":
                username=value
            if key=="password":
                password=value
    d1 = webdriver.Chrome(executable_path="D:\driver\chromedriver")
    d1.implicitly_wait(10)
    d1.get("https://www.amazon.in/gp/cart/view.html?ref_=nav_cart")
    d1.find_element_by_id("a-autoid-0-announce").click()
    d1.find_element_by_id("ap_email").send_keys(username)
    d1.find_element_by_id("continue").click()



@app.route("/result",methos=['POST'])

def selscript():
    if request.method=='POST':
        result=request.form
        for key,value in result.items():
            if key=="username":
                username=value
            if key=="password":
                password=value
    driver = webdriver.Chrome(executable_path="D:\driver\chromedriver")

    driver.implicitly_wait(10)
    driver.get("https://www.amazon.in/gp/cart/view.html?ref_=nav_cart")
    driver.find_element_by_id("a-autoid-0-announce").click()
    driver.find_element_by_id("ap_email").send_keys(username)
    driver.find_element_by_id("continue").click()
    driver.find_element_by_id("ap_password").send_keys(password)
    driver.find_element_by_id("signInSubmit").click()
    a=driver.find_element_by_id("auth-error-message-box")
    if a!=None:
        print(a.text)
    name = driver.find_elements_by_css_selector(
        "div.sc-list-item-content > div > div.a-column.a-span10 > div > div > div.a-fixed-left-grid-col.a-col-right > ul > li:nth-child(1) > span > a > span.a-size-medium.sc-product-title.a-text-bold")

    price = driver.find_elements_by_css_selector(
        " div.sc-list-item-content > div > div.a-column.a-span2.a-text-right.sc-item-right-col.a-span-last > p > span")
    with open('file.csv', 'w', newline='') as f:
        fieldnames = ['name', 'price']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
        for i in range(len(name)):
            thewriter.writerow({'name': name[i].text+str(";"), 'price': price[i].text})


    file = open("file.csv", 'r')
    file = file.readlines()
    head = file[0]
    head = head.split(',')
    # for headings
    table = PrettyTable([head[0], head[1]])
    for i in range(1, len(file)):
        table.add_row(file[i].split(';'))
    htmlCode = table.get_html_string()
    final_htmlFile = open('templates/Table.html', 'w')
    final_htmlFile = final_htmlFile.write(htmlCode)
    return render_template('Table.html')


if __name__ =='__main__':
    app.run(debug=True)