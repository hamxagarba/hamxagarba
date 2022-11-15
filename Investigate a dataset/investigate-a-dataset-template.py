#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset (Patient No Show Appointments May 2016.csv)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# ## Introduction
# 
# This dataset collects information
# from 100k medical appointments in
# Brazil and is focused on the question
# of whether or not patients show up
# for their appointment. A number of
# characteristics about the patient are
# included in each row.
# 
# ● ‘ScheduledDay’ tells us on
# what day the patient set up their
# appointment.
# 
# ● ‘Neighborhood’ indicates the
# location of the hospital.
# 
# ● ‘Scholarship’ indicates
# whether or not the patient is
# enrolled in Brasilian welfare
# program Bolsa Família.
# 
# ● Be careful about the encoding
# of the last column: it says ‘No’ if
# the patient showed up to their
# appointment, and ‘Yes’ if the patient did not show up
# 
# ## Describtion of the Dataset
# I am going to use a CSV file which contains the data I am going to use.
# 
# ## Questions for Analysis
# What are the factors to consider in order to know weather a patient is going to show up for his/her appointment.
# 

# In[53]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as snb
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Data Wrangling
# 
# 
# ### General Properties

# In[54]:


df=pd.read_csv('KaggleV2-May-2016.csv')
df.head()


# In[55]:


# Exploring the shape of the dataset
df.shape


# The dataset has 110527 rows and 14 colums

# In[56]:


# Getting more information about the dataset
df.describe()


# This is the summary statistics of the dataset; it gives us an insight into tha statistics of the dataset. If you notice you'll see -1 as the min of age which is an error; the next cell will query that error.

# In[57]:


# Checking -1 min age
mask=df.query('Age=="-1"')
mask


# In[58]:


# Getting infomation on missing data
df.info()


# The .info function shnows a metadata of the dataset showing types, number of rows and colums, colum names etc. it helps us to norrow down the content of the dataset and understand it's structure and shape.

# In[59]:


# Showing the types of data contain by each colum
df.dtypes


# The dtypes function shows us the type of each colum specifically. You may see that there are no 'strings' in the types; that is because python recognize and stores 'strings' as object; so where we see 'object' we'll it's a string.

# In[60]:


# Checking for duplicated values
df.duplicated().sum()


# There are no duplicated values in the dataset

# In[61]:


# Checking for unique values in the dataset
df.nunique()


# In[62]:


# Checking for unique patient id 
df['PatientId'].nunique()


# There are 62299 out of 110527 unique patient Id

# In[63]:


# Checking for duplicated patient Id
df['PatientId'].duplicated().sum()


# There are 48228 duplicated patient Id

# ## Data Cleaning Stage

# In[64]:


# Dropping the -1 value in the Age colum of the dataset
df.drop(index=99832, inplace=True)
df.describe()


# In[65]:


# Correcting colum names
df.rename(columns={'Hipertension':'Hypertension'}, inplace= True)
df.rename(columns={'No-show':'No_Show'}, inplace= True)
df.head()


# As you can see the column names for 'Hipertension' and 'No-show' has been corrected and change to 'Hypertention' and 'No_SHow' respectively.

# In[66]:


# Removing duplicates values
df.drop_duplicates(['PatientId', 'No_Show'], inplace= True)
df.shape


# The duplicated values have been droped from 110526 rows to 71816 rows

# In[67]:


# Renoving unnecessary data
df.drop(['PatientId', 'AppointmentID', 'ScheduledDay', 'AppointmentDay'], axis=1, inplace= True)
df.head()


# ## Data Wrangling Summary

# In this stage I was able to gather my Data from a CSV file and explore the first few rows to see the sturcture of my data and it's general properties. I was able to see the dimention of the data, checked the data for duplicated values, missing values and possible errors; I found some duplicated values in the 'PatiendId' column and remove them.  checked the dataset type to see if there are any furthr missing data to handle. And lastly I was able to see some statistical information about my data on min, max, and mean. And finally I cleaned my data by removing duplicates, unnecessary data, correcting the columns names and dropping unnecessary columns.

# ## Exploratory Data Analysis 

# Now that I have trimmed and cleaned my data, it's time to move on to exploration. Computing statistics and creating visualizations with the goal of addressing the research questions that I posed in the Introduction section.

# In[68]:


# Creating visualization of the columns using histogram
df.hist(figsize=(14,4.3));


# In[69]:


# Deviding the patient in to two (2) groups 'show' and 'noshow' and exploring them
show = df.No_Show == 'No'
noshow = df.No_Show == 'Yes'
df[show].count(), df[noshow].count()


# The Number of showed is 54153 which is greater than number of no show 17663

# In[70]:


# Getting the mean of both groups
df[show].mean(), df[noshow].mean()


# Mean age for show is 37 and the mean age for noshow is 34, but the SMS_received mean of noshow is higher than that of show whnich means that we need to look into our messaging strategies.

