# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 17:03:23 2014

"""

import re

def exec_sql_file(cursor, sql_file):
    # reset statement    
    statement = ""

    # execute each SQL statement
    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print "[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

            statement = ""
            
            
