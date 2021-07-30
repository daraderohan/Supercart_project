from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import schedule

import csv
def job(username,password):
    from selenium import webdriver
    import csv
    driver = webdriver.Chrome(executable_path="D:\driver\chromedriver")


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

