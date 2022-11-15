#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset - [Hospital Appointment No-Show Dataset]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row
# 
# In this project we will answer some question on why patients miss their scheduled appointment. We will be predicting some of the factors that affecting patient attendance in the Hospital.
# 
# 
# ### Question(s) for Analysis
# 
# Does the patient Gender and Age has any effect on attendance? Does receiving SMS remainder increase the chance of a patient showing for their appointment? Does the location or neighborhood of the patient play a role in missing or showing up for appointment? Does the disease type affect the patient's that show up or missed appointment?

# In[4]:


# Python Library for Data Analysis
import pandas as pd

# Numpy is the fundamental package for scientific computing in python
import numpy as np

# Matplotlib is the plotting library for the python programming language and it's numerical mathematics extension for Numpy
import matplotlib.pyplot as plt

# Is a library for making statistical graphics in python
import seaborn as snb

# It sets the baeckend of Matplotlib for the 'inline' backend
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# ### General Properties

# In[5]:


# Load Dataset Using Pandas
df=pd.read_csv('KaggleV2-May-2016.csv')

# Get the dataframe
df.head()


# In[6]:


# Exploring the shape of the dataset
df.shape


# In[7]:


# Getting more information about the dataset
df.describe()


# In[8]:


# Checking -1 min age
mask=df.query('Age=="-1"')
mask


# In[9]:


# Getting infomation on missing data
df.info()


# In[10]:


# Showing the types of data contain by each colum
df.dtypes


# In[11]:


# Checking for duplicated values
df.duplicated().sum()


# In[12]:


# Checking for unique values in the dataset
df.nunique()


# In[13]:


# Checking for unique patient id 
df['PatientId'].nunique()


# In[14]:


# Checking for duplicated patient Id
df['PatientId'].duplicated().sum()


# ## Data Cleaning

# In[15]:


# Dropping the -1 value in the Age colum of the dataset
df.drop(index=99832, inplace=True)
df.describe()


# In[16]:


# Correcting colum names
df.rename(columns={'Hipertension':'Hypertension'}, inplace= True)
df.rename(columns={'No-show':'No_Show'}, inplace= True)
df.head()


# In[17]:


# Removing duplicates values
df.drop_duplicates(['PatientId', 'No_Show'], inplace= True)
df.shape


# In[18]:


# Renoving unnecessary data
df.drop(['PatientId', 'AppointmentID', 'ScheduledDay', 'AppointmentDay'], axis=1, inplace= True)
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Research Question 1 (Are young people showing up for appointment more? Are women more likely to showup for schedule appointments than men?)

# In this stage we were able to gather our Data from a CSV file and explore the first few rows to see the sturcture of the data and it's general properties. We then check to see the dimention of the data, checked the data for duplicated values, missing values and possible errors; We found some duplicated values in the 'PatiendId' column and remove them.  checked the dataset type to see if there are any further missing data to handle. And lastly we were able to see some statistical information about the data on min, max, and mean. And finally we cleaned the data by removing duplicates, unnecessary data, correcting the columns names and dropping unnecessary columns.

# Now that I have trimmed and cleaned my data, it's time to move on to exploration. Computing statistics and creating visualizations with the goal of addressing the research questions that I posed in the Introduction section.

# In[19]:


# Creating visualization of the columns using histogram
df.hist(figsize=(14,4.3));


# In[20]:


# Deviding the patient in to two (2) groups 'show' and 'noshow' and exploring them
show = df.No_Show == 'No'
noshow = df.No_Show == 'Yes'
df[show].count(), df[noshow].count()


# In[22]:


# Does Age Affect the Attendance?
def attendance(df, col_name, attended, absent): # Setting
    
    plt.figure(figsize= [18,5])
    df[col_name][show].hist(alpha=.5, bins=10, color='maroon', label='show')
    df[col_name][noshow].hist(alpha=.5, bins=10, color='red', label='noshow')
    plt.legend();
    plt.title('Comparison Acc. to Age')
    plt.xlabel('Age')
    plt.ylabel('Patients Number');
attendance(df, 'Age', show,noshow)


# In[23]:


# Checking if Age and Chronic diseases affect the attendance
plt.figure(figsize=[18,5])
df[show].groupby(['Hypertension', 'Diabetes']).mean()['Age'].plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby(['Hypertension', 'Diabetes']).mean()['Age'].plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acc. to Age, Chronic Diseases')
plt.xlabel('Chronic Diseases')
plt.ylabel('mean Age')


