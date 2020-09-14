#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import datetime
from datetime import date
import sys


# In[2]:


def empty_db():
    with open('db.json', 'w') as outfile:
        json.dump({}, outfile)


# In[3]:


def read_db():
    with open('db.json') as json_file:
        return(json.load(json_file))


# In[4]:


def validate_date(val):
    try:
        datetime.datetime.strptime(val, '%m/%d/%Y')
        pd.to_datetime(val).year
        if date.today() >= pd.to_datetime(val).date() >= pd.to_datetime('01/01/1900').date():
            return True
        else:
            return False
    except ValueError:
        return False
    
def get_date(dateType):
    dt = input(dateType + ' - Enter format MM/DD/YYYY:\n')
    if dt != '':
        if validate_date(dt) == False:
            dFormat = False
            while dFormat == False:
                dt = input(dateType + ' - Wrong Format or Date out of Range - Enter format MM/DD/YYYY:\n')
                if dt != '':
                    dFormat = validate_date(dt)
                else:
                    dFormat = True
    return dt


# In[5]:


def validate_fin(val):
    try:
        for n in [' ', '$', ',']:
            val = val.replace(n, '')
        float(val)
        if val.lower() != 'nan':
            return True
        else:
            return False
    except ValueError:
        return False
    
def get_fin(finType):
    fin = input(finType + ':\n')
    if fin != '':
        if validate_fin(fin) == False:
            fFormat = False
            while fFormat == False:
                fin = input(finType + ' - Invalid Entry - Enter a non-negative financial value:\n')
                if sum(fin.replace(' ','').startswith(n) for n in ['-','$-',',-']) > 0:
                    continue
                if fin != '':
                    fFormat = validate_fin(fin)
                else:
                    fFormat = True
    if fin != '':
        for n in [' ', '$', ',']:
            fin = fin.replace(n, '')
        fin = round(float(fin),2)
    return fin


# In[6]:


def add_user():
    dct = read_db()
    gender = input('Gender:\n')
    dob = get_date('Date of Birth')
    ssn = input('Social Security Number:\n')
    smokeStatus = input('Smoking Status:\n')
    allergies = input('Allergies:\n')
    medCtns = input('Medical Conditions:\n')
    
    newKey = str(len(dct) + 1)
    dct.update({newKey: {'gender': gender,
                        'dob': dob,
                        'ssn': ssn,
                        'smokeStatus': smokeStatus,
                        'allergies': allergies,
                        'medCtns': medCtns,
                        'events': {}}})
    
    with open('db.json', 'w') as outfile:
        json.dump(dct, outfile)
        
    print('\nAdded new user ' + str(newKey))


# In[7]:


def add_event():
    dct = read_db()
    user = input('\nPlease provide a user to add an insured event:\n')
    crnt_users = list(dct.keys())
    crnt_users_dsp = str([int(n) for n in dct.keys()]).strip('[]')
    
    while user not in crnt_users:
        user = input('\nNot a valid user - please select from user(s) ' + crnt_users_dsp + '\n')
    
    lossDate = get_date('Date of Incidence')
    lossType = input('Type of Issue:\n')
    billedAmount = get_fin('Billed Amount')
    coveredAmount = get_fin('Covered Amount')
    
    newEventKey = str(len(dct[user]['events']) + 1)
    dct[user]['events'].update({newEventKey: {'lossDate': lossDate,
                                            'lossType': lossType,
                                            'billedAmount': billedAmount,
                                            'coveredAmount': coveredAmount}})
    
    with open('db.json', 'w') as outfile:
        json.dump(dct, outfile)


# In[8]:


def list_insured():
    dct = read_db()
    print('\n')
    for k in dct.keys():
        print(k)


# In[9]:


def list_events():
    dct = read_db()
    user = input('\nPlease provide a user:\n')
    crnt_users = list(dct.keys())
    crnt_users_dsp = str([int(n) for n in dct.keys()]).strip('[]')
    
    while user not in crnt_users:
        user = input('\nNot a valid user - please select from user(s) ' + crnt_users_dsp + '\n')
    
    if len(dct[user]['events']) == 0:
        print('\nNo Events for this user')
    else:
        print('\nUser ' + user + ':\n')
        for k,v in dct[user]['events'].items():
            print('Event ' + str(k) + ':')
            for k2,v2 in v.items():
                print(k2 + ': ' + str(v2))
            print('\n')


# In[10]:


def view_agg():
    dct = read_db()
    totalCovered = 0
    claimsPerYear = {}
    avgAge = {'sm': 0, 'ct': 0}
    
    for k,v in dct.items():
        if v['dob'] != '':
            dobDt = pd.to_datetime(v['dob'])
            mo = dobDt.month
            dy = dobDt.day
            yr = date.today().year
            
            avgAge['sm'] += yr - dobDt.year
            if datetime.datetime(year=yr, month=mo, day=dy).date() > date.today():
                avgAge['sm'] -= 1
            
            avgAge['ct'] += 1
        if len(v['events']) > 0:
            for k2, v2 in v['events'].items():
                if v2['coveredAmount'] != '':
                    totalCovered += v2['coveredAmount']
                yr = pd.to_datetime(v2['lossDate']).year
                if str(yr) != 'nan':
                    if yr not in claimsPerYear:
                        claimsPerYear.update({yr: 1})
                    else:
                        claimsPerYear[yr] += 1
    
    print('\nTotal covered amount for all claims: $' + str(totalCovered))
    if len(claimsPerYear) > 0:
        print('Claims per year:')
        for k,v in claimsPerYear.items():
            print(str(k) + ': ' + str(v))
    if avgAge['ct'] > 0:
        print('Average age of insured: ' + str(round(avgAge['sm']/avgAge['ct'])))


# In[11]:


msgSelect = "\nPlease select from the following options to either \nadd a new insured user, add an insurance event for a user, \nlist all insured, list all events associated with a user, \nor view aggregate results of data: \n\nAdd User \nAdd Event \nList Insured \nList Events \nView Agg\n\n"

msgExit = "\nNot a valid option, please try again. To exit service, enter 'exit'"

optTpl = tuple('''add user, add event, list insured, list events, view agg, exit'''.split(', '))


# In[12]:


def select_options():
    dct = read_db()
    opt = input(msgSelect).lower()
    if opt in optTpl:
        if opt == 'add user':
            add_user()
        elif opt == 'exit':
            sys.exit('Service stopped. Rerun app to start over.')
        elif len(dct) > 0:
            if opt == 'add event':
                add_event()
            elif opt == 'list insured':
                list_insured()
            elif opt == 'list events':
                list_events()
            elif opt == 'view agg':
                view_agg()
        else:
            print('\nDatabase is empty - please add one or more users')
        return(opt)
    else:
        print(msgExit)

def start_selection():
    choice = None
    while choice == None:
        choice = select_options()


# In[13]:


def continue_options():
    optc = input('\nContinue? Y or N\n\n')
    if optc.lower() in ['y', 'n']:
        return(optc.lower())
    else:
        print(msgExit)

def continue_selection():
    yesOrNo = None
    while yesOrNo == None:
        yesOrNo = continue_options()
    return yesOrNo


# In[14]:


empty_db()


# In[16]:


keepGoing = 'y'

while keepGoing == 'y':
    start_selection()
    keepGoing = continue_selection()
    
sys.exit('Thank you - service complete. To start over, rerun app.')

