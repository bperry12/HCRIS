# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 17:28:48 2014

@author: Bryan
"""
import os
import csv

def getExtract(outfilename,c):
    # open extract variables list
    exVarsRpt = importCSVtoList('extractVariablesRpt.csv')
    exVarsAlpha = importCSVtoList('extractVariablesAlpha.csv')
    exVarsNmrc = importCSVtoList('extractVariablesNmrc.csv')
    
    # write strings needed for queries
    varsStrRpt = writeVarsStr(exVarsRpt,1,True)    
    varsStrAlpha = writeVarsStr(exVarsAlpha,3,False)
    varsStrNmrc = writeVarsStr(exVarsNmrc,3,False)
    whereStrAlpha = writeWhereStr(exVarsAlpha)
    whereStrNmrc = writeWhereStr(exVarsNmrc)
    transStrAlpha = writeTransStr(exVarsAlpha,"alpha")
    transStrNmrc = writeTransStr(exVarsNmrc,"nmrc")

    # create temporary tables
    createExtractTable(c,exVarsAlpha,whereStrAlpha,transStrAlpha,"alpha")
    createExtractTable(c,exVarsNmrc,whereStrNmrc,transStrNmrc,"nmrc")

    # merge and export
    outfile = os.getcwd()
    outfile = outfile.replace("\\","/")
    outfile = outfile + "/" + outfilename
    exportFile(c,outfile,varsStrRpt,varsStrAlpha,varsStrNmrc)

def writeVarsStr(exvars,ind,rptind):
    varsStr = exvars[0][ind]    
    for row in exvars[1:]:
        if (rptind and (row[0]=="X")) or not rptind:
            varsStr += ", " + row[ind]
    return varsStr

def writeWhereStr(exvars):
    whereStr = "((WKSHT_CD=" + '\"' + exvars[0][0] + '\"' + " AND LINE_NUM=" + exvars[0][1] + " AND CLMN_NUM=" + exvars[0][2] + ")"
    for row in exvars[1:]:
        whereStr += " OR (WKSHT_CD=" + '\"' + row[0] + '\"' + " AND LINE_NUM=" + row[1] + " AND CLMN_NUM=" + row[2] + ")"
    whereStr += ")"            
    return whereStr

def writeTransStr(exvars,typ):
    if typ=="alpha":
        transStr = "MAX(CASE WHEN varname=" + '\"' + exvars[0][3] + '\"' + " THEN alphnmrc_itm_txt END) " + exvars[0][3]
        for row in exvars[1:]:
            transStr += ", MAX(CASE WHEN varname=" + '\"' + row[3] + '\"' + " THEN alphnmrc_itm_txt END) " + row[3]
    elif typ=="nmrc":
        transStr = "MAX(CASE WHEN varname=" + '\"' + exvars[0][3] + '\"' + " THEN itm_val_num END) " + exvars[0][3]
        for row in exvars[1:]:
            transStr += ", MAX(CASE WHEN varname=" + '\"' + row[3] + '\"' + " THEN itm_val_num END) " + row[3]
    return transStr

def createExtractTable(c,exvars,whereStr,transStr,typ):
    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_""" + typ + """
              SELECT * 
              FROM """ + typ + """ WHERE """ + 
              whereStr)
    
    c.execute("ALTER TABLE temp_" + typ + " ADD COLUMN varname varchar(32)")
    
    for row in exvars:
        c.execute("""UPDATE temp_""" + typ + """ SET varname=""" + '\"' + row[3] + '\"' + """
                  WHERE (WKSHT_CD=""" + '\"' + row[0] + '\"' + """
                  AND LINE_NUM=""" + row[1] + """
                  AND CLMN_NUM=""" + row[2] + ")")
    
    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_""" + typ + """_trans 
              SELECT rpt_rpt_rc_num,""" + 
              transStr + """
              FROM temp_""" + type + """
              GROUP BY rpt_rpt_rc_num""")
    
def exportFile(c,outfile,varsStrRpt,varsStrAlpha,varsStrNmrc):
    c.execute("""SELECT \'""" + varsStrRpt.replace(", ","""\', \'""") + """\', \'""" + varsStrAlpha.replace(", ","""\', \'""") + """\', \'""" + varsStrNmrc.replace(", ","""\', \'""") + """\' 
               UNION
              (SELECT """ + varsStrRpt + ', ' + varsStrAlpha + ', ' + varsStrNmrc + """
               FROM rpt r
               LEFT JOIN temp_alpha_trans a
               ON r.rpt_rc_num=a.rpt_rpt_rc_num
               LEFT JOIN temp_nmrc_trans n
               ON r.rpt_rc_num=n.rpt_rpt_rc_num
               GROUP BY r.rpt_rc_num
               ORDER BY r.prvdr_num, r.fy_end_dt
               INTO OUTFILE '""" + outfile + """'
               FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
               LINES TERMINATED BY '""" + "\\" + """n')""")

def importCSVtoList(filename):
    with open(filename,'rb') as csvfile:
        outlist = list(csv.reader(csvfile))
    return outlist



#def getExtract(outfilename,c):
#    with open('extractVariablesRpt.csv','rb') as csvfile:
#        exVarsRpt = list(csv.reader(csvfile))
#    
#    with open('extractVariablesAlpha.csv','rb') as csvfile:
#        exVarsAlpha = list(csv.reader(csvfile))
#    
#    with open('extractVariablesNmrc.csv','rb') as csvfile:
#        exVarsNmrc = list(csv.reader(csvfile))
#
#
#    ....
#
#
#    varsStrRpt = exVarsRpt[0][1]
#    for row in exVarsRpt[1:]:
#        if row[0]=="X":
#            varsStrRpt = varsStrRpt + ", " + row[1]
#    
#    whereStrAlpha = "((WKSHT_CD=" + '\"' + exVarsAlpha[0][0] + '\"' + " AND LINE_NUM=" + exVarsAlpha[0][1] + " AND CLMN_NUM=" + exVarsAlpha[0][2] + ")"
#    transStrAlpha = "MAX(CASE WHEN varname=" + '\"' + exVarsAlpha[0][3] + '\"' + " THEN alphnmrc_itm_txt END) " + exVarsAlpha[0][3]
#    varsStrAlpha = exVarsAlpha[0][3]
#    for row in exVarsAlpha[1:]:
#        whereStrAlpha = whereStrAlpha + " OR (WKSHT_CD=" + '\"' + row[0] + '\"' + " AND LINE_NUM=" + row[1] + " AND CLMN_NUM=" + row[2] + ")"
#        transStrAlpha = transStrAlpha + ", MAX(CASE WHEN varname=" + '\"' + row[3] + '\"' + " THEN alphnmrc_itm_txt END) " + row[3]
#        varsStrAlpha = varsStrAlpha + ", " + row[3]
#    whereStrAlpha = whereStrAlpha + ")"        
#    
#    whereStrNmrc = "((WKSHT_CD=" + '\"' + exVarsNmrc[0][0] + '\"' + " AND LINE_NUM=" + exVarsNmrc[0][1] + " AND CLMN_NUM=" + exVarsNmrc[0][2] + ")"
#    transStrNmrc = "MAX(CASE WHEN varname=" + '\"' + exVarsNmrc[0][3] + '\"' + " THEN itm_val_num END) " + exVarsNmrc[0][3]
#    varsStrNmrc = exVarsNmrc[0][3]
#    for row in exVarsNmrc[1:]:
#        whereStrNmrc = whereStrNmrc + " OR (WKSHT_CD=" + '\"' + row[0] + '\"' + " AND LINE_NUM=" + row[1] + " AND CLMN_NUM=" + row[2] + ")"
#        transStrNmrc = transStrNmrc + ", MAX(CASE WHEN varname=" + '\"' + row[3] + '\"' + " THEN itm_val_num END) " + row[3]
#        varsStrNmrc = varsStrNmrc + ", " + row[3]
#    whereStrNmrc = whereStrNmrc + ")"        
#    # alpha table extract
#    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_alpha
#              SELECT * 
#              FROM alpha WHERE """ + 
#              whereStrAlpha)
#    
#    c.execute("ALTER TABLE temp_alpha ADD COLUMN varname varchar(32)")
#    
#    for row in exVarsAlpha:
#        c.execute("""UPDATE temp_alpha SET varname=""" + '\"' + row[3] + '\"' + """
#                  WHERE (WKSHT_CD=""" + '\"' + row[0] + '\"' + """
#                  AND LINE_NUM=""" + row[1] + """
#                  AND CLMN_NUM=""" + row[2] + ")")
#    
#    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_alpha_trans 
#              SELECT rpt_rpt_rc_num,""" + 
#              transStrAlpha + """
#              FROM temp_alpha
#              GROUP BY rpt_rpt_rc_num""")
#    
#    # nmrc table extract
#    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_nmrc
#              SELECT * 
#              FROM nmrc WHERE """ + 
#              whereStrNmrc)
#    
#    c.execute("ALTER TABLE temp_nmrc ADD COLUMN varname varchar(32)")
#    
#    for row in exVarsNmrc:
#        c.execute("""UPDATE temp_nmrc SET varname=""" + '\"' + row[3] + '\"' + """
#                  WHERE (WKSHT_CD=""" + '\"' + row[0] + '\"' + """
#                  AND LINE_NUM=""" + row[1] + """
#                  AND CLMN_NUM=""" + row[2] + ")")
#    
#    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_nmrc_trans 
#              SELECT rpt_rpt_rc_num,""" + 
#              transStrNmrc + """
#              FROM temp_nmrc
#              GROUP BY rpt_rpt_rc_num""")
#    c.execute("""SELECT \'""" + varsStrRpt.replace(", ","""\', \'""") + """\', \'""" + varsStrAlpha.replace(", ","""\', \'""") + """\', \'""" + varsStrNmrc.replace(", ","""\', \'""") + """\' 
#               UNION
#              (SELECT """ + varsStrRpt + ', ' + varsStrAlpha + ', ' + varsStrNmrc + """
#               FROM rpt r
#               LEFT JOIN temp_alpha_trans a
#               ON r.rpt_rc_num=a.rpt_rpt_rc_num
#               LEFT JOIN temp_nmrc_trans n
#               ON r.rpt_rc_num=n.rpt_rpt_rc_num
#               GROUP BY r.rpt_rc_num
#               ORDER BY r.prvdr_num, r.fy_end_dt
#               INTO OUTFILE '""" + outfile + """'
#               FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
#               LINES TERMINATED BY '""" + "\\" + """n')""")