# In[24]:


# Checking if gender affect the attendance (Checking for attended gender)
def attendance(df, col_name, attended, absent):
    plt.figure(figsize= [14,6])
    df[col_name][show].value_counts(normalize= True).plot(kind= 'pie', label= 'show')
    plt.legend();
    plt.title('Comparison Between Gender and Attendance')
    plt.xlabel('Gender')
    plt.ylabel('Number of Patients')
attendance(df, 'Gender', show, noshow)


# In[25]:


# Checking if gender affect the attendance (Checking for absent gender)
def attendance(df, col_name, attended, absent):
    plt.figure(figsize= [14,6])
    df[col_name][show].value_counts(normalize= True).plot(kind= 'pie', label= 'noshow')
    plt.legend();
    plt.title('Comparison Between Gender and Absent')
    plt.xlabel('Gender')
    plt.ylabel('Number of Patients')
attendance(df, 'Gender', noshow, show)


# In[26]:


# Checking for comparison between gender and age
plt.figure(figsize= [16,6]) # Setting fig. size
df[show].groupby('Gender').Age.mean().plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby('Gender').Age.mean().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Between Gender and Age')
plt.xlabel('Gender')
plt.ylabel('Mean Age');


# In[27]:


print(df[show].groupby('Gender').Age.mean(), df[noshow].groupby('Gender').Age.mean())
print( df[show].groupby('Gender').Age.median(), df[noshow].groupby('Gender').Age.median())


# ### Research Question 2  (Do recieving SMS encourage more attendance? Does neighbourhood affect the attendance?)

# In[28]:


# Does Receiving SMS affect the attendance
def attendance(df, col_name, attended, absent):
    plt.figure(figsize= [18,7])
    df[col_name][show].hist(alpha=.5, bins= 15, color= 'maroon', label= 'show')
    df[col_name][noshow].hist(alpha=.5, bins= 15, color= 'red', label= 'noshow')
    plt.legend();
    plt.title('Comparison Acc. to Receiving SMS')
    plt.xlabel('SMS')
    plt.ylabel('Patients Number')
attendance(df, 'SMS_received', show, noshow)


# In[29]:


# Checking if the Neighbourhood affect the attendance
plt.figure(figsize= [14,8]) # Setting fig. size
df.Neighbourhood[show].value_counts().plot(kind= 'bar', color= 'maroon', label= 'show')
df.Neighbourhood[noshow].value_counts().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acc. to Neighbourhood')
plt.xlabel('Neighbourhood')
plt.ylabel('Patients Number');


# In[30]:


# Checking Comparison between Neighnourhood and SMS_receiving mean.
plt.figure(figsize= [18,3]) # Setting fig size
df[show].groupby('Neighbourhood').SMS_received.mean().plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby('Neighbourhood').SMS_received.mean().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acc. to Neighbourhood, SMS_receiving')
plt.xlabel('Neighbourhood')
plt.ylabel('Patients Number');


# In[31]:


# Checking comparison between Neighbourhood and Age mean
plt.figure(figsize=[18,3]) # Setting fig. size
df[show].groupby('Neighbourhood').Age.mean().plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby('Neighbourhood').Age.mean().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acct. to Neighbourhood, Age Mean')
plt.xlabel('Neighbourhood')
plt.ylabel('Mean Age');


# Ptient attendance differ by neighbourhood; AEROPORTO has the highest attendance rate followed by the rest. Despite having the highest SMS received in ILHAS OCEANICAS DE TRINDADE it has the highest no show rate.

# <a id='conclusions'></a>
# ## Conclusions
# 
# 

# Having finished the analysis we found that Neighbourhood has the heighest effect on attendance having some neighbourhood having
# the greater number of patients and also having the greater number of showing.
# 
# Also Age has a greater effect on the showing rate as the age range 0:10 has the highest number of shows and the age range 40:100 and above has lower shows.

# ## Limitations

# There may be some patterns that I wasn't able to identify due to my lack of expertise. However, from the data we know that if the hospital does not capture the patients details correcly the petient will not recieve an SMS but if patient details where capture correctly the chances of the person coming for hospital appointments will increase. So we need to search for more factors to help patient remenber their appointments and show up
# 
# Thers is no clear correlation between showing and chronic diseases, gender and enrolment in the walfare program.

# In[34]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

