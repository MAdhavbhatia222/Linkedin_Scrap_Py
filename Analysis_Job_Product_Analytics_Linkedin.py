#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary libraries
import pandas as pd
import random
from datetime import date
from matplotlib import pyplot as plt
import numpy as np
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords

# Read job details data from a CSV file from code_2
Job_Details_df = pd.read_csv(r"csv_path.csv")

# Filter job details containing 'product' in the job name
Job_Details_df = Job_Details_df[Job_Details_df.Name.apply(lambda x: 'product' in x.lower())]

# Create a new column 'Full_Time' based on 'Contract' column
Job_Details_df['Full_Time'] = Job_Details_df.Contract.apply(lambda x: True if 'full-time' in x.lower() else False)

# Filter job details for full-time positions
Job_Details_df = Job_Details_df[Job_Details_df.Full_Time]

# Function to clean and extract salary ranges
def Salary_Clean(x):
    if '$' in x:
        if len(x.split("$")) > 2:
            low = x.replace("/yr", "").split("·")[0].split("(")[0].split("$")[1].replace("-", "").replace(" ", "")
            high = x.replace("/yr", "").split("·")[0].split("(")[0].split("$")[2].replace("-", "").replace(" ", "")
        if len(x.split("$")) <= 2:
            low = x.replace("/yr", "").split("·")[0].split("(")[0].split("$")[1].replace("-", "").replace(" ", "")
            high = x.replace("/yr", "").split("·")[0].split("(")[0].split("$")[1].replace("-", "").replace(" ", "")
    else:
        low = 0
        high = 0
    return [low, high]

# Apply Salary_Clean function to create new columns for lower and higher salary ranges
Job_Details_df["Lower_Range"] = Job_Details_df.Contract.apply(lambda x: Salary_Clean(x)[0])
Job_Details_df["Higher_Range"] = Job_Details_df.Contract.apply(lambda x: Salary_Clean(x)[1])

# Display the job details DataFrame
display(Job_Details_df)

# Split and process the skills data
Job_Details_df['Skills_list'] = Job_Details_df.Skills.apply(lambda x: x.replace(" ", "").split(","))
Job_Details_df['Skills_Meet_List'] = Job_Details_df['Skills_Meet'].apply(lambda x: x.replace(" ", "").split(","))
Job_Details_df["Missing_Skills"] = Job_Details_df.apply(lambda x: list(set(x.Skills_list).difference(x.Skills_Meet_List)), axis=1)

# Explode the skills list column and create a DataFrame
List_Skills = Job_Details_df['Skills_list'].explode()
List_Skills_Df = pd.DataFrame(List_Skills).reset_index(drop=True)

# Display the top 20 most common skills
print(List_Skills_Df[List_Skills_Df.Skills_list != ""].value_counts()[:20])


# In[2]:


# Set the figure size and layout settings for the plot
plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams["figure.autolayout"] = True

# Create a subplot for the plot
fig, ax = plt.subplots()

# Create a bar plot of the top 15 most common skills
ax = List_Skills_Df[List_Skills_Df.Skills_list!=""].value_counts()[:15].plot(
    kind='bar', xlabel='Skill', ylabel='Jobs', color='skyblue', edgecolor='black'
)

# Adding a title/header to the plot
ax.set_title('Top 15 Most Common Skills in Product Analyst Jobs')

# Rotating x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Highlight the first bar by assigning a different color
colors = ['orange' if i == 0 else 'skyblue' for i in range(len(ax.patches))]
ax.patches[0].set_color('orange')  # Highlight the first bar

# Adding labels to bars
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Adjust layout and display the plot
plt.tight_layout()
plt.show()


# In[3]:


# Explode the 'Missing_Skills' list column and create a DataFrame
List_Skills_Missing = Job_Details_df['Missing_Skills'].explode()
List_Skills_Missing_Df = pd.DataFrame(List_Skills_Missing).reset_index(drop=True)

# Display the top 20 most common missing skills
print(List_Skills_Missing_Df[List_Skills_Missing_Df.Missing_Skills!=""].value_counts()[:20])


# In[4]:


# Set the figure size and layout settings for the plot
plt.rcParams["figure.figsize"] = [15, 5]
plt.rcParams["figure.autolayout"] = True

# Create a subplot for the plot
fig, ax = plt.subplots()

# Create a bar plot of the top 20 most common missing skills
List_Skills_Missing_Df[List_Skills_Missing_Df.Missing_Skills!=""].value_counts()[:20].plot(
    ax=ax, kind='bar', xlabel='Skill', ylabel='Frequency', color='skyblue', edgecolor='black'
)

# Adding a title/header to the plot
ax.set_title('Top 20 Most Common Missing Skills in Product Analyst Jobs')

# Rotating x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Display the plot
plt.tight_layout()
plt.show()


# In[5]:


# Create a histogram plot
fig, ax = plt.subplots(figsize=(15, 5))

# Filter and prepare data for the histogram
data_for_histogram = Job_Details_df[(Job_Details_df.Full_Time) & (Job_Details_df['Lower_Range'] != 0) & (Job_Details_df['Lower_Range'].apply(lambda x: 'hr' not in str(x)))]
data_for_histogram = data_for_histogram['Lower_Range'].apply(lambda x: int(str(x).replace(",", ""))).to_list()

