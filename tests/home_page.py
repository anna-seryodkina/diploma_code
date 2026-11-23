from selenium.webdriver.common.by import By



class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.myaccount_button = (By.ID, "myAccountButton")
    
    
    def get_button_text(self):
        return self.driver.find_element(*self.myaccount_button).text
    

