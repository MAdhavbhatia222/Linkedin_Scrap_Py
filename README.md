This repository contains code for data extraction from LinkedIn.
It has 3 parts - 
1. Job hyperlinks extraction: Data_Scrap_Linkedin-Product_Analyst_code_1
2. Extract data from job hyperlinks: Data_Scrap_Linkedin_Hyperlink-code_2
3. Data Analysis: Analysis_Job_Product_Analytics_Linkedin

Project Summary: Enhancing LinkedIn Profile and Resume with Data Analysis

Objective: Improve LinkedIn skills section and resume using insights gained from analyzing product analyst job postings on LinkedIn.

Data Gathering:

Utilized Selenium for web scraping to gather job posting data from LinkedIn.
Extracted job details, skills requirements, contact information, and other relevant data using BeautifulSoup.
Collected URLs of job postings for further analysis.

Data Cleaning:

Processed and cleaned the extracted data to prepare it for analysis.
Created functions to tokenize and clean text data, remove stopwords, and filter relevant information.

Data Analysis:
Identified common skills required for product analyst roles by analyzing skills listed in job descriptions.
Identified skills that candidates often lacked compared to the required skills.
Extracted lower and upper salary ranges from job postings.
Analyzed common bigrams (word pairs) in job descriptions to identify recurring patterns.

Visualization:
Used Matplotlib to create histograms and bar plots for salary distribution and skill insights.
Visualized the distribution of salary ranges for full-time product analyst jobs.
Created bar plots to showcase the most common skills and bigrams in job descriptions.

Outcomes:
Gained insights into the most sought-after skills for product analyst roles.
Identified skills candidates commonly lacked, helping to focus skill improvement efforts.
Determined salary ranges for product analyst jobs, aiding negotiation and expectation-setting.
Revealed recurring word pairs in job descriptions to inform resume and LinkedIn profile content.

Impact:
Enhanced my LinkedIn profile by incorporating relevant skills from the analysis.
Improved my resume by tailoring it to match the skills and requirements identified in job postings.


Sample Insights from Product Analyst Job Data Extraction.

Insight 1 - 
Communication is the most sought out skill.

![output_1_0](https://github.com/MAdhavbhatia222/Linkedin_Scrap_Py/assets/32282603/3ad621b9-56df-47da-92e0-d994382d6d43)

Insight 2 - 
Top 20 Most Common Missing Skills in my Profile for Product Analyst Jobs
![output_3_0](https://github.com/MAdhavbhatia222/Linkedin_Scrap_Py/assets/32282603/476a2abf-6392-457e-bea9-439327c056c9)

Insight 3 - 
Distribution of Lower Salary Ranges for Full-Time Product Analyst Jobs
![output_4_0](https://github.com/MAdhavbhatia222/Linkedin_Scrap_Py/assets/32282603/8909b59f-c484-476b-8c73-448326b40a36)

Insight 4 -
Distribution of Higher Salary Ranges for Full-Time Product Analyst Jobs
![output_5_0](https://github.com/MAdhavbhatia222/Linkedin_Scrap_Py/assets/32282603/024ff1d4-4839-4837-a2cc-d552b75b7356)
