from selenium.webdriver.common.by import By



class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.myaccount_button = (By.ID, "myAccountButton")
    
    
    def get_button_text(self):
        return self.driver.find_element(*self.myaccount_button).text
    

    def __click_my_account(self):
        self.driver.find_element(*self.myaccount_button).click()


    def get_account_firstname(self):
        self.__click_my_account()
        firstname_element = self.driver.find_element(By.ID, "myaccountFirstname")
        return firstname_element.get_attribute("innerText").strip()

    
