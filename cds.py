'''
    QuantLib with python example
    Copyright (C) 2014 John Orford

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
#######################################################################
## 1) Global data
## 2) Date setup
## 3) Construct yield term structure
## 4) Setup initial bond
## 5) Calibrate and find spread
## 6) Collate results


from QuantLib import *
from volkills.models import CDS



def modelCds_Value(c):


	#######################################################################
	## 1) Global data
	calendar = WeekendsOnly()

	# The conventional recovery rate to apply in the calculation is as specified by ISDA, 
	# not necessarily equal to the market-quoted one. It is typically 0.4 for SeniorSec 
	# and 0.2 for subordinate_date_ql_ql
	recovery_rate = 0.4

	#if nominal is -ve then seller else buyer
	buy_or_sell = Protection.Buyer
	day_counter = Actual365Fixed()
	payment_frequency = Quarterly
	payment_convention = Following
	#default 'CDS' choice not implemented
	date_generation = DateGeneration.TwentiethIMM


	#######################################################################
	## 2) Date setup
	
	valuation_date_ql 	= Date(c.valuation_date.day,c.valuation_date.month,c.valuation_date.year)
	maturity_date_ql 	= Date(c.maturity_date.day,c.maturity_date.month,c.maturity_date.year)
	
	
        #must be a business day
	valuation_date_ql = calendar.adjust(valuation_date_ql);
	maturity_date_ql = calendar.adjust(maturity_date_ql);

	Settings.instance().evaluationDate = valuation_date_ql


	#######################################################################
	## 3) Construct term structures

	## Discounting setup

	zcQuotes = [	(c.term_structure_1m, Period(1,Months)),
			(c.term_structure_3m, Period(3,Months)),		
			(c.term_structure_6m, Period(6,Months)),
			(c.term_structure_1y, Period(1,Years)),
			(c.term_structure_2y, Period(2,Years)),
			(c.term_structure_3y, Period(3,Years)),
			(c.term_structure_5y, Period(5,Years)),
			(c.term_structure_7y, Period(7,Years)),
			(c.term_structure_10y, Period(10,Years)),
			(c.term_structure_20y, Period(20,Years)),
			(c.term_structure_30y, Period(30,Years))
		]

	zcHelpers = [ DepositRateHelper(	QuoteHandle(SimpleQuote(r)),
			                	tenor, 
						0,
			                	calendar, 
						payment_convention,
			        	        True, 
						day_counter)
	      	for (r,tenor) in zcQuotes ]

	discountingTermStructure = PiecewiseFlatForward(valuation_date_ql, 
							zcHelpers,
							day_counter)

	interest_rate = YieldTermStructureHandle(discountingTermStructure)


	##Set up hazard rate term structure in order to calibrate latr
	##Assume flat structure

	hr = QuoteHandle(SimpleQuote(c.default_probability))

	fhr = FlatHazardRate(	valuation_date_ql,
				hr,
				day_counter
				)
	probability = DefaultProbabilityTermStructureHandle(fhr)


	#######################################################################
	## 4) Setup initial CDS

	engine = MidPointCdsEngine(probability, recovery_rate, interest_rate)


	cdsSchedule = Schedule(	valuation_date_ql,
	    	                maturity_date_ql, 
				Period(payment_frequency),
	                     	calendar,
	                     	Unadjusted, 
				Unadjusted,
	                     	date_generation, 
				False)

	cds = CreditDefaultSwap(buy_or_sell,
				c.nominal,
				c.contract_spread,
				cdsSchedule,
				payment_convention,
				day_counter
				)


			
	cds.setPricingEngine(engine)

	#######################################################################
	## 6) Collate results

	c.result_npv 			= cds.NPV()
	c.result_coupon_leg_bps 	= cds.couponLegBPS()
	c.result_fair_spread		= cds.fairSpread()
	c.result_default_leg_npv	= cds.defaultLegNPV()
	c.result_coupon_leg_npv 	= cds.couponLegNPV()
	c.result_running_spread 	= cds.runningSpread()
	
	c.save()

	return c
		


def modelCds_Calibrate(c):


	#######################################################################
	## 1) Global data
	calendar = WeekendsOnly()

	# The conventional recovery rate to apply in the calculation is as specified by ISDA, 
	# not necessarily equal to the market-quoted one. It is typically 0.4 for SeniorSec 
	# and 0.2 for subordinate_date_ql_ql
	recovery_rate = 0.4

	#if nominal is -ve then seller else buyer
	buy_or_sell = Protection.Buyer
	day_counter = Actual365Fixed()
	payment_frequency = Quarterly
	payment_convention = Following
	#default 'CDS' choice not implemented
	date_generation = DateGeneration.TwentiethIMM


	#######################################################################
	## 2) Date setup
	
	valuation_date_ql 	= Date(c.valuation_date.day,c.valuation_date.month,c.valuation_date.year)
	maturity_date_ql 	= Date(c.maturity_date.day,c.maturity_date.month,c.maturity_date.year)
	
	
        #must be a business day
	valuation_date_ql = calendar.adjust(valuation_date_ql);
	maturity_date_ql = calendar.adjust(maturity_date_ql);

	Settings.instance().evaluationDate = valuation_date_ql


	#######################################################################
	## 3) Construct term structures

	## Discounting setup

	zcQuotes = [	(c.term_structure_1m, Period(1,Months)),
			(c.term_structure_3m, Period(3,Months)),		
			(c.term_structure_6m, Period(6,Months)),
			(c.term_structure_1y, Period(1,Years)),
			(c.term_structure_2y, Period(2,Years)),
			(c.term_structure_3y, Period(3,Years)),
			(c.term_structure_5y, Period(5,Years)),
			(c.term_structure_7y, Period(7,Years)),
			(c.term_structure_10y, Period(10,Years)),
			(c.term_structure_20y, Period(20,Years)),
			(c.term_structure_30y, Period(30,Years))
		]

	zcHelpers = [ DepositRateHelper(	QuoteHandle(SimpleQuote(r)),
			                	tenor, 
						0,
			                	calendar, 
						payment_convention,
			        	        True, 
						day_counter)
	      	for (r,tenor) in zcQuotes ]

	discountingTermStructure = PiecewiseFlatForward(valuation_date_ql, 
							zcHelpers,
							day_counter)

	interest_rate = YieldTermStructureHandle(discountingTermStructure)


	##Set up hazard rate term structure in order to calibrate latr
	##Assume flat structure

	hr = QuoteHandle(SimpleQuote(0.01))

	fhr = FlatHazardRate(	valuation_date_ql,
				hr,
				day_counter
				)
	probability = DefaultProbabilityTermStructureHandle(fhr)


	#######################################################################
	## 4) Setup initial CDS

	engine = MidPointCdsEngine(probability, recovery_rate, interest_rate)


	cdsSchedule = Schedule(	valuation_date_ql,
	    	                maturity_date_ql, 
				Period(payment_frequency),
	                     	calendar,
	                     	Unadjusted, 
				Unadjusted,
	                     	date_generation, 
				False)

	cds = CreditDefaultSwap(buy_or_sell,
				c.nominal,
				c.contract_spread,
				cdsSchedule,
				payment_convention,
				day_counter
				)
			
	cds.setPricingEngine(engine)


	#######################################################################
	## 5) Calibrate and find hazard rate
	#then feed back into model and remodel

	hr_calibrated = cds.impliedHazardRate(c.market_value, interest_rate, day_counter, recovery_rate)

	hr_qh_calibrated = QuoteHandle(SimpleQuote(hr_calibrated))

	fhr_calibrated = FlatHazardRate(valuation_date_ql, hr_qh_calibrated, day_counter)
			
	probability_calibrated = DefaultProbabilityTermStructureHandle(fhr_calibrated)

	engine_calibrated = MidPointCdsEngine(probability_calibrated, recovery_rate, interest_rate)

	cds.setPricingEngine(engine_calibrated)


	#######################################################################
	## 6) Collate results

	c.result_npv 			= cds.NPV()
	c.result_coupon_leg_bps 	= cds.couponLegBPS()
	c.result_fair_spread		= cds.fairSpread()
	c.result_default_leg_npv	= cds.defaultLegNPV()
	c.result_coupon_leg_npv 	= cds.couponLegNPV()
	c.result_running_spread 	= cds.runningSpread()
	c.result_implied_hazard_rate 	= cds.impliedHazardRate(c.market_value, interest_rate, day_counter, recovery_rate)
	
	c.save()

	return c
		
