# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 13:32:19 2014

@author: Bryan Perry
"""

import mysql.connector as conn
import loadHCRIS_yyyy as load
import exec_sql_file as esf
import getExtract as ge
import os

"""
TEST CODE: 
    beg_yr = 1995
    end_yr = 2013
    outfile96 = "HCRISextract96.csv"
    outfile10 = "HCRISextract10.csv"
    loadHCRIS(outfile96,outfile10)
"""

def loadHCRIS(outfile96,outfile10,beg_yr=[],end_yr=[],createdbs=False,importdata=False,exportextract=True,hostname="localhost",username="root"): 
    if createdbs and exportextract and not importdata:
        raise Exception("Cannot export data from a new database without importing data.")

    # connect to MySQL Server1
    mysql_pwd = input("Input database password: ")
    db = conn.connect(host=hostname,user=username,passwd=mysql_pwd)
    c = db.cursor()
    
    # create database
    if createdbs:
        esf.exec_sql_file(c,"createHCRISdb96.sql")
        esf.exec_sql_file(c,"createHCRISdb10.sql")
    
    # load raw data into HCRIS database
    if importdata:
        for yr in xrange(beg_yr,end_yr+1):
            print yr
            if yr > 2010:
                ver = 2010
                c.execute("USE hcris_db_10")
            elif yr == 2010:
                ver = 1996
                c.execute("USE hcris_db_96")
                load.loadHCRIS_yyyy(yr,ver,c)
                db.commit()
                ver = 2010
                c.execute("USE hcris_db_10")
            else:
                ver = 1996
                c.execute("USE hcris_db_96")
            load.loadHCRIS_yyyy(yr,ver,c)
            db.commit()
    
    # extract required data ###
    if exportextract:
        # remove output files if it exists 
        os.remove(outfile96) if os.path.exists(outfile96) else None
        os.remove(outfile10) if os.path.exists(outfile10) else None
        # extract data
        c.execute("USE hcris_db_96")
        ge.getExtract(outfile96,c)
        c.execute("USE hcris_db_10")
        ge.getExtract(outfile10,c)
    
    # close connection to MySQL database
    db.close()
    