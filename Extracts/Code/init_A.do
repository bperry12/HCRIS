cap program drop cleandata
program define cleandata

* label variables
label var exp_capequip_sal "EXPENSE: CAPITAL EQUIPMENT, SALARY"
label var exp_radiodiag_sal "EXPENSE: DIAGNOSTIC RADIOLOGY, SALARY"
label var exp_radiother_sal "EXPENSE: THERAPEUTIC RADIOLOGY, SALARY"
label var exp_radiosotope_sal "EXPENSE: RADIOISOTOPE, SALARY"

label var exp_capequip_oth "EXPENSE: CAPITAL EQUIPMENT, OTHER"
label var exp_radiodiag_oth "EXPENSE: DIAGNOSTIC RADIOLOGY, OTHER"
label var exp_radiother_oth "EXPENSE: THERAPEUTIC RADIOLOGY, OTHER"
label var exp_radiosotope_oth "EXPENSE: RADIOISOTOPE, OTHER"

label var exp_capequip "EXPENSE: CAPITAL EQUIPMENT, TOTAL"
label var exp_radiodiag "EXPENSE: DIAGNOSTIC RADIOLOGY, TOTAL"
label var exp_radiother "EXPENSE: THERAPEUTIC RADIOLOGY, TOTAL"
label var exp_radiosotope "EXPENSE: RADIOISOTOPE, TOTAL"


* clean up missing values
foreach var of varlist exp*_sal exp*_oth {
	replace `var' = 0 if missing(`var')
}

* correct missing totals
foreach var of varlist exp_capequip exp_radiodiag exp_radiother exp_radiosotope {
	replace `var' = `var'_sal + `var'_oth if missing(`var')
}

* reorder variables
order exp_radiodiag_sal, after(exp_capequip_sal)
order exp_radiodiag_oth, after(exp_capequip_oth)
order exp_radiodiag, after(exp_capequip)

end



* import A_96.csv
import delimited "A_96.csv", delimiter(comma) clear

egen exp_capequip_sal = rowtotal(exp_capequip_old_sal exp_capequip_new_sal), missing
egen exp_capequip_oth = rowtotal(exp_capequip_old_oth exp_capequip_new_oth), missing
egen exp_capequip = rowtotal(exp_capequip_old exp_capequip_new), missing

drop *_old* *_new*

cleandata

save "Stata/A_96.dta", replace



* import A_10.csv
import delimited "A_10.csv", delimiter(comma) clear

egen exp_radiodiag_sal_n = rowtotal(exp_radiodiag_sal exp_ct_sal exp_mri_sal), missing
egen exp_radiodiag_oth_n = rowtotal(exp_radiodiag_oth exp_ct_oth exp_mri_oth), missing
egen exp_radiodiag_n = rowtotal(exp_radiodiag exp_ct exp_mri), missing

drop exp_radiodiag_sal exp_radiodiag_oth exp_radiodiag

rename exp_radiodiag_sal_n exp_radiodiag_sal
rename exp_radiodiag_oth_n exp_radiodiag_oth
rename exp_radiodiag_n exp_radiodiag

drop *_ct* *_mri*

cleandata

save "Stata/A_10.dta", replace
