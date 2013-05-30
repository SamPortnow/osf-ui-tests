"""
Miscellaneous utility functions for smokescreen tests
"""

# Project imports
import config

# Set up MongoDB
from pymongo import MongoClient
client = MongoClient(config.mongo_uri)


def login(driver, username, password):

    """Log in to OSF

    Args:
        driver : selenium.webdriver instance
        username : OSF username
        password : OSF password
    """
    # Browse to OSF page
    driver.get(config.osf_home)
    driver.implicitly_wait(30)
    # Click login button
    login_link = driver.find_element_by_xpath('//a[@href="/account"]')
    login_link.click()

    # Get login elements
    signin_email = driver.find_element_by_xpath(
        '//form[@name="signin"]//input[@id="username"]')
    signin_password = driver.find_element_by_xpath(
        '//form[@name="signin"]//input[@id="password"]')
    signin_submit = driver.find_element_by_xpath(
        '//form[@name="signin"]//button[@type="submit"]')

    # Login
    signin_email.send_keys(username)
    signin_password.send_keys(password)
    signin_submit.click()


def goto_profile(driver):
    """
    goes to a logged in user's public profile

    Args:
        driver : selenium.webdriver instance
        username : OSF username
        password : OSF password
    """
    # go to OSF home page
    driver.get(config.osf_home)

    # grab the profile button and load the page
    profile_button = driver.find_element_by_link_text('My Public Profile')
    profile_button.click()


def goto_project(driver, project_name):
    """
    goes to a logged in user's specific project

    Args:
        driver : selenium.webdriver instance
        project_name : name of project to be loaded (case sensitive)
    """
    # go to user's profile
    goto_profile(driver)

    # grab the project button and load the page
    project_button = driver.find_element_by_link_text(project_name)
    project_button.click()


def logout(driver):
    """
    logs current user out of OSF

    Args:
        driver : selenium.webdriver instance
    """
    # browse to OSF page
    driver.get(config.osf_home)

    # locate and click logout button
    logout_link = driver.find_element_by_xpath('//ul[@class="nav pull-right"]//a[@href="/logout"]')
    logout_link.click()


def create_project(driver, project_title, project_description):

    driver.get('http://localhost:5000/dashboard')
    #find the new project link and click it
    link = driver.find_element_by_link_text("New Project")
    link.click()
    # enter the title and description of your project
    # in the relevant fields and submit
    title_field = driver.find_element_by_xpath(
        '//form[@name="newProject"]//input[@id="title"]')
    description_field = driver.find_element_by_xpath(
        '//form[@name="newProject"]//textarea[@id="description"]')
    title_field.send_keys(project_title)
    description_field.send_keys(project_description)
    submit_button = driver.find_element_by_xpath(
        '//button[@class="btn primary"][@type="submit"]')
    submit_button.click()


def clear_users():

    """Clear all users from database
    """
    client[config.db_name]['user'].remove()


def clear_project(title):
    """Clear project from database

    Args:
        title : Project title

    """
    client[config.db_name]['node'].remove({'title': title})
