#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[33]:


import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import matplotlib.pyplot as plt


# # Import Data

# In[7]:


cars_data = pd.read_csv(r'C:\Users\fast\Downloads\Span_new.csv')
cars_data.head()


# # Pre Process Data/ Exploratory data analysis

# In[8]:


cars_data.columns


# In[9]:


cars_data.drop([3,4,5,6,7], axis = 0, inplace= True)


# In[10]:


cars_data[['gear','fuel_type']]


# In[11]:


cars_data['fuel_type'].value_counts()


# In[12]:


cars_data['gear'].value_counts()


# In[35]:


manual_cars = cars_data[(cars_data.make == 'Bmw') & (cars_data.age >= 1990 )]
manual_cars


# # EDA

# In[13]:


cars_data.rename({'age':'model_year'}, axis = 1, inplace= True)
cars_data.gear.value_counts()


# In[41]:


cars_data.replace({'manual':0, 'automatic': 1, 'unknown':2, 'semi-automatic': 3})


# In[43]:


cars_data['color'] = cars_data.power * 1.5
cars_data


# In[44]:


cars_data[cars_data.make != 'Porsche']


# In[55]:


dv = pd.DataFrame(cars_data.price)
iv = cars_data[['gear', 'make', 'kms', 'fuel_type' ]]


# # Visualize Data

# # Split Data

# In[ ]:


# Defining dependent and idependent variable


# In[14]:


independent_vaiable = cars_data[['model_year','power','kms']]


# In[15]:


dependent_vaiable = cars_data[['price']]


# In[ ]:





# In[27]:


# train test split

x_train, x_test, y_train, y_test = train_test_split(independent_vaiable, dependent_vaiable, test_size= 0.2)


# In[36]:


# Linear regression

# OLS = ordinary least square (Linear regression in stats is called OLS)

# Create regression model
regression_model = sm.OLS(y_train, x_train)

# Create regression line
results = regression_model.fit()


results.summary()


# In[43]:


# Class practice

dep_var = cars_data['price']
ind_var = cars_data[['model_year','kms','months_old','power']]
x_train, x_test, y_train, y_test = train_test_split(ind_var, dep_var, test_size= 0.2)

regression_model = sm.OLS(y_train, x_train)

results = regression_model.fit()

results.summary()


# # Conduct predictive modeling 

# In[46]:


# 'model_year','kms','months_old','power'
results.predict([50, 10000 , 80, 300 ])


# In[49]:


results.predict(x_test).head()


# # Visualize Data

# # Check Accuracy

# In[ ]:





# # Deploy Model

# In[ ]:




