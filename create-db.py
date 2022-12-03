
from datetime import datetime
import sqlite3
from tokenize import String
from operator import itemgetter
from typing import List

def detect_latest_ver_from_script_list(list : List, known_latest : String):
    max_ver =  max(list, key=itemgetter(1) )[0];
    if max_ver > known_latest:
        return max_ver;
    return known_latest;

def create_latest():

    latest_ver = '0.0.0' 

    conn = sqlite3.connect('event.sqlite')
    if table_exists(conn, "__ver") == False:
        print('"__ver" Table does not exist. Creating it...');
        conn.execute('''CREATE TABLE __ver
             (date text, ver text)''')
        # Insert ver mark
        conn.execute("INSERT INTO __ver VALUES ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "', '0.0.0')")
    
    #this should represent all schema objects
    sql_stmt = list();
    sql_stmt = sql_stmt + sql_gen_create_Domain();
    sql_stmt = sql_stmt + sql_gen_create_Subject();
    sql_stmt = sql_stmt + sql_gen_create_Occurance();
    
    latest_ver = detect_latest_ver_from_script_list(sql_stmt, latest_ver); 

    #get infile schema version
    current_ver = get_ver(conn);
    print("Current schema version: {}\n".format( current_ver));

    #if not latest roll forward
    if current_ver < latest_ver:      
        print("Bringing schema to version: {}\n".format (latest_ver));
        for migration_ver, sql in sql_stmt:
            if current_ver < migration_ver:
                conn.execute(sql);
        conn.execute("UPDATE __ver set date='" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "', ver='" + latest_ver + "'")

    conn.commit()
    conn.close()

def table_exists(conn :sqlite3.Connection, table_name :String):
    result = False;
    c = conn.cursor()
    #get the count of tables with the name
    c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name + "' ")
    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : 
        result = True;
    c.close();
    return result;

def get_ver(conn :sqlite3.Connection):
    result = '0.0.0';
    c = conn.cursor()
    #get the count of tables with the name
    c.execute(" SELECT ver FROM __ver ")
    results = c.fetchall();
    if len(results) > 0:
        result = results[0][0];
    c.close();
    return result;

def sql_gen_create_Domain():
    lst = list();
    lst.append(
     ('1.0.0', 
                ''' CREATE TABLE 'Domain' (
	            'domian'	TEXT,
	            'description'	TEXT,
	            PRIMARY KEY('domian')
                );'''
            ));
    lst.append(
            ('2.0.0',
                ''' INSERT INTO Domain Values('Person', 'Domain for people');''' 
            ));
    return lst;

def sql_gen_create_Subject():
    lst = list();
    lst.append(
      ('1.0.0', ''' CREATE TABLE 'Subject' (
	    'subject_id'	TEXT,
	    'default_synonym_id'	INTEGER NOT NULL,
	    'default_synonym'	TEXT NOT NULL,
	    'domain'	TEXT NOT NULL,
	    PRIMARY KEY('subject_id')
        ) WITHOUT ROWID;'''));
    return lst;

def sql_gen_create_Occurance():
    lst = list();
    lst.append( ('1.0.0', ''' CREATE TABLE 'Occurance' (
        'year'	INTEGER,
        'month'	INTEGER,
        'day'	INTEGER,
        'hour'	INTEGER,
        'minute'	INTEGER,
        'second'	INTEGER,
        'event_subject_id'	TEXT NOT NULL,
        'event_subject_default_name'	TEXT NOT NULL,
        'event_verb'	TEXT NOT NULL,
        'event_default_domain'	TEXT NOT NULL,
        'confidence'	REAL,
        'last_modified_timestamp'	TEXT,
        'last_modified_by_upn'	TEXT,
        PRIMARY KEY('event_subject_id','event_verb','year','month','day','hour','minute','second')
        ) WITHOUT ROWID;'''));
    return lst;

create_latest()

