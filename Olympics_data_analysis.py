# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:33:40 2023

@author: dhair
"""
#************** Importing Library First **************

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#************ Importing Dataset ************

df = pd.read_csv('/Users/dhair/OneDrive/Desktop/athlete_events.csv')
region_df = pd.read_csv('/Users/dhair/OneDrive/Desktop/noc_regions.csv')

#print(df.shape)

#********* Now filter the data on the bases of summer season **********

df = df[df['Season'] == 'Summer']
#print(df.shape)

#******** Merge the Dataset on the bases of NOC ***********************

df = df.merge(region_df , on = 'NOC' , how = 'left')
#print(df)

#print(df['region'].unique())

#*********** Check the null values and duplicate values *******
#print(df.isnull().sum())
#print(df.duplicated().sum())

#********** Remove Duplicates rows ************** 

df.drop_duplicates(inplace = True)

#print(df.duplicated().sum())

#******** Do onehotEncode Medal column ************

#print(df['Medal'].value_counts())
#print(pd.get_dummies(df['Medal']))

df = pd.concat([df ,pd.get_dummies(df['Medal'])],axis =1)

#***********  Apply GroupBY fun on NOC column and sum all columns ************

#print(df.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending = False).reset_index())

#*********** Remove the duplicate subsets ****************

medal_tally = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal']) 

#**************Using the GroupBy fun her *********

#medal_tally = medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending = False).reset_index()
medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending = False).reset_index()
#print(medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending = False).reset_index())

#*********** Create a new column TOTAL & SUM of all columns G S B **************

medal_tally['Total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
#print(medal_tally)

#*********Create a new column of YEAR with the year and covert into a list *********

years = df['Year'].unique().tolist() 
#print(years)
years.sort()
years.insert(0,"Overall")

#print(years)

#*********** Extract the country from the region column *********************

country = np.unique(df['region'].dropna().values).tolist()
country.sort()
country.insert(0,"Overall")
#print(country)

#********* Create a function to fetch the country and year in the dataset *******

def fetch_medal_tally(df , year , country):
    medal_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year' , ascending = True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending = False).reset_index()
    
    x['Total'] = x['Gold']+x['Silver']+x['Bronze']
    print(x)

#medal_df = df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])

#*********** Now finding the overall Analysis Of Olympics some key points *************
                     #********#
                     
             # 1- No. of Edition 
             # 2- No. of Cities
             # 3- No. of events/sports 
             # 4- No. of Athletes 
             # 5- Participating Nations  
             
                     #********#
#print(df['Year'].unique().shape[0] -1)
#print(df['City'].unique().shape[0])
#print(df['Sport'].unique().shape[0])
#print(df['Event'].unique().shape[0])
#print(df['Name'].unique().shape[0])
#print(df['region'].unique().shape[0])

edition = df['Year'].unique().shape[0] -1
cities = df['City'].unique().shape[0]
sports = df['Sport'].unique().shape[0]
events = df['Event'].unique().shape[0]
Athletes = df['Name'].unique().shape[0]
Nation = df['region'].unique().shape[0]

#********** Now draw  a plot on the bases of year and nation  ************

#print(df.drop_duplicates(['Year' , 'region'])['Year'].value_counts().reset_index().sort_values('index'))

nation_over_time = df.drop_duplicates(['Year' , 'region'])['Year'].value_counts().reset_index().sort_values('index')

nation_over_time.rename(columns = {'index': 'Edition' , 'Year': 'No of Countries'} , inplace = True)

#********* Importing The plotly library ***********
#import plotly.io as pio
#pio.renderers.default = "svg"

import plotly.express as px

fig = px.line(nation_over_time, x = "Edition", y= "No of Countries")
#fig.show()

sns.lineplot(data = nation_over_time , x = 'Edition' , y = 'No of Countries')
#plt.xlabel('Edition')
#plt.xlabel('No of Countries')
#plt.lineplot(Edition , No of Countries , color = 'red')
plt.show()

#************ Event analysis based on the year *********

#print(df.drop_duplicates(['Year' , 'Event'])['Year'].value_counts().reset_index().sort_values('index'))
event_over_time = df.drop_duplicates(['Year' , 'Event'])['Year'].value_counts().reset_index().sort_values('index')
event_over_time.rename(columns={'index': 'Edition' , 'Year': 'No of Events'},inplace = True)

fig = px.line(event_over_time , x = 'Edition' , y = 'No of Events')
#fig.show()

#********* Draw a heatmap for howmany events in every sports using the pivot table *************

x= df.drop_duplicates(['Year' ,'Sport' , 'Event'])

#******** Print Pivot Tabel ****************

print(x.pivot_table(index = 'Sport' , columns = 'Year' , values = 'Event' , aggfunc = 'count').fillna(0).astype('int'))
plt.figure(figsize = (25,25))
sns.heatmap(x.pivot_table(index = 'Sport' , columns = 'Year' , values = 'Event' , aggfunc = 'count').fillna(0).astype('int'),annot = True)
plt.show()

#****** Create a function for finding the athlete who won howmany medal in olympics **********

def most_successful (df , sport):
    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x =temp_df['Name'].value_counts().reset_index().head(15).merge(df , left_on = 'index' , right_on = 'Name' , how = 'left')[['index', 'Name_x', 'Sport' ,'region']].drop_duplicates('index')
    x.rename(columns = {'index': 'Name', 'Name':'Medals'},inplace = True)
    return x
#print(most_successful(df , 'Gymnastics')  

#************* Country Wise Analysis *******************
#1- Country Wise medal tally per year
#2- What countries are good at heatmap
#3- Most Successful Athlete(Top 10)

#print(df.dropna(subset=['Medal']))
temp_df = df.dropna(subset=['Medal'])
temp_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'] , inplace = True)

#print(temp_df.groupby('Year').count()['Medal'])
new_df = temp_df[temp_df['region'] == 'USA']
#print(new_df.groupby('Year').count()['Medal'])
final_df = new_df.groupby('Year').count()['Medal'].reset_index()
#print(final_df)

fig = px.line(final_df , x = 'Year' , y = 'Medal')
#fig.show()

#******** Generate a heatmap for which country is good in which sport **********

new_df = temp_df[temp_df['region'] == 'India']
#*********Create a pivot table **********
plt.figure(figsize = (20,20))
sns.heatmap(new_df.pivot_table(index = 'Sport', columns = 'Year' , values = 'Medal' , aggfunc = 'count').fillna(0),annot = True)
#plt.show()

#********* Create a funtion to find the Top 10 player ****************

def most_successful (df , country):
    temp_df = df.dropna(subset = ['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
    x =temp_df['Name'].value_counts().reset_index().head(15).merge(df , left_on = 'index' , right_on = 'Name' , how = 'left')[['index', 'Name_x', 'Sport' ]].drop_duplicates('index')
    x.rename(columns = {'index': 'Name', 'Name':'Medals'},inplace = True)
    return x

print(most_successful(df, 'India'))


#4- Athlete wise analysis  

import plotly.figure_factory as FF

athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])
x1 = athlete_df['Age'].dropna()
x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

fig = FF.create.distplot([x1,x2,x3,x4] , ['Overall' , 'Gold Medalist', 'Silver Medalist','Bronze Medalist'],show_hist = False , show_rug = False)
fig.show()




















