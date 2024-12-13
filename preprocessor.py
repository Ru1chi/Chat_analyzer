# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 17:16:51 2024

@author: sr322
"""
import re

import pandas as pd
def preprocess(data):
    pattern = r'\[(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AP]M)\]\s(.*)'
    message = re.sub(pattern, '', data).strip()
    matches = re.findall(pattern, data)
    df = pd.DataFrame(matches, columns=['date_time', 'user_message'])
    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%y, %I:%M:%S %p')
    
    #seperate users and message
    users=[]
    messages=[]
    for message in df['user_message']:
       entry=re.split('([\w\W]+?):\s',message)
       if entry[1:]:
          users.append(entry[1])
          messages.append(entry[2])
       else:
          users.append('group_notification')
          messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    
    df['year']=df['date_time'].dt.year
    df['month_num']=df['date_time'].dt.month
    df['date']=df['date_time'].dt.date
    df['month']=df['date_time'].dt.month_name()
    df['day']=df['date_time'].dt.day
    df['day_name']=df['date_time'].dt.day_name()
    df['hour']=df['date_time'].dt.hour
    df['minute']=df['date_time'].dt.minute
    
    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
           period.append(str(hour)+"-"+str('00'))
        elif hour==0:
             period.append(str('00')+'-'+str(hour+1))
        else:
             period.append(str(hour)+'-'+str(hour+1))
    df['period']=period  
  
    return df


