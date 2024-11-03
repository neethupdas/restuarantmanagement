

# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# class TestLoginPage(unittest.TestCase):
#     def setUp(self):
#         try:
#             self.driver = webdriver.Chrome() 
#         except Exception as e:
#             print(f"Error initializing WebDriver: {e}")
#     def tearDown(self):
#         if hasattr(self, 'driver') and self.driver:
#             self.driver.quit()
#     def test_login_page(self):
#         if not hasattr(self, 'driver') or not self.driver:
#             self.fail("WebDriver not initialized, check previous errors.")
#         try:
#             self.driver.get("http://127.0.0.1:8000/accounts/login/")
#         except Exception as e:
#             self.fail(f"Error opening URL: {e}")
#         username_input = self.driver.find_element("name", "username")
#         password_input = self.driver.find_element("name", "password")
#         username_input.send_keys("binyamp2024a@mca.ajce.in")
#         password_input.send_keys("Binya@123")
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         time.sleep(2)
#         assert "welcome-message" in self.driver.page_source  
# if __name__ == "__main__":
#     unittest.main()





# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# class TestLoginPage(unittest.TestCase):
#     def setUp(self):
#         try:
#             self.driver = webdriver.Chrome()  # Use the appropriate webdriver for your browser (e.g., Chrome, Firefox)
#         except Exception as e:
#             print(f"Error initializing WebDriver: {e}")

#     def tearDown(self):
#         if hasattr(self, 'driver') and self.driver:
#             self.driver.quit()

#     def test_login_page(self):
#         if not hasattr(self, 'driver') or not self.driver:
#             self.fail("WebDriver not initialized, check previous errors.")

#         try:
#             self.driver.get("http://127.0.0.1:8000/accounts/login/")  # Replace with the actual URL of your login page
#         except Exception as e:
#             self.fail(f"Error opening URL: {e}")

#         # Assuming you have form elements with name attributes 'username' and 'password'
#         username_input = self.driver.find_element("name", "username")
#         password_input = self.driver.find_element("name", "password")

#         # Enter test username and password
#         username_input.send_keys("binyamp2024a@mca.ajce.in")
#         password_input.send_keys("Binya@123")

#         # Click the login button
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()

#         # Add a delay to allow any potential messages to be displayed
#         time.sleep(2)

#         # Check if the login was successful by looking for a success message or checking the URL
#         # You need to adjust this based on your actual implementation
#         assert "welcome-message" in self.driver.page_source  # Replace "success" with a string indicative of successful login

#         # Optionally, you can also check the URL or any other elements to ensure successful login
#         # assert self.driver.current_url == "expected_url_after_login"

#         # Add more assertions or checks based on your specific implementation
        

# if __name__ == "__main__":
#     unittest.main()









# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# class TestLoginPage(unittest.TestCase):
#     def setUp(self):
#         try:
#             self.driver = webdriver.Chrome()
#         except Exception as e:
#             print(f"Error initializing WebDriver: {e}")
#     def tearDown(self):
#         if hasattr(self, 'driver') and self.driver:
#             self.driver.quit()
#     def test_login_page(self):
#         if not hasattr(self, 'driver') or not self.driver:
#             self.fail("WebDriver not initialized, check previous errors.")
#         try:
#             self.driver.get("http://127.0.0.1:8000/accounts/login/")
#         except Exception as e:
#             self.fail(f"Error opening URL: {e}")
#         print("Navigate to the website")
#         username_input = self.driver.find_element("name", "username")
#         password_input = self.driver.find_element("name", "password")
#         username_input.send_keys("binyamp2024a@mca.ajce.in")
#         password_input.send_keys("Binya@123")
#         print("Enter email and password")
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         print("click on login button")
#         time.sleep(2)
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         print("Clicked on the add to cart button")
#         time.sleep(2)
#         assert "testclass" in self.driver.page_source
#         print("Navigate to Cart page")
# if __name__ == "__main__":
#     unittest.main()






# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# class TestLoginPage(unittest.TestCase):
#     def setUp(self):
#         try:
#             self.driver = webdriver.Chrome()
#         except Exception as e:
#             print(f"Error initializing WebDriver: {e}")
#     def tearDown(self):
#         if hasattr(self, 'driver') and self.driver:
#             self.driver.quit()
#     def test_login_page(self):
#         if not hasattr(self, 'driver') or not self.driver:
#             self.fail("WebDriver not initialized, check previous errors.")
#         try:
#             self.driver.get("http://127.0.0.1:8000/accounts/login/") 
#         except Exception as e:
#             self.fail(f"Error opening URL: {e}")
#         print("Navigate to the website")
#         username_input = self.driver.find_element("name", "username")
#         password_input = self.driver.find_element("name", "password")
#         username_input.send_keys("binyaj245@gmail.com")
#         password_input.send_keys("binya@123")
#         print("Enter email and password")
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         print("click on login button")
#         time.sleep(2)
#         addc = self.driver.find_element("name", "addcategory")
#         addc.click()
#         print("click on the add category link")
#         time.sleep(2)
#         category_input = self.driver.find_element("name", "name")
#         category_input.send_keys("Newcategory12")
#         print("Entered the category name")
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         print("Click on add button")
#         assert "test_for_a_vew_category" in self.driver.page_source
#         time.sleep(2)
# if __name__ == "__main__":
#     unittest.main()






# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# class TestLoginPage(unittest.TestCase):
#     def setUp(self):
#         try:
#             self.driver = webdriver.Chrome()
#         except Exception as e:
#             print(f"Error initializing WebDriver: {e}")
#     def tearDown(self):
#         if hasattr(self, 'driver') and self.driver:
#             self.driver.quit()
#     def test_login_page(self):
#         if not hasattr(self, 'driver') or not self.driver:
#             self.fail("WebDriver not initialized, check previous errors.")
#         try:
#             self.driver.get("http://127.0.0.1:8000/accounts/login/") 
#         except Exception as e:
#             self.fail(f"Error opening URL: {e}")
#         print("Navigate to the website")
#         username_input = self.driver.find_element("name", "username")
#         password_input = self.driver.find_element("name", "password")
#         username_input.send_keys("binyamp2024a@mca.ajce.in")
#         password_input.send_keys("Binya@123")
#         print("email and password are entered")
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         print("Click on the button")
#         time.sleep(2)
#         addc = self.driver.find_element("name", "profile")
#         addc.click()
#         print("click on the profile link")
#         time.sleep(2)
#         address = self.driver.find_element("name", "address")
#         address.send_keys("Muthiyalaparambil")
#         print("Update the profile")
#         login_button = self.driver.find_element("css selector", "button[type='submit']")
#         login_button.click()
#         print("click on edit button")
#         assert "test_for_customerprofile" in self.driver.page_source
#         time.sleep(2)
# if __name__ == "__main__":
#     unittest.main()



import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
class TestLoginPage(unittest.TestCase):
    def setUp(self):
        try:
            self.driver = webdriver.Chrome()
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
    def test_login_page(self):
        if not hasattr(self, 'driver') or not self.driver:
            self.fail("WebDriver not initialized, check previous errors.")
        try:
            self.driver.get("http://127.0.0.1:8000/accounts/login/") 
        except Exception as e:
            self.fail(f"Error opening URL: {e}")
        print("Navigate to the website")
        username_input = self.driver.find_element("name", "username")
        password_input = self.driver.find_element("name", "password")
        username_input.send_keys("binyamp2024a@mca.ajce.in")
        password_input.send_keys("Binya@123")
        print("email and password are entered")
        login_button = self.driver.find_element("css selector", "button[type='submit']")
        login_button.click()
        print("Click on the button")
        time.sleep(2)
        addc = self.driver.find_element("name", "reservation")
        addc.click()
        print("click on the reservation link")
        time.sleep(2)

        name_input = self.driver.find_element("name", "username")
        email_input = self.driver.find_element("name", "email")
        phone_input = self.driver.find_element("name", "phone")
        date_input = self.driver.find_element("name", "date")
        timein_input = self.driver.find_element("name", "time")
        timeout_input = self.driver.find_element("name", "timeout")
        guests_input = self.driver.find_element("name", "numberofpersons")

        date_input.send_keys("2024-05-20")  # Fill with desired date
        timein_input.send_keys("12:00")
        timeout_input.send_keys("13:00")
        guests_input.send_keys("4")
        time.sleep(2)
        print("Values are entered")

        login_button = self.driver.find_element("css selector", "button[type='submit']")
        login_button.click()

        
if __name__ == "__main__":
    unittest.main()





