cap program drop cleandata
program define cleandata

* label the variables
label var bldg_sqft_tot "BUILDING SQFT, TOTAL"
label var bldg_sqft_raddiag "BUILDING SQFT, DIAGNOSTIC RADIOLOGY"
label var bldg_sqft_radther "BUILDING SQFT, THERAPEUTIC RADIOLOGY"
label var bldg_sqft_radio "BUILDING SQFT, RADIOISOTOPE"

label var moveq_dolval_tot "MOVABLE EQUIPMENT VALUE, TOTAL"
label var moveq_dolval_raddiag "MOVABLE EQUIPMENT VALUE, DIAGNOSTIC RADIOLOGY"
label var moveq_dolval_radther "MOVABLE EQUIPMENT VALUE, THERAPEUTIC RADIOLOGY"
label var moveq_dolval_radio "MOVABLE EQUIPMENT VALUE, RADIOISOTOPE"

order bldg_sqft_raddiag, after(bldg_sqft_tot)
order moveq_dolval_raddiag, after(moveq_dolval_tot)

end



* import B1_96.csv
import delimited "B1_96.csv", delimiter(comma) clear

egen bldg_sqft_tot = rowtotal(bldg_sqft_old_tot bldg_sqft_new_tot), missing
egen bldg_sqft_raddiag = rowtotal(bldg_sqft_old_raddiag bldg_sqft_new_raddiag), missing
egen bldg_sqft_radther = rowtotal(bldg_sqft_old_radther bldg_sqft_new_radther), missing
egen bldg_sqft_radio = rowtotal(bldg_sqft_old_radio bldg_sqft_new_radio), missing

egen moveq_dolval_tot = rowtotal(moveq_dolval_old_tot moveq_dolval_new_tot), missing
egen moveq_dolval_raddiag = rowtotal(moveq_dolval_old_raddiag moveq_dolval_new_raddiag), missing
egen moveq_dolval_radther = rowtotal(moveq_dolval_old_radther moveq_dolval_new_radther), missing
egen moveq_dolval_radio = rowtotal(moveq_dolval_old_radio moveq_dolval_new_radio), missing

drop *_old_* *_new_*

cleandata

save "Stata/B1_96.dta", replace


* import B1_10.csv
import delimited "B1_10.csv", delimiter(comma) clear

egen bldg_sqft_raddiag_n = rowtotal(bldg_sqft_raddiag bldg_sqft_ct bldg_sqft_mri), missing
egen moveq_dolval_raddiag_n = rowtotal(moveq_dolval_raddiag moveq_dolval_ct moveq_dolval_mri), missing

drop bldg_sqft_raddiag moveq_dolval_raddiag

rename bldg_sqft_raddiag_n bldg_sqft_raddiag
rename moveq_dolval_raddiag_n moveq_dolval_raddiag

drop *_ct* *_mri*

cleandata

save "Stata/B1_10.dta", replace
