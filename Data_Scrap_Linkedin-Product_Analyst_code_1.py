#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the necessary modules for web scraping and data manipulation
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
from datetime import date


# In[4]:


# Create an empty DataFrame to store overall data from jobs pages
Overall_Data_Jobs_Page = pd.DataFrame()

# Get today's date in the format 'YYYYMMDD'
today_date = date.today().strftime("%Y%m%d")

# Function to start the web driver and perform LinkedIn login
def driver_start():
    DRIVER_PATH = r"Path_to_Driver"  # Replace with the actual path to the driver
    driver = webdriver.Chrome()  # Create a Chrome web driver instance

    # Open LinkedIn's login page
    driver.get("https://linkedin.com/uas/login")

    # Wait for the page to load
    time.sleep(5)

    # Find and fill the username field
    username = driver.find_element(By.ID, "username")
    username.send_keys("*****")  # Enter your email address here

    # Find and fill the password field
    pword = driver.find_element(By.ID, "password")
    pword.send_keys("******")  # Enter your password here

    # Click the login button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    return driver  # Return the initialized driver instance


# In[7]:


# Function to scroll through the webpage and load more content
def scroll_func():
    start = time.time()  # Record the starting time of scrolling

    # Define initial and final scroll positions
    initialScroll = 0
    finalScroll = 1000

    while True:
        # Execute JavaScript to scroll the window
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        
        # Update scroll positions for the next iteration
        initialScroll = finalScroll
        finalScroll += 1000

        # Pause execution for a few seconds to allow data to load
        time.sleep(3)  # Adjust this based on your needs and internet speed

        end = time.time()  # Get the current time

        # Limit scrolling duration to 5 seconds
        if round(end - start) > 5:
            break  # Exit the loop if scrolling duration exceeds 5 seconds


# In[11]:


# Define the URL of the LinkedIn jobs search page
url = "https://www.linkedin.com/jobs/search/?currentJobId=3651763841&distance=25&geoId=103644278&keywords=product%20analyst"

# Start the web driver and perform LinkedIn login
driver = driver_start()

# Pause for 3 seconds before continuing
time.sleep(3)

# Open the specified URL using the web driver
driver.get(url)

# Pause for 4 seconds to allow the page to load
time.sleep(4)


# In[24]:


# Find the generic Ember element using XPath
generic_ember_element = driver.find_element(By.XPATH, '//*[starts-with(@id, "ember")]')

# Scroll to the generic Ember element using JavaScript
driver.execute_script('arguments[0].scrollIntoView(true);', generic_ember_element)

# Call the scroll function to load more content
scroll_func()

# Get the page source after scrolling to load more content
src = driver.page_source


# In[155]:


# Create a BeautifulSoup object from the updated page source
soup = BeautifulSoup(src, "html.parser")

# Find all 'a' elements with a specific class using BeautifulSoup
# These elements likely represent job links on the page
Links_elements = soup.findAll('a', {'class': 'disabled ember-view job-card-container__link job-card-list__title'})


# In[156]:


# Initialize empty lists to store hyperlinks and positions
hyperlink = []
position = []

# Iterate through the found 'a' elements representing job links
for each in Links_elements:
    # Check if the hyperlink contains 'jobs' and 'refId', and if the element's text is not empty
    if 'jobs' in each['href'] and 'refId' in each['href'] and each.text.strip() != "":
        hyperlink.append(each['href'])  # Append the hyperlink to the list
        position.append(each.text.strip())  # Append the position text to the list


# In[157]:


# Create a DataFrame using the collected hyperlinks and positions
Data_Page_1 = pd.DataFrame({'hyperlink': hyperlink, 'position': position})

# Add a new column 'Date' to the DataFrame with today's date
Data_Page_1['Date'] = today_date

# Prepend the base LinkedIn URL to each hyperlink in the DataFrame
Data_Page_1['hyperlink'] = Data_Page_1.hyperlink.apply(lambda x: "https://www.linkedin.com" + x)


# In[158]:


# Display the content of the Data_Page_1 DataFrame
display(Data_Page_1)


# In[159]:


# Concatenate the current page's data with the existing overall data
Overall_Data_Jobs_Page = pd.concat([Overall_Data_Jobs_Page, Data_Page_1])

# Drop duplicate rows based on the 'hyperlink' column
Overall_Data_Jobs_Page = Overall_Data_Jobs_Page.drop_duplicates(subset='hyperlink')


# In[160]:


# Drop duplicate rows based on the 'hyperlink' column and save the DataFrame to a CSV file
Overall_Data_Jobs_Page.drop_duplicates(subset='hyperlink').to_csv(
    "Overall_Data_Product_Analyst_" + today_date + ".csv",  # Construct the CSV filename with today's date
    index=False  # Exclude index column from the CSV
)


# In[161]:


# Display the content of the Overall_Data_Jobs_Page DataFrame
display(Overall_Data_Jobs_Page)


# In[162]:


# Close the WebDriver instance
# driver.quit()

driver.close()


# In[ ]:




