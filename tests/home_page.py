from selenium.webdriver.common.by import By



class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.title = (By.CSS_SELECTOR, "#content h2") # Fix this
    
    
    def get_title(self):
        return self.driver.find_element(*self.title).text

