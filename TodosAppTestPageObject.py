from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

from Base.Pages.MainPage import MainPage

URL = 'http://todomvc.com/examples/angularjs/'
CHROME_DRIVER_PATH = '/Users/andreypolakowski//PycharmProjects/QA_LAB_3/chromedriver'


driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(URL)
driver.implicitly_wait(6)

page = MainPage(driver)

page.add_tasks()


class GoogleTestCase(unittest.TestCase):

    def assertTrue(self, expr, num, msg = ...) -> None:
        super().assertTrue(expr, msg)
        if expr: page.toggle(num, True)

    def test_add_new_element(self):
        page.add_new_task()
        self.assertTrue(page.is_new_task_added(), 1)

    def test_edit_element(self):
        page.edit_last_task()
        self.assertTrue(page.is_last_task_edit(), 2)

    def test_mark_as_done(self):
        page.toggle(8)
        self.assertTrue(page.is_last_task_completed(), 3)

    def test_remove_element(self):
        page.remove_last_task()
        self.assertTrue(page.is_last_task_removed(), 4)

    def test_active_tasks_count(self):
        self.assertTrue(page.is_counter_true(), 5)

    def test_view_active_tasks(self):
        page.go_to_active_tasks()
        active_task = page.get_current_tasks()
        page.go_to_all_tasks()
        self.assertTrue(page.compare_active_task(active_task), 6)

    def test_view_completed_tasks(self):
        page.go_to_completed_tasks()
        completed_task = page.get_current_tasks()
        page.go_to_all_tasks()
        self.assertTrue(page.compare_completed_task(completed_task), 7)


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
