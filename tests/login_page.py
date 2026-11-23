from selenium.webdriver.common.by import By



class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.ID, "email")
        self.password = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    
    def open(self):
        self.driver.get("http://127.0.0.1:5000/login")
    
    
    def login_with(self, username, password):
        self.open()
        self.__enter_username(username)
        self.__enter_password(password)
        self.__click_login()
    
    
    def __enter_username(self, username):
        self.driver.find_element(*self.username).send_keys(username)
    
    
    def __enter_password(self, password):
        self.driver.find_element(*self.password).send_keys(password)
    
    
    def __click_login(self):
        self.driver.find_element(*self.login_button).click()


    