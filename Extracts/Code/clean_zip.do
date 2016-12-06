* North Carolina
replace zip = "28719" if rpt_rc_num==264757|rpt_rc_num==106559
replace zip = "27104" if hosp_name=="OLD VINEYARD" & substr(zip,1,5)=="27004"
replace zip = "27055" if hosp_name=="CAH #10 - YADKINVILLE" & zip=="27065"
replace zip = "27514" if hosp_name=="UNIVERSITY OF NORTH CAROLINA HOSP." & zip=="27511"
replace zip = "27962" if rpt_rc_num==20009|rpt_rc_num==20012
replace zip = "28472" if rpt_rc_num==19807|rpt_rc_num==53052
replace zip = "28792" if hosp_name=="PARK RIDGE HOSPITAL" & zip=="28732"
replace zip = "28906" if hosp_name=="MURPHY MEDICAL CENTER" & substr(zip,1,5)=="28904"
replace zip = "28712" if city=="BREVARD" & substr(zip,1,5)=="29712"
replace zip = "28204" if hosp_name=="PRESBYTERIAN HOSPITAL" & substr(zip,1,5)=="33549"
replace zip = "28204" if hosp_name=="PRESBYTERIAN SPECIALTY HOSPITAL" & zip=="34425"
replace zip = "27103" if substr(hosp_name,1,4)=="AMOS" & (zip=="37013"|zip=="37103")
replace zip = "28792" if hosp_name=="PARK RIDGE HOSPITAL" & zip=="38732"

* FINAL TOUCHES
gen zip3 = substr(strltrim(zip),1,3)
gen zip5 = substr(strltrim(zip),1,5)

label var zip3 "ZIP CODE - 3 DIGIT"
label var zip5 "ZIP CODE - 5 DIGIT"


