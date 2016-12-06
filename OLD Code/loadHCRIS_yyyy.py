# -*- coding: utf-8 -*-
"""
.. module:: loadHCRIS_yyyy
    :platform: Windows
    :synopsis: Load HCRIS data into existing MySQL database.
.. moduleauthor:: Bryan Perry <perryb@mit.edu>

Created on Fri Dec 12 16:52:31 2014


This module loads data from Medicare Cost Reports (HCRIS) into a MySQL database.


HEADING
======================

Some stuff...

.. function:: loadHCRIS_yyyy(year, version, cursor)

"""

import os


# load
def loadHCRIS_yyyy(year,version,cursor):
    """
    Import a year of Medicare cost report (HCRIS) data into an existing MySQL 
    database.
    
    Parameters
    ----------------------------
    year : int
        The year of data to import. Must be greater than or equal to 1995.
    version : int 
        The version of the cost report used. Must be equal to 1996 or 2010.
    cursor : mysql.connector.cursor
        Cursor linked to the MySQL database to have data loaded.
     
    """
    
    # load stuff     
    mypath = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
    mypath = mypath.replace("\\","/")
    if version==2010:
        mypath = mypath + "/HCRIS_" + str(year) + "/hosp10_" + str(year) + "_"
    elif version==1996:
        mypath = mypath + "/HCRIS_" + str(year) + "/hosp_" + str(year) + "_"
        
    cursor.execute("""LOAD DATA INFILE '""" + mypath + """RPT.csv' 
                   INTO TABLE rpt 
                   FIELDS TERMINATED BY ',' 
                   LINES TERMINATED BY '""" + "\\" + """n' 
                   (RPT_RC_NUM,   PRVDR_CTRL_TYPE_CD, PRVDR_NUM, @NPI,RPT_STUS_CD, 
                    @FY_BGN_DT,   @FY_END_DT,         @PROC_DT,  INITL_RPT_SW, 
                    LAST_RPT_SW,  TRNSMTL_NUM,        FI_NUM,    ADR_VNDR_CD,  
                    @FI_CREAT_DT, UTIL_CD,	        @NPR_DT,   @SPEC_IND, 
                    @FI_RCPT_DT) 
                   SET NPI = IF(@NPI='',NULL,@NPI), 
                   FY_BGN_DT = STR_TO_DATE(@FY_BGN_DT, '%m/%d/%Y'), 
                   FY_END_DT = STR_TO_DATE(@FY_END_DT, '%m/%d/%Y'), 
                   PROC_DT = STR_TO_DATE(@PROC_DT, '%m/%d/%Y'), 
                   FI_CREAT_DT = STR_TO_DATE(@FI_CREAT_DT, '%m/%d/%Y'), 
                   NPR_DT = IF(@NPR_DT='',NULL,STR_TO_DATE(@NPR_DT, '%m/%d/%Y')), 
                   SPEC_IND = IF(@SPEC_IND='',NULL,@SPEC_IND), 
                   FI_RCPT_DT = STR_TO_DATE(@FI_RCPT_DT, '%m/%d/%Y')""")
    
    cursor.execute("""LOAD DATA INFILE '""" + mypath + """ALPHA.csv' 
                   INTO TABLE alpha 
                   FIELDS TERMINATED BY ',' 
                   LINES TERMINATED BY '""" + "\\" + """n'
                   (RPT_RPT_RC_NUM, WKSHT_CD, LINE_NUM, CLMN_NUM, ALPHNMRC_ITM_TXT)""")
    
    cursor.execute("""LOAD DATA INFILE '""" + mypath + """NMRC.csv' 
                   INTO TABLE nmrc 
                   FIELDS TERMINATED BY ',' 
                   LINES TERMINATED BY '""" + "\\" + """n'
                   (RPT_RPT_RC_NUM,   WKSHT_CD,  LINE_NUM, CLMN_NUM, ITM_VAL_NUM)""")
