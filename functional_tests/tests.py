from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kelly has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        # She types "Buy shoes from DSW" into a text box
        inputbox.send_keys('Buy shoes from DSW')
    
        # When she hits enter, she is taken to a new URL, and now the page lists
        # "1: Buy shoes from DSW" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        kellys_list_url = self.browser.current_url
        self.assertRegex(kellys_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy shoes from DSW')

        # There is still a text box inviting her to add another item. 
        # She enters "Pack new shoes for Vegas trip"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Pack new shoes for Vegas trip')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy shoes from DSW')
        self.check_for_row_in_list_table('2: Pack new shoes for Vegas trip')

        # Now a new user, Kendal, comes along to the site.

        ## Use a new browser session to make sure that no information
        ## of Kelly's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Chrome('./chromedriver')

        # Kendal visits the home page.  There is no sign of Kelly's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy shoes from DSW', page_text)
        self.assertNotIn('Vegas trip', page_text)

        # Kendal start a new list by entering a new item.  
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Watch Dora')
        inputbox.send_keys(Keys.ENTER)

        # Kendal gets her own unique URL
        kendals_list_url = self.browser.current_url
        self.assertRegex(kendals_list_url, '/lists/.+')
        self.assertNotEqual(kendals_list_url, kellys_list_url)

        # Again, there is no trace of Kelly's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy shoes from DSW', page_text)
        self.assertIn('Watch Dora', page_text)

        # Satisfied, they both go back to sleep        

    def test_layout_and_styling(self):
        # Kelly goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
