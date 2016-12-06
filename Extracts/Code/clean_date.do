******** DATE ADJUSTMENTS ********
gen fybdt = date(fy_bgn_dt,"YMD")
gen fyedt = date(fy_end_dt,"YMD")
drop fy_bgn_dt fy_end_dt
rename fybdt fy_bgn_dt
rename fyedt fy_end_dt

gen year = year(fy_bgn_dt)
gen mon = month(fy_bgn_dt)
replace year = year + 1 if inrange(mon,10,12)
drop mon

/*
* Deal with duplicate hosp-year pairs
gen nummon = year(fy_end_dt)*12+month(fy_end_dt)-year(fy_bgn_dt)*12-month(fy_bgn_dt)+1

egen group = group(prvdr_num year)
sum group, meanonly
local numgps = `r(max)'
forvalues i = 1/`numgps' {
	di `i'/`numgps'
	qui count if group==`i'
	if `r(N)'>1 {
		if `r(N)'==2{
			qui sum nummon if group==`i'
			if `r(max)'==12 & `r(mean)'!=12 {
				qui sum prvdr_num if group==`i'
				local mcrid = `r(mean)'
				qui sum year if group==`i'
				local yr = `r(mean)'
				count if prvdr_num==`mcrid' & year==`yr'-1
				if `r(N)'==0 {
					replace year = year - 1 if group==`i' & nummon!=12
				}
			}
			else {
				qui sum fy_bgn_dt if group==`i'
				local bg2 = `r(max)'
				qui sum fy_end_dt if group==`i'
				local en1 = `r(min)'
				if `bg2'-`en1'<=1 {
					drop if group==`i'
					**** collapse (sum) rev* nummon (max) prvdr_ctrl_type_cd hosp_id_medicare fyedt cbsa cbsa_hospital year isfloor wi_diff group duptag (min) fybdt (mean) beds if group==`i'
				}
			}
		}
	}
}

duplicates tag prvdr_num year, generate(duptag)
duplicates report prvdr_num year
drop if duptag>0
drop group duptag
*/
