import hcris

mypath = "C:/Users/Bryan/Dropbox (MIT)/Research/HCRIS/"

mydb = hcris.createlink(1996)
mydb.connect()

keepgoing = input("""You are about to erase the 1996 database and create it 
                    from scratch. This can take a very long time. Are you 
                    sure you want to continue? (Y/N)
                    """)

if keepgoing=="Y" or keepgoing=="y":
    mydb.create()
    mydb.load(1995,2010,mypath + "Raw Data")

mydb.close()