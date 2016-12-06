cap program drop cleandata
program define cleandata

* label the variables
label var capital_begbal_fixequip "CAPITAL: FIXED EQUIPMENT, BEG BALANCE"
label var capital_purchase_fixequip "CAPITAL: FIXED EQUIPMENT, PURCHASES"
label var capital_don_fixequip "CAPITAL: FIXED EQUIPMENT, DONATIONS"
label var capital_totaq_fixequip "CAPITAL: FIXED EQUIPMENT, TOTAL ACQUISITIONS"
label var capital_disp_fixequip "CAPTIAL: FIXED EQUIPMENT, DISPOSALS"
label var capital_endbal_fixequip "CAPITAL: FIXED EQUIPMENT, END BALANCE"
label var capital_fulldep_fixequip "CAPITAL: FIXED EQUIPMENT, FULLY DEPRECIATED"

label var capital_begbal_movequip "CAPITAL: MOVABLE EQUIPMENT, BEG BALANCE"
label var capital_purchase_movequip "CAPITAL: MOVABLE EQUIPMENT, PURCHASES"
label var capital_don_movequip "CAPITAL: MOVABLE EQUIPMENT, DONATIONS"
label var capital_totaq_movequip "CAPITAL: MOVABLE EQUIPMENT, TOTAL ACQUISITIONS"
label var capital_disp_movequip "CAPITAL: MOVABLE EQUIPMENT, DISPOSALS"
label var capital_endbal_movequip "CAPITAL: MOVABLE EQUIPMENT, END BALANCE"
label var capital_fulldep_movequip "CAPITAL: MOVABLE EQUIPMENT, FULLY DEPRECIATED"

label var capcost_dep_equip "EQUIPMENT DEPRECIATION EXPENSES"
label var capcost_lease_equip "EQUIPMENT LEASE EXPENSES"
label var capcost_interest_equip "EQUIPMENT INTEREST EXPENSES"
label var capcost_insurance_equip "EQUIPMENT INSURANCE EXPENSES"
label var capcost_taxes_equip "EQUIPMENT TAX EXPENSES"
label var capcost_other_equip "EQUIPMENT OTHER EXPENSES"
label var capcost_tot_equip "EQUIPMENT TOTAL EXPENSES"

label var capcost_grossass_equip "EQUIPMENT, GROSS VALUE"
label var capcost_caplease_equip "EQUIPMENT, VALUE OF CAPITALIZED LEASES"

* fix totals
replace capital_purchase_fixequip=0 if missing(capital_purchase_fixequip) & ~missing(capital_begbal_fixequip)
replace capital_don_fixequip=0 if missing(capital_don_fixequip) & ~missing(capital_begbal_fixequip)
replace capital_totaq_fixequip=0 if missing(capital_totaq_fixequip) & ~missing(capital_begbal_fixequip)
replace capital_disp_fixequip=0 if missing(capital_disp_fixequip) & ~missing(capital_begbal_fixequip)

replace capital_purchase_movequip=0 if missing(capital_purchase_movequip) & ~missing(capital_begbal_movequip)
replace capital_don_movequip=0 if missing(capital_don_movequip) & ~missing(capital_begbal_movequip)
replace capital_totaq_movequip=0 if missing(capital_totaq_movequip) & ~missing(capital_begbal_movequip)
replace capital_disp_movequip=0 if missing(capital_disp_movequip) & ~missing(capital_begbal_movequip)

replace capcost_dep_equip = 0 if ~missing(capcost_tot_equip)
replace capcost_lease_equip = 0 if ~missing(capcost_tot_equip)
replace capcost_interest_equip = 0 if ~missing(capcost_tot_equip)
replace capcost_insurance_equip = 0 if ~missing(capcost_tot_equip)
replace capcost_taxes_equip = 0 if ~missing(capcost_tot_equip)
replace capcost_other_equip = 0 if ~missing(capcost_tot_equip)

end



* import A7_96.csv
import delimited "A7_96.csv", delimiter(comma) clear

* combine all _new and _old variables
foreach var of varlist *_new {
	local svar = substr("`var'",1,length("`var'")-4)
	egen `svar' = rowtotal(`svar'*), missing
}

drop *_old* *_new*

* fix totals
drop *_totaq_*
egen capital_totaq_fixequip = rowtotal(capital_purchase_fixequip capital_don_fixequip), missing
egen capital_totaq_movequip = rowtotal(capital_purchase_movequip capital_don_movequip), missing

drop *_endbal_*
replace capital_disp_fixequip = -capital_disp_fixequip
replace capital_disp_movequip = -capital_disp_movequip
egen capital_endbal_fixequip = rowtotal(capital_begbal_fixequip capital_totaq_fixequip capital_disp_fixequip) ///
		if ~missing(capital_begbal_fixequip), missing
egen capital_endbal_movequip = rowtotal(capital_begbal_movequip capital_totaq_movequip capital_disp_movequip) ///
		if ~missing(capital_begbal_movequip), missing
replace capital_disp_fixequip = -capital_disp_fixequip
replace capital_disp_movequip = -capital_disp_movequip

cleandata

save "Stata/A7_96.dta", replace

* import A7_10.csv
import delimited "A7_10.csv", delimiter(comma) clear

cleandata

save "Stata/A7_10.dta", replace
