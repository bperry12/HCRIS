* General Adjustments
qui replace county = subinstr(county,"  "," ",.)
qui replace county = subinstr(county," COUNTY","",.)
qui replace county = subinstr(county," COUNTRY","",.)
qui replace county = subinstr(county," BOROUGH","",.)
qui replace county = subinstr(county," BURROUGH","",.)
qui replace county = subinstr(county," PARISH","",.)
qui replace county = subinstr(county," PARRISH","",.)
qui replace county = subinstr(county,"ST ","ST. ",.)
qui replace county = subinstr(county,"SAINT ","ST. ",.)
qui replace county = subinstr(county,"MUNICIPALITY OF ","",.)

qui replace county = "." if county=="NONE"
qui replace county = "." if county=="N/A"
qui replace county = "." if county=="NOT APPLICABLE"

qui replace county = "." if county=="US"
qui replace county = "." if county=="U S"
qui replace county = "." if county=="USA"
qui replace county = "." if county=="U.S.A"
qui replace county = "." if county=="U S A"
qui replace county = "." if county=="U.S.A."
qui replace county = "." if county=="UNITED STATES"
qui replace county = "." if county=="UNITED STATE OF AMERICA"
qui replace county = "." if county=="UNITED STATES OF AMERICA"

qui replace county = subinstr(county,"ST.LOUIS","ST. LOUIS",.)

* State Adjustments
qui replace state = "AK" if state=="AD"
qui replace state = "AL" if city=="MUSCLE SHOALS" & state=="TN"
qui replace state = "AL" if county=="SUMTER" & state=="MS"
qui replace state = "AL" if state=="ALABAMA"
qui replace state = "AR" if state=="ARKANSAS"
qui replace state = "AR" if county=="GRAIGHEAD" & state=="AK"
qui replace state = "AZ" if city=="GLENDALE" & state=="MS"
qui replace state = "AZ" if state=="AX"|state=="ARIZONA"
qui replace state = "CA" if city=="ROSEVEILLE" & state=="GA"
qui replace state = "CA" if state=="CALIFORNIA"
qui replace state = "CO" if city=="ENGLEWOOD" & state=="CA"
qui replace state = "CO" if state=="COLORADO"
qui replace state = "CT" if state=="CONNECTICUT"
qui replace state = "FL" if city=="MIAMI" & state=="CA"
qui replace state = "FL" if city=="TAMPA" & state=="CA"
qui replace state = "GA" if county=="MCDUFFIE" & state=="AL"
qui replace state = "GA" if state=="GEORGIA"|state=="GE"|state=="GS"
qui replace state = "IA" if city=="IOWA FALLS" & state=="CA"
qui replace state = "IA" if city=="ONAWA" & state=="NE"
qui replace state = "IA" if state=="IO"
qui replace state = "ID" if county=="JEROME" & state=="WA"
qui replace state = "ID" if county=="TETON" & state=="UT"
qui replace state = "IL" if state=="ILLINOIS"|state=="ILLINIOS"
qui replace state = "IN" if city=="PORTLAND" & state=="NE"
qui replace state = "KS" if city=="WICHITA" & state=="GA"
qui replace state = "KS" if county=="KEARNY" & state=="KY"
qui replace state = "KS" if state=="KANSAS"|state=="KA"
qui replace state = "KY" if state=="KE"
qui replace state = "LA" if city=="LAFAYETTE" & zip3=="705" & state=="MO"
qui replace state = "LA" if state=="LOUISIANA"|state=="LO"
qui replace state = "MD" if city=="ROCKVILLE" & state=="DE"
qui replace state = "MI" if state=="MICHIGAN"
qui replace state = "MN" if city=="BEMIDJI" & state=="NC"
qui replace state = "MO" if city=="WENTZVILLE" & state=="FL"
qui replace state = "MO" if county=="BOONE" & state=="MT"
qui replace state = "MS" if state=="MISSISSIPPI"
qui replace state = "MT" if state=="MONTANA"
qui replace state = "NC" if state=="EE"
qui replace state = "NC" if state=="NORTH CAROLINA"
qui replace state = "NE" if county=="HARLAN" & state=="KS"
qui replace state = "NJ" if city=="NEWARK" & county=="ESSEX" & state=="NY"
qui replace state = "NM" if city=="SANTA FE" & state=="MN"
qui replace state = "NM" if state=="NEW MEXICO"
qui replace state = "NY" if state=="NEW YORK"
qui replace state = "OH" if county=="CUYAHOGA" & state=="PA"
qui replace state = "OK" if state=="OKLAHOMA"
qui replace state = "PA" if state=="PANNSYLVANIA"
qui replace state = "PR" if county=="PUERTO RICO"
qui replace state = "PR" if state=="PUERTO RICO"|state=="PURETO RICO"|state=="P."
qui replace state = "SC" if city=="GAFFNEY" & state=="NC"
qui replace state = "SC" if county=="HORRY" & state=="NC"
qui replace state = "SC" if state=="SO"
qui replace state = "SD" if city=="VERMILLION" & county=="CLAY" & state=="MN"
qui replace state = "TN" if state=="TNNNESSEE"|state=="TENNESSEE"|state=="TE"
qui replace state = "TX" if city=="CENTER POINT" & state=="MO"
qui replace state = "TX" if city=="HOUSTON" & state=="CA"
qui replace state = "TX" if city=="SAN ANTONIO" & state=="AL"
qui replace state = "TX" if county=="DALLAS" & state=="CA"
qui replace state = "TX" if state=="TEXAS"|(state=="TE"&county!="COFFEE-FRANKLIN")
qui replace state = "UT" if state=="UTAH"
qui replace state = "VA" if state=="50"
qui replace state = "VI" if state=="US"
qui replace state = "WI" if city=="NEW RICHMOND" & state=="CA"
qui replace state = "WI" if state=="WISCONSIN"|state=="WS"

* ZIP Code State Check
qui merge m:1 zip3 using "Stata/zip3_to_state.dta"
replace st3 = "CA" if zip5=="99410"
drop if _merge==2
drop _merge
replace state = st3 if state=="."
replace state = st3 if state=="AL" & st3=="AK"
replace state = st3 if state=="AR" & st3=="AZ"
replace state = st3 if state=="MA" & st3=="MD"
replace state = st3 if state=="MI" & st3=="MN"
replace state = st3 if state=="MI" & st3=="MO"
replace state = st3 if state=="MI" & st3=="MS"
replace state = st3 if state=="MO" & st3=="MT"
replace state = st3 if state=="NE" & st3=="NJ"
replace state = st3 if state=="NE" & st3=="NV"
replace state = st3 if state=="VI" & st3=="VA"
replace state = st3 if state=="TN" & st3=="TX"
replace state = st3 if state=="AK" & st3=="AR"

drop st3
