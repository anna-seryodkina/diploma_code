import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from tests.login_page import LoginPage
from tests.home_page import HomePage



@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_login_with_valid_data(driver):
    login_page = LoginPage(driver)
    login_page.login_with("testing@gmail.com", "0987654321")
    home_page = HomePage(driver)
    
    assert home_page.get_button_text() == "Мій аккаунт"