# ## Investigation for the Influencing Factors on the Attendance Rate

# In[71]:


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


# Thnis histogram shows that patient from 0:10 years of age are the most showing and patient from 45:100 and above are the least showing.

# In[72]:


# Checking if Age and Chronic diseases affect the attendance
plt.figure(figsize=[18,5])
df[show].groupby(['Hypertension', 'Diabetes']).mean()['Age'].plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby(['Hypertension', 'Diabetes']).mean()['Age'].plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acc. to Age, Chronic Diseases')
plt.xlabel('Chronic Diseases')
plt.ylabel('mean Age')


# The Above figure show that there is correlation between Age and chronic diseases but there is no correlation between Age and attendance.

# In[73]:


# Checking if gender affect the attendance (Checking for attended gender)
def attendance(df, col_name, attended, absent):
    plt.figure(figsize= [14,6])
    df[col_name][show].value_counts(normalize= True).plot(kind= 'pie', label= 'show')
    plt.legend();
    plt.title('Comparison Between Gender and Attendance')
    plt.xlabel('Gender')
    plt.ylabel('Number of Patients')
attendance(df, 'Gender', show, noshow)


# In[74]:


# Checking if gender affect the attendance (Checking for absent gender)
def attendance(df, col_name, attended, absent):
    plt.figure(figsize= [14,6])
    df[col_name][show].value_counts(normalize= True).plot(kind= 'pie', label= 'noshow')
    plt.legend();
    plt.title('Comparison Between Gender and Absent')
    plt.xlabel('Gender')
    plt.ylabel('Number of Patients')
attendance(df, 'Gender', noshow, show)


# You'll notice that there is no change in attendance for both sexes in the pie chart. that show that gender does not affect the attendance.

# In[75]:


# Checking for comparison between gender and age
plt.figure(figsize= [16,6]) # Setting fig. size
df[show].groupby('Gender').Age.mean().plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby('Gender').Age.mean().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Between Gender and Age')
plt.xlabel('Gender')
plt.ylabel('Mean Age');


# In[76]:


print(df[show].groupby('Gender').Age.mean(), df[noshow].groupby('Gender').Age.mean())
print( df[show].groupby('Gender').Age.median(), df[noshow].groupby('Gender').Age.median())


# There is no correlation between Gender and  Age affecting the attendance; the mean adn the meadian of both sexes are almost thesame.

# In[77]:


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


# The number of patient showing withouth receiving SMS is higher than those whowing after receiving SMS.

# In[78]:


# Checking if the Neighbourhood affect the attendance
plt.figure(figsize= [14,8]) # Setting fig. size
df.Neighbourhood[show].value_counts().plot(kind= 'bar', color= 'maroon', label= 'show')
df.Neighbourhood[noshow].value_counts().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acc. to Neighbourhood')
plt.xlabel('Neighbourhood')
plt.ylabel('Patients Number');


# In[79]:


# Checking Comparison between Neighnourhood and SMS_receiving mean.
plt.figure(figsize= [18,3]) # Setting fig size
df[show].groupby('Neighbourhood').SMS_received.mean().plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby('Neighbourhood').SMS_received.mean().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acc. to Neighbourhood, SMS_receiving')
plt.xlabel('Neighbourhood')
plt.ylabel('Patients Number');


# this shows that only 5 Neighbourhood response to the SMS with ILHAS OCEANICAS DE TRINDADE having the highest response

# In[80]:


# Checking comparison between Neighbourhood and Age mean
plt.figure(figsize=[18,3]) # Setting fig. size
df[show].groupby('Neighbourhood').Age.mean().plot(kind= 'bar', color= 'maroon', label= 'show')
df[noshow].groupby('Neighbourhood').Age.mean().plot(kind= 'bar', color= 'red', label= 'noshow')
plt.legend();
plt.title('Comparison Acct. to Neighbourhood, Age Mean')
plt.xlabel('Neighbourhood')
plt.ylabel('Mean Age');


# Ptient attendance differ by neighbourhood; AEROPORTO has the highest attendance rate followed by the rest. Despite having the highest SMS received in ILHAS OCEANICAS DE TRINDADE it has the highest no show rate.

# ## Conclusions

# Having finished my analysis I found that Neighbourhood has the heighest effect on attendance having some neighbourhood having
# the greater number of patients and also having the greater number of showing. And some neighbourhood are clearly affected by SMS received and Age.
# 
# Also Age has a greater effect on the showing rate as the age range 0:10 has the highest number of shows and the age range 40:100 and above has lower shows.
# 
# Lastly I noticed that the number of showing patient by SMS received is lower than those without receiving the SMS. This shows that we need to revist our SMS sending strategy.

# ## Limitations

# Thers is no clear correlation between showing and chronic diseases, gender and enrolment in the walfare program.

# ## Thank You
