cap program drop cleandata
program define cleandata

* label the variables
label var city "CITY"
label var state "STATE"
label var zip "ZIP CODE"
label var county "COUNTY"
label var hosp_name "HOSPITAL NAME"

* clean data
do "Code/clean_zip.do"
do "Code/clean_state.do"
do "Code/clean_county.do"

end



import delimited "S2_96.csv", delimiter(comma) clear

cleandata

save "Stata/S2_96.dta", replace


import delimited "S2_10.csv", delimiter(comma) clear

cleandata

save "Stata/S2_10.dta", replace