# Create the histogram
ax.hist(data_for_histogram, bins=10)

# Adding labels and title
ax.set_xlabel('Salary Range')
ax.set_ylabel('Number of Jobs')
ax.set_title('Distribution of Salary Ranges for Full-Time Product Analyst Jobs')

# Display the plot
plt.show()


# In[6]:


# Create a histogram plot
fig, ax = plt.subplots(figsize=(15, 5))

# Filter and prepare data for the histogram
data_for_histogram = Job_Details_df[(Job_Details_df.Full_Time) & (Job_Details_df['Higher_Range'] != 0) & (Job_Details_df['Higher_Range'].apply(lambda x: 'hr' not in str(x)))]
data_for_histogram = data_for_histogram['Higher_Range'].apply(lambda x: int(str(x).replace(",", ""))).to_list()

# Create the histogram
ax.hist(data_for_histogram, bins=10)

# Adding labels and title
ax.set_xlabel('Salary Range')
ax.set_ylabel('Number of Jobs')
ax.set_title('Distribution of Higher Salary Ranges for Full-Time Product Analyst Jobs')

# Display the plot
plt.show()


# In[7]:


# Extracting company information from Primary_Detail column
Job_Details_df['Company'] = Job_Details_df.Primary_Detail.apply(lambda x: x.replace("\n","· ").split(" · ")[0])

# Extracting location information from Primary_Detail column
Job_Details_df['Location_Job'] = Job_Details_df.Primary_Detail.apply(lambda x: x.replace("\n","· ").split(" · ")[1].split("(")[0])

# Extracting remote work information from Primary_Detail column
Job_Details_df['Remote'] = Job_Details_df.Primary_Detail.apply(lambda x: 
    x.replace("\n","· ").split(" · ")[1].split("(")[1].replace(")","").replace("]","").replace("]","").replace("Reposted","").replace(" ","")
    if len(x.replace("\n","· ").split(" · ")[1].split("(")) > 1
    else x.replace("\n","· ").split(" · ")[1].split("(")
)

# Standardizing remote work information
Job_Details_df['Remote'] = Job_Details_df['Remote'].apply(lambda x: x if x in ['Remote','On-site','Hybrid'] else 'On-site')

# Extracting job duration information from Primary_Detail column
Job_Details_df['Duration'] = Job_Details_df.Primary_Detail.apply(lambda x: x.replace("\n","· ").split(" · ")[2].replace("·",""))


# In[16]:





# In[8]:


# Set of stopwords from the NLTK library
stop_words = set(stopwords.words('english'))

# Additional words to clean from the text
clean_words = ['job', 'About', 'opportunity']

# Function to tokenize and clean text data
def token_data(text):
    tokenized_text = nltk.word_tokenize(text.lower())  # Tokenize and convert to lowercase
    filtered_tokens = [word for word in tokenized_text if word.lower() not in stop_words]  # Remove stopwords
    filtered_tokens = [word for word in filtered_tokens if len(word) >= 3 and word not in clean_words]  # Remove short words and specified clean_words
    return filtered_tokens

# Apply the token_data function to create a new column 'About_section_Clean'
Job_Details_df['About_section_Clean'] = Job_Details_df.Secondary_Detail.apply(lambda x: token_data(x))

# Explode the 'About_section_Clean' column and create a DataFrame
List_About = Job_Details_df['About_section_Clean'].explode()
List_About_Df = pd.DataFrame(List_About).reset_index(drop=True)


# In[9]:


# Display the top 50 most common cleaned words
print(List_About_Df[List_About_Df.About_section_Clean!=""].value_counts()[:50])


# In[10]:


# Updated list of words to clean
clean_words = ['job', 'About', 'equal', 'opportunity', 'national', 'origin', 'sexual', 'orientation', 'gender', 'veteran',
            'race', 'color', 'dental', 'vision', 'paid', 'medical', 'marital', 'regard', 'federal', 'state', 'genetic',
            'protected', 'status', 'religion', 'age', 'sex', 'identity', 'united', 'states'
            ]

# Function to tokenize and create bigrams from text data
def token_data_gram(text, n):
    tokenized_text = nltk.word_tokenize(text.lower())  # Tokenize and convert to lowercase
    filtered_tokens = [word for word in tokenized_text if word.lower() not in stop_words]  # Remove stopwords
    filtered_tokens = [word for word in filtered_tokens if len(word) >= 3 and word not in clean_words]  # Remove short words and specified clean_words
    bgrams = list(ngrams(filtered_tokens, n))  # Create n-grams (bigrams in this case)
    return bgrams

# Apply the token_data_gram function to create a new column 'Bigram'
Job_Details_df['Bigram'] = Job_Details_df.Secondary_Detail.apply(lambda x: token_data_gram(x, 2))

# Explode the 'Bigram' column and create a DataFrame
List_About = Job_Details_df['Bigram'].explode()
List_About_Df = pd.DataFrame(List_About).reset_index(drop=True)


# In[11]:


# Display the top 50 most common bigrams
print(List_About_Df[List_About_Df.Bigram!=""].value_counts()[:50])


# In[58]:


#Save Data
Job_Details_df.to_csv("Job_Details_df_partial_clean.csv",index=False)


# In[ ]:




