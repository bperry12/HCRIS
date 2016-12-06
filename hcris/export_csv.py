import csv

def export_csv(varpath,outfile,ver,c):
    # open extract variables list
    if ver==1996:
        exVarsRpt = importCSVtoList(varpath + '/1996/extractVariablesRpt.csv')
        exVarsAlpha = importCSVtoList(varpath + '/1996/extractVariablesAlpha.csv')
        exVarsNmrc = importCSVtoList(varpath + '/1996/extractVariablesNmrc.csv')
    elif ver==2010:
        exVarsRpt = importCSVtoList(varpath + '/2010/extractVariablesRpt.csv')
        exVarsAlpha = importCSVtoList(varpath + '/2010/extractVariablesAlpha.csv')
        exVarsNmrc = importCSVtoList(varpath + '/2010/extractVariablesNmrc.csv')
        
    hasAlpha = len(exVarsAlpha)>1
    hasNmrc = len(exVarsNmrc)>1
    
    # write strings needed for queries
    varsStrRpt = writeVarsStr(exVarsRpt,True,False)    
    varsStrAlpha = writeVarsStr(exVarsAlpha,False,hasAlpha)
    varsStrNmrc = writeVarsStr(exVarsNmrc,False,hasNmrc)
    varsStrAlpha2 = writeVarsStr2(exVarsAlpha,hasAlpha)
    varsStrNmrc2 = writeVarsStr2(exVarsNmrc,hasNmrc)
    whereStrAlpha = writeWhereStr(exVarsAlpha,hasAlpha,ver)
    whereStrNmrc = writeWhereStr(exVarsNmrc,hasNmrc,ver)
    transStrAlpha = writeTransStr(exVarsAlpha,"alpha",hasAlpha)
    transStrNmrc = writeTransStr(exVarsNmrc,"nmrc",hasNmrc)

    # create temporary tables
    if hasAlpha:
        createExtractTable(c,exVarsAlpha,whereStrAlpha,transStrAlpha,"alpha")
    if hasNmrc:
        createExtractTable(c,exVarsNmrc,whereStrNmrc,transStrNmrc,"nmrc")
    
    # merge and export
    exportFile(c,outfile,varsStrRpt,varsStrAlpha,varsStrNmrc,varsStrAlpha2,varsStrNmrc2,hasAlpha,hasNmrc)
    
    # drop temporary tables
    if hasAlpha:
        droptemps(c,"alpha")
    if hasNmrc:
        droptemps(c,"nmrc")

def writeVarsStr(exvars,rptind,has):
    if rptind:
        varsStr = exvars[0][1]    
        for row in exvars[1:]:
            if row[0]=="X":
                varsStr += ", " + row[1]
    elif has:        
        varsStr = exvars[1][3]    
        for row in exvars[2:]:
            varsStr += ", " + row[3]
    else:
        varsStr = ""
    return varsStr
    
def writeVarsStr2(exvars,has):
    if has:
        varsStr = """IFNULL(""" + exvars[1][3] + """,".")"""    
        for row in exvars[2:]:
            varsStr += """, IFNULL(""" + row[3] + """,".")"""    
    else:
        varsStr = ""
    return varsStr

def writeWhereStr(exvars,has,ver):
    if ver==1996:
        fill=4
    elif ver==2010:
        fill=5
        
    if has:
        whereStr = "((WKSHT_CD=" + '\"' + exvars[1][0] + '\"' + " AND LINE_NUM=" + '\"' + str(exvars[1][1]).zfill(5) + '\"' + " AND CLMN_NUM=" + '\"' + str(exvars[1][2]).zfill(fill) + '\"' + ")"
        for row in exvars[2:]:
            whereStr += " OR (WKSHT_CD=" + '\"' + row[0] + '\"' + " AND LINE_NUM=" + '\"' + str(row[1]).zfill(5) + '\"' + " AND CLMN_NUM=" + '\"' + str(row[2]).zfill(fill) + '\"' + ")"
        whereStr += ")"    
    else:
        whereStr = "" 
    return whereStr

def writeTransStr(exvars,typ,has):
    if has:
        if typ=="alpha":
            transStr = ", MAX(CASE WHEN varname=" + '\"' + exvars[1][3] + '\"' + " THEN alphnmrc_itm_txt END) " + exvars[1][3]
            for row in exvars[2:]:
                transStr += ", MAX(CASE WHEN varname=" + '\"' + row[3] + '\"' + " THEN alphnmrc_itm_txt END) " + row[3]
        elif typ=="nmrc":
            transStr = ", MAX(CASE WHEN varname=" + '\"' + exvars[1][3] + '\"' + " THEN itm_val_num END) " + exvars[1][3]
            for row in exvars[2:]:
                transStr += ", MAX(CASE WHEN varname=" + '\"' + row[3] + '\"' + " THEN itm_val_num END) " + row[3]
    else:
        transStr = ""
    return transStr

