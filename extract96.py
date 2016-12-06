import hcris

mypath = "C:/Users/Bryan/Dropbox (MIT)/Research/HCRIS/"

mydb = hcris.createlink(1996)
mydb.connect()


#mydb.export(mypath + "Variable Selections/Baseline",
#            mypath + "Extracts/baseline_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht S-2",
#            mypath + "Extracts/S2_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht S-3",
#            mypath + "Extracts/S3_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht A",
#            mypath + "Extracts/A_96.csv")
#            
#mydb.export(mypath + "Variable Selections/Wksht A-7",
#            mypath + "Extracts/A7_96.csv")
#   
#mydb.export(mypath + "Variable Selections/Wksht B-1",
#            mypath + "Extracts/B1_96.csv")
#   
#mydb.export(mypath + "Variable Selections/Wksht C",
#            mypath + "Extracts/C_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht E",
#            mypath + "Extracts/E_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht G",
#            mypath + "Extracts/G_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht G-1",
#            mypath + "Extracts/G1_96.csv")
#
#mydb.export(mypath + "Variable Selections/Wksht G-3",
#            mypath + "Extracts/G3_96.csv")
#

mydb.close()