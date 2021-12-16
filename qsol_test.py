import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
from dotenv import dotenv_values


class TestLoginPage():
    islogged = False

    def test_login(self, browser):
        test_data = self.read_csv()
        for index, line in enumerate(test_data):
            self.login(browser=browser, company_name=line["FIRMA1"], index=index, street=line["STRASSE"])
            self.islogged = True

    def login(self, browser, company_name, index, street):
        browser.maximize_window()

        wait = WebDriverWait(browser, 40)
        if not self.islogged:
            browser.get("https://acsinformatik2020mai.crm4.dynamics.com/")
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@type = 'email']")))
            element.send_keys("ah@ACSInformatik2020Mai.onmicrosoft.com" + "\n")
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@type = 'password']")))
            element.send_keys("acsD81245" + "\n")
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@id = 'idSIButton9']")))
            element.click()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "AppLandingPage")))
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@id = 'AppModuleTileSec_1_Item_1']")))
            element.click()
            # time.sleep(100)
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'Accounts')]")))
            element.click()
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'New')]")))
        element.click()
        time.sleep(3)
        # enter Account name
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@data-id='name.fieldControl-text-box-text']")))
        element.click()
        time.sleep(1)
        element.send_keys(company_name)
        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        # enter street
        element = wait.until(EC.presence_of_element_located(
            (
                By.XPATH, "//input[@data-id='address1_line1.fieldControl-text-box-text']")))
        element.click()
        # time.sleep()
        element.send_keys(street + str(index))

        # enter city
        element = wait.until(EC.presence_of_element_located(
            (
                By.XPATH, "//input[@data-id='address1_city.fieldControl-text-box-text']")))
        element.click()
        element.send_keys("Muenchen" + str(index))
        # enter postal code
        element = wait.until(EC.presence_of_element_located(
            (
                By.XPATH, "//input[@data-id='address1_postalcode.fieldControl-text-box-text']")))
        element.send_keys("81245" + str(index))
        # Save and close
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Save')]")))
        element.click()
        time.sleep(2)
        if len(browser.window_handles) > 1:
            browser.switch_to_window(browser.window_handles[1])
            browser.close()
            browser.switch_to_window(browser.window_handles[0])
        time.sleep(5)

    def read_csv(self):
        variables = dotenv_values()
        filename = variables['FILENAME']

        with open(filename, newline='', encoding='ANSI') as csvfile:
            d_reader = csv.DictReader(csvfile, delimiter=';')
            return list(d_reader)
