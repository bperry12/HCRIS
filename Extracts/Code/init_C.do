cap program drop cleandata
program define cleandata

* label the variables
label var charges_inpat_raddiag "CHARGES: DIAGNOSTIC RADIOLOGY, INPATIENT"
label var charges_inpat_radther "CHARGES: THERAPEUTIC RADIOLOGY, INPATIENT"
label var charges_inpat_radio "CHARGES: RADIOISOTOPE, INPATIENT"

label var charges_outpat_raddiag "CHARGES: DIAGNOSTIC RADIOLOGY, OUTPATIENT"
label var charges_outpat_radther "CHARGES: THERAPEUTIC RADIOLOGY, OUTPATIENT"
label var charges_outpat_radio "CHARGES: RADIOISOTOPE, OUTPATIENT"

label var charges_total_raddiag "CHARGES: DIAGNOSTIC RADIOLOGY, TOTAL"
label var charges_total_radther "CHARGES: THERAPEUTIC RADIOLOGY, TOTAL"
label var charges_total_radio "CHARGES: RADIOISOTOPE, TOTAL"

order charges_inpat_raddiag, after(rpt_rc_num)
order charges_outpat_raddiag, after(charges_inpat_radio)
order charges_total_raddiag, after(charges_outpat_radio)

end


* import C_96.csv
import delimited "C_96.csv", delimiter(comma) clear

drop charges_total_raddiag charges_total_radther charges_total_radio

egen charges_total_raddiag = rowtotal(charges_inpat_raddiag charges_outpat_raddiag), missing
egen charges_total_radther = rowtotal(charges_inpat_radther charges_outpat_radther), missing
egen charges_total_radio = rowtotal(charges_inpat_radio charges_outpat_radio), missing

cleandata

save "Stata/C_96.dta", replace


* import C_10.csv
import delimited "C_10.csv", delimiter(comma) clear

egen charges_inpat_raddiag_n = rowtotal(charges_inpat_raddiag charges_inpat_ct charges_inpat_mri), missing
egen charges_outpat_raddiag_n = rowtotal(charges_outpat_raddiag charges_outpat_ct charges_outpat_mri), missing
egen charges_total_raddiag_n = rowtotal(charges_total_raddiag charges_total_ct charges_total_mri), missing

drop charges_*_raddiag

rename charges_inpat_raddiag_n charges_inpat_raddiag
rename charges_outpat_raddiag_n charges_outpat_raddiag
rename charges_total_raddiag_n charges_total_raddiag

drop *_ct *_mri

cleandata

save "Stata/C_10.dta", replace 
