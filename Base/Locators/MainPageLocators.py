from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    COUNTER = (By.CSS_SELECTOR, 'span.todo-count>strong')
    NEW_TODO = (By.CLASS_NAME, 'new-todo')

    ALL_BUTTON = (By.CSS_SELECTOR, ".filters a[href='#/']")
    ACTIVE_BUTTON = (By.CSS_SELECTOR, ".filters a[href='#/active']")
    COMPLETED_BUTTON = (By.CSS_SELECTOR, ".filters a[href='#/completed']")

    TASK_8_LABEL = (By.CSS_SELECTOR, 'ul.todo-list>li:nth-child(8)>div>label')
    LAST_LI = (By.CSS_SELECTOR, 'ul.todo-list>li:last-of-type')
    LAST_LABEL = (By.CSS_SELECTOR, 'ul.todo-list>li:last-of-type>div>label')
    LAST_REMOVE_BUTTON = (By.CSS_SELECTOR, 'ul.todo-list>li:last-of-type>div.view>button')
