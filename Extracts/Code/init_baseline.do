cap program drop cleandata
program define cleandata

do "Code/clean_date.do"

* label the variables
label var prvdr_ctrl_type_cd "HOSPITAL TYPE"
label var prvdr_num "CMS ID NUMBER"
label var fy_bgn_dt "FISCAL YEAR, START DATE"
label var fy_end_dt "FISCAL YEAR, END DATE"

label define cntrltype 1 "Nonprofit, Church" ///
					   2 "Nonprofit, Other" ///
					   3 "Proprietary, Individual" ///
					   4 "Proprietary, Corporation" ///
					   5 "Proprietary, Partnership" ///
					   6 "Proprietary, Other" ///
					   7 "Government, Federal" ///
					   8 "Government, City-County" ///
					   9 "Government, County" ///
					   10 "Government, State" ///
					   11 "Government, Hospital District" ///
					   12 "Government, City" ///
					   13 "Government, Other"
					   
label values prvdr_ctrl_type_cd cntrltype

label var year "YEAR"

end




* import baseline_96.csv
import delimited "baseline_96.csv", delimiter(comma) clear

cleandata

save "Stata/baseline_96.dta", replace




* import baseline_10.csv
import delimited "baseline_10.csv", delimiter(comma) clear

cleandata

* save the file
save "Stata/baseline_10.dta", replace
