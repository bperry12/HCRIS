# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 09:09:49 2015

@author: Bryan
"""

def createlink(version,connection=None):
    return HCRISDataBase(version,connection)


class HCRISDataBase:
    
    def __init__(self,version,connection=None):
        self.version = version
        if self.version==1996:
            self.name = "hcris_db_96"
        elif self.version==2010:
            self.name = "hcris_db_10"
        else:
            ### ERROR ###
            pass
        self.conn = connection        
        if connection is not None:
            self.cursor = self.conn.cursor()


    def connect(self,hostname="localhost",username="root"):
        from mysql import connector
        mysql_pwd = input("Input database password: ")
        self.conn = connector.connect(host=hostname,user=username,passwd=mysql_pwd)
        self.cursor = self.conn.cursor()
    

    def create(self):
        import os
        from hcris.exec_sql import exec_sql_file as esf
        if self.version==1996:
            sql_file = os.path.dirname(os.path.realpath(__file__)) + "\\createHCRISdb96.sql"
            esf(self.cursor,sql_file)
        elif self.version==2010:
            sql_file = os.path.dirname(os.path.realpath(__file__)) + "\\createHCRISdb10.sql"
            esf(self.cursor,sql_file)        
        else:
            ### ERROR ###
            pass


    def load(self,beg_yr,end_yr,datapath):
        if self.conn is None:
            ### ERRROR ###
            pass

        from hcris.load import load_yr
        
        datapath = replaceforwardslash(datapath)
        
        for yr in xrange(beg_yr,end_yr+1):
            print yr
            if yr >= 2010 and self.version==2010:
                self.cursor.execute("USE hcris_db_10")
                load_yr(yr,datapath,self.version,self.cursor)
                self.conn.commit()        
            elif yr<=2010 and self.version==1996:
                self.cursor.execute("USE hcris_db_96")
                load_yr(yr,datapath,self.version,self.cursor)
                self.conn.commit()        
            else:
                ### ERROR ###
                pass
        
        
    def export(self,varpath,outfile):
        if self.conn is None:
            ### ERRROR ###
            pass

        import os
        from hcris.export_csv import export_csv
        
        varpath = replaceforwardslash(varpath)
        outfile = replaceforwardslash(outfile)
        
        os.remove(outfile) if os.path.exists(outfile) else None

        # extract data
        if self.version==1996:
            self.cursor.execute("USE hcris_db_96")
        elif self.version==2010:
            self.cursor.execute("USE hcris_db_10")
        else:
            ### ERROR ###
            pass
            
        export_csv(varpath,outfile,self.version,self.cursor)


    def close(self):
        if self.conn is None:
            ### ERRROR ###
            pass
        self.conn.close()    


def replaceforwardslash(string):
    return string.replace("\\","/").replace("\t","/t").replace("\b","/b").replace("\n","/n").replace("\r","/r").replace("\v","/v").replace("\a","/a")