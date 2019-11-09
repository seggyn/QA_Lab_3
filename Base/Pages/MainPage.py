from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Base.Pages.BasePage import BasePage
from Base.Locators.MainPageLocators import MainPageLocators


class MainPage(BasePage):
    """Home page action methods come here"""

    checklist = [
        'Додавання елемента списку',
        'Редагування елемента списку',
        'Відміти як виконане',
        'Видалення елементу списку',
        'Кількість активних задач',
        'Переглянути активні задачі',
        'Переглянути виконані задачі'
    ]
    toggles = []

    new_task = 'Нова задача'
    edited_task = 'Нова задача 2'

    def add_tasks(self):
        element = self.driver.find_element(*MainPageLocators.NEW_TODO)
        for item in self.checklist:
            element.send_keys(item + Keys.ENTER)

    def add_new_task(self):
        element = self.driver.find_element(*MainPageLocators.NEW_TODO)
        element.send_keys(self.new_task + Keys.ENTER)

    def toggle(self, num, checklist_flag=False):
        element = self.driver.find_element_by_css_selector('ul.todo-list>li:nth-child(' + str(num) + ')>div>input.toggle')
        element.click()
        if checklist_flag:
            self.toggles.append(self.checklist[num - 1])

    def is_new_task_added(self):
        element = self.driver.find_element(*MainPageLocators.LAST_LABEL)
        return element.text == self.new_task

    def edit_last_task(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.LAST_LABEL))
        ActionChains(self.driver).double_click(element).perform()
        ActionChains(self.driver).send_keys(Keys.SPACE + '2' + Keys.ENTER).perform()

    def is_last_task_edit(self):
        element = self.driver.find_element(*MainPageLocators.LAST_LABEL)
        return element.text == self.edited_task

    def is_last_task_completed(self):
        element = self.driver.find_element(*MainPageLocators.LAST_LI)
        return 'completed' in element.get_attribute('class').split(' ')

    def remove_last_task(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.LAST_LI))
        ActionChains(self.driver).move_to_element(element).perform()
        button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(MainPageLocators.LAST_REMOVE_BUTTON))
        button.click()

    def is_last_task_removed(self):
        flag = False
        try:
            self.driver.find_element(*MainPageLocators.TASK_8_LABEL)
        except NoSuchElementException:
            flag = True
        return flag

    def is_counter_true(self):
        active_count = len(self.checklist) - len(self.toggles)
        counter_num = self.driver.find_element(*MainPageLocators.COUNTER)
        return int(counter_num.text) == active_count

    def go_to_all_tasks(self):
        element = self.driver.find_element(*MainPageLocators.ALL_BUTTON)
        element.click()

    def go_to_active_tasks(self):
        element = self.driver.find_element(*MainPageLocators.ACTIVE_BUTTON)
        element.click()

    def go_to_completed_tasks(self):
        element = self.driver.find_element(*MainPageLocators.COMPLETED_BUTTON)
        element.click()

    def get_current_tasks(self):
        return self.driver.execute_script("let array = [];"
                    "for (let elem of document.getElementsByClassName('todo-list')[0].getElementsByTagName('li')) { "
                    " array.push(elem.innerText); }; return array;")

    def compare_active_task(self, array):
        return list(set(self.checklist) - set(self.toggles)) == array

    def compare_completed_task(self, array):
        return array == self.toggles
