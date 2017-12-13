#Imports
from __future__ import division
from bs4 import element
import sqlite3
import re

conn = sqlite3.connect('hurricanes.db')

def table_mapper(row):
    map = []
    for x in range(0, len(row.find_all('th'))):
        column_name = data_fit(row.find_all('th')[x]).replace(' ', '_')
        data_name = find_col(column_name)
        if data_name is None:
            continue
        map.append((x,data_name))
    return map

def fit_data(row, map):
    out = {'year':0000, 'tropical_storms':-1, 'major_hurricanes':-1,
    'number_of_hurricanes':-1, 'deaths':-1, 'damage':-1, 'notes':'', 'strongest_storm' :'',
     'retired_names':''}
    for curr in map:
        try:
            cleaned_item = data_fit(row.find_all('td')[curr[0]])
            out[curr[1]] = cleaned_item
        except IndexError:
            continue
    return out

def put_db(data):
    #start with blank notes
    notes = ''
    #first add in actual notes
    if 'notes' in data.keys() and len(data['notes']) > 0:
        notes += 'Notes: ' + data['notes'] + ' '
    #then add retired names and strongest storms
    if 'retired_names' in data.keys() and len(data['retired_names']) > 0:
        notes += 'Retired Names: ' + data['retired_names'] + ' '
    if 'strongest_storm' in data.keys() and len(data['strongest_storm']) > 0:
        notes += 'Strongest Storm: ' + data['strongest_storm']

    deaths = int_clean(data['deaths'])
    if deaths is None or deaths == -1:
        deaths = 'NULL'
    damage = process_dam(data['damage'])
    if damage is None or damage == -1:
        damage = 'NULL'
    conn.cursor().execute('INSERT INTO atlantic_hurricanes VALUES (?,?,?,?,?,?,?)', (data['year'],
        data['tropical_storms'], data['number_of_hurricanes'], data['major_hurricanes'],
         deaths, damage ,notes))
    conn.commit()

def data_fit(it):
    out = ''
    for part in it.contents:
        if type(part) is element.NavigableString:
            out += part + ' '
        elif type(part) is element.Tag:
            if len(part.contents) > 0:
                for it in part.contents:
                    if type(it) is element.NavigableString:
                        out += it + ' '
    out = out.strip().replace('\n','').replace('  ',' ').lower()
    return out

def clean_float(it):
    try:
        value = re.findall(r'[\d.]+', it)
        if len(value) == 1:
            return float(value[0])
        elif len(value)== 0:
            return None
        else:
            return float(int_clean(it))
    except ValueError:
        return None

def int_clean(it):
    try:
        out = 0
        all = re.findall('\d+', it)
        for part in all:
            out = int(part) + (out*(10**len(part)))
        return out
    except ValueError:
        return None

def process_dam(it):
    times = {'thousand': 1000, 'million': 1000000, 'billion': 1000000000}
    try:
        if type(it) is int:
            return it
        part = it.split()
        value = clean_float(part[0])
        if len(part)>1:
            value = value * times.get(part[1])
        return value
    except ValueError:
        return None

def find_col(column_name):
    for name in ['year','tropical_storms','major_hurricanes','number_of_hurricanes','deaths','damage','notes','strongest_storm']:
        if name in column_name:
            return name