def createExtractTable(c,exvars,whereStr,transStr,typ):
    if typ=="alpha":
        c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_""" + typ + """
                  SELECT RPT_RPT_RC_NUM, WKSHT_CD, LINE_NUM, CLMN_NUM, IFNULL(REPLACE(ALPHNMRC_ITM_TXT,'\r',""),".") AS ALPHNMRC_ITM_TXT
                  FROM """ + typ + """ WHERE """ + 
                  whereStr)
    elif typ=="nmrc":
        c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_""" + typ + """
                  SELECT RPT_RPT_RC_NUM, WKSHT_CD, LINE_NUM, CLMN_NUM, IFNULL(REPLACE(ITM_VAL_NUM,'\r',""),".") AS ITM_VAL_NUM
                  FROM """ + typ + """ WHERE """ + 
                  whereStr)
    c.execute("ALTER TABLE temp_" + typ + " ADD COLUMN varname varchar(32)")
    for row in exvars[1:]:
        c.execute("""UPDATE temp_""" + typ + """ SET varname=""" + '\"' + row[3] + '\"' + """
                  WHERE (WKSHT_CD=""" + '\"' + row[0] + '\"' + """
                  AND LINE_NUM=""" + row[1] + """
                  AND CLMN_NUM=""" + row[2] + ")")
    
    c.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp_""" + typ + """_trans 
              SELECT rpt_rpt_rc_num""" + transStr + """
              FROM temp_""" + typ + """
              GROUP BY rpt_rpt_rc_num""")
    
    for row in exvars[1:]:
        c.execute("""UPDATE temp_""" + typ + """_trans 
                  SET """ + row[3] + """=IFNULL(""" + row[3] + """,".")""")

def exportFile(c,outfile,varsStrRpt,varsStrAlpha,varsStrNmrc,varsStrAlpha2,varsStrNmrc2,hasAlpha,hasNmrc):
    if hasAlpha and hasNmrc:
        c.execute("""SELECT \'""" + varsStrRpt.replace(", ","""\', \'""") + """\', \'""" + varsStrAlpha.replace(", ","""\', \'""") + """\', \'""" + varsStrNmrc.replace(", ","""\', \'""") + """\' 
                   UNION
                  (SELECT """ + varsStrRpt + ', ' + varsStrAlpha2 + ', ' + varsStrNmrc2 + """
                   FROM rpt r
                   LEFT JOIN temp_alpha_trans a
                   ON r.rpt_rc_num=a.rpt_rpt_rc_num
                   LEFT JOIN temp_nmrc_trans n
                   ON r.rpt_rc_num=n.rpt_rpt_rc_num
                   GROUP BY r.rpt_rc_num
                   ORDER BY r.prvdr_num, r.fy_end_dt
                   INTO OUTFILE '""" + outfile + """'
                   FIELDS ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '"' 
                   LINES TERMINATED BY '""" + "\\" + """r""" + "\\" + """n')""")
    elif hasAlpha and not hasNmrc:
        c.execute("""SELECT \'""" + varsStrRpt.replace(", ","""\', \'""") + """\', \'""" + varsStrAlpha.replace(", ","""\', \'""") + """\' 
                   UNION
                  (SELECT """ + varsStrRpt + ', ' + varsStrAlpha2 + """
                   FROM rpt r
                   LEFT JOIN temp_alpha_trans a
                   ON r.rpt_rc_num=a.rpt_rpt_rc_num
                   GROUP BY r.rpt_rc_num
                   ORDER BY r.prvdr_num, r.fy_end_dt
                   INTO OUTFILE '""" + outfile + """'
                   FIELDS ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '"' 
                   LINES TERMINATED BY '""" + "\\" + """r""" + "\\" + """n')""")
    elif not hasAlpha and hasNmrc:
        c.execute("""SELECT \'""" + varsStrRpt.replace(", ","""\', \'""") + """\', \'""" + varsStrNmrc.replace(", ","""\', \'""") + """\' 
                   UNION
                  (SELECT """ + varsStrRpt + ', ' + varsStrNmrc2 + """
                   FROM rpt r
                   LEFT JOIN temp_nmrc_trans n
                   ON r.rpt_rc_num=n.rpt_rpt_rc_num
                   GROUP BY r.rpt_rc_num
                   ORDER BY r.prvdr_num, r.fy_end_dt
                   INTO OUTFILE '""" + outfile + """'
                   FIELDS ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '"' 
                   LINES TERMINATED BY '""" + "\\" + """r""" + "\\" + """n')""")
    elif not hasAlpha and not hasNmrc:
        c.execute("""SELECT \'""" + varsStrRpt.replace(", ","""\', \'""") + """\' 
                   UNION
                  (SELECT """ + varsStrRpt + """
                   FROM rpt r
                   GROUP BY r.rpt_rc_num
                   ORDER BY r.prvdr_num, r.fy_end_dt
                   INTO OUTFILE '""" + outfile + """'
                   FIELDS ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '"' 
                   LINES TERMINATED BY '""" + "\\" + """r""" + "\\" + """n')""")

def importCSVtoList(filename):
    with open(filename,'rb') as csvfile:
        outlist = list(csv.reader(csvfile))
    return outlist
    
def droptemps(c,typ):
    c.execute("""DROP TABLE temp_""" + typ)    
    c.execute("""DROP TABLE temp_""" + typ + """_trans""")