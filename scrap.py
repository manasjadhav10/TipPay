from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Chrome WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# URL of the webpage you want to fetch
url = "https://www.tripadvisor.in/Restaurant_Review-g304554-d803846-Reviews-New_Modern_Cafe-Mumbai_Maharashtra.html"

# Open the webpage
driver.get(url)

# Wait for the user to solve CAPTCHA manually
input("Please solve the CAPTCHA and then press Enter...")

# Get the page source after CAPTCHA is solved
html_content = driver.page_source

# Save the content to a file
with open("page.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Webpage content saved to 'page.html'")

# Close the driver
driver.quit()
