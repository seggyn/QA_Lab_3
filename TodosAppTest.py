from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

driver = webdriver.Chrome('/Users/andreypolakowski//PycharmProjects/QA_LAB_3/chromedriver')
driver.get('http://todomvc.com/examples/angularjs/')
driver.implicitly_wait(6)

checklist = [
    'Додавання елемента списку',
    'Редагування елемента списку',
    'Відміти як виконане',
    'Видалення елементу списку',
    'Кількість активних задач',
    'Переглянути активні задачі',
    'Переглянути виконані задачі'
]

toggle_array = []

new_element = 'Нова задача'
edited_element = 'Нова задача 2'

new_todo = driver.find_element_by_class_name('new-todo')
for elem in checklist:
    new_todo.send_keys(elem + Keys.ENTER)


def toggle(num, checklist_flag=False):
    toggle_elem = driver.find_element_by_css_selector('ul.todo-list>li:nth-child(' + str(num) + ')>div>input.toggle')
    toggle_elem.click()
    if checklist_flag:
        toggle_array.append(checklist[num - 1])


class GoogleTestCase(unittest.TestCase):

    def assertTrue(self, expr, num, msg = ...) -> None:
        super().assertTrue(expr, msg)
        if expr:
            toggle(num, True)

    def test_add_new_element(self):
        new_todo = driver.find_element_by_class_name('new-todo')
        new_todo.send_keys(new_element + Keys.ENTER)

        task_8_label = driver.find_element_by_css_selector('ul.todo-list>li:last-of-type>div>label')
        self.assertTrue(task_8_label.text == new_element, 1)

    def test_edit_element(self):
        task_8_label = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.todo-list>li:last-of-type>div>label')))
        ActionChains(driver).double_click(task_8_label).perform()
        ActionChains(driver).send_keys(Keys.SPACE + '2' + Keys.ENTER).perform()
        self.assertTrue(task_8_label.text == edited_element, 2)

    def test_mark_as_done(self):
        toggle(8)
        task_8_li = driver.find_element_by_css_selector('ul.todo-list>li:last-of-type')
        self.assertTrue('completed' in task_8_li.get_attribute('class').split(' '), 3)

    def test_remove_element(self):
        task_8_li = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.todo-list>li:last-of-type')))
        ActionChains(driver).move_to_element(task_8_li).perform()
        task_8_remove = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.todo-list>li:last-of-type>div.view>button')))
        task_8_remove.click()
        flag = False
        try:
            driver.find_element_by_css_selector('ul.todo-list>li:nth-child(8)>div>label')
        except NoSuchElementException:
            flag = True
        self.assertTrue(flag, 4)

    def test_active_tasks_count(self):
        active_count = len(checklist) - len(toggle_array)
        todo_count_num = driver.find_element_by_css_selector('span.todo-count>strong')
        self.assertTrue(int(todo_count_num.text) == active_count, 5)

    def test_view_active_tasks(self):
        active_button = driver.find_element_by_css_selector(".filters a[href='#/active']")
        active_button.click()

        active_task = driver.execute_script("let array = [];"
                              "for (let elem of document.getElementsByClassName('todo-list')[0].getElementsByTagName('li')) { "
                              " array.push(elem.innerText); }; return array;")

        check_active_task = list(set(checklist) - set(toggle_array))

        all_button = driver.find_element_by_css_selector(".filters a[href='#/']")
        all_button.click()

        self.assertTrue(check_active_task == active_task, 6)

    def test_view_completed_tasks(self):
        completed_button = driver.find_element_by_css_selector(".filters a[href='#/completed']")
        completed_button.click()

        completed_task = driver.execute_script("let array = [];"
                              "for (let elem of document.getElementsByClassName('todo-list')[0].getElementsByTagName('li')) { "
                              " array.push(elem.innerText); }; return array;")

        all_button = driver.find_element_by_css_selector(".filters a[href='#/']")
        all_button.click()

        self.assertTrue(completed_task == toggle_array, 7)


suite = unittest.TestSuite()

suite.addTest(GoogleTestCase('test_add_new_element'))
suite.addTest(GoogleTestCase('test_edit_element'))
suite.addTest(GoogleTestCase('test_mark_as_done'))
suite.addTest(GoogleTestCase('test_remove_element'))

suite.addTest(GoogleTestCase('test_active_tasks_count'))

suite.addTest(GoogleTestCase('test_view_active_tasks'))
suite.addTest(GoogleTestCase('test_view_completed_tasks'))

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite)
