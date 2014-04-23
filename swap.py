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
from volkills.models import IRS





		
		


def modelSwap_Calibrate(s):

	#Assumptions
	floatingLegAdjustment = ModifiedFollowing
	compounding = QuantLib.Compounded
	dayCounter =  ActualActual(ActualActual.ISDA)
	settlementDays = 2
	fixingDays = 2
	fixedLegAdjustment = Unadjusted


	valuation_date_ql 	= Date(s.valuation_date.day,s.valuation_date.month,s.valuation_date.year)
	#not really necessary for swaps which have already started
	start_date_ql 	= Date(s.start_date.day,s.start_date.month,s.start_date.year)
	maturity_date_ql 	= Date(s.maturity_date.day,s.maturity_date.month,s.maturity_date.year)


	if s.fixed_leg_frequency == 'once':
		fixed_leg_frequency_ql = QuantLib.Once
	elif s.fixed_leg_frequency == 'annual':
		fixed_leg_frequency_ql = QuantLib.Annual
	elif s.fixed_leg_frequency == 'semiannual':
		fixed_leg_frequency_ql = QuantLib.Semiannual
	elif s.fixed_leg_frequency == 'quarterly':
		fixed_leg_frequency_ql = QuantLib.Quarterly
	elif s.fixed_leg_frequency == 'bimonthly':
		fixed_leg_frequency_ql = QuantLib.Bimonthly
	elif s.fixed_leg_frequency == 'monthly':
		fixed_leg_frequency_ql = QuantLib.Monthly
	elif s.fixed_leg_frequency == 'weekly':
		fixed_leg_frequency_ql = QuantLib.Weekly
	elif s.fixed_leg_frequency == 'daily':
		fixed_leg_frequency_ql = QuantLib.Daily


	if s.floating_leg_frequency == 'once':
		floating_leg_frequency_ql = QuantLib.Once
	elif s.floating_leg_frequency == 'annual':
		floating_leg_frequency_ql = QuantLib.Annual
	elif s.floating_leg_frequency == 'semiannual':
		floating_leg_frequency_ql = QuantLib.Semiannual
	elif s.floating_leg_frequency == 'quarterly':
		floating_leg_frequency_ql = QuantLib.Quarterly
	elif s.floating_leg_frequency == 'bimonthly':
		floating_leg_frequency_ql = QuantLib.Bimonthly
	elif s.floating_leg_frequency == 'monthly':
		floating_leg_frequency_ql = QuantLib.Monthly
	elif s.floating_leg_frequency == 'weekly':
		floating_leg_frequency_ql = QuantLib.Weekly
	elif s.floating_leg_frequency == 'daily':
		floating_leg_frequency_ql = QuantLib.Daily


	fixedLegTenor = Period(fixed_leg_frequency_ql)
	floatingLegTenor = Period(floating_leg_frequency_ql)


	#######################################################################
	## 2) Date setup


	calendar = TARGET()

	#Assume settlement is +2
	settlementDate_ql = calendar.advance(valuation_date_ql,2,Days)
	Settings.instance().evaluationDate = valuation_date_ql



	#######################################################################
	## 3) Construct yield term structure

	## Discounting setup

	zcQuotes = [	(s.term_structure_1m, Period(1,Months)),
			(s.term_structure_3m, Period(3,Months)),		
			(s.term_structure_6m, Period(6,Months)),
			(s.term_structure_1y, Period(1,Years)),
			(s.term_structure_2y, Period(2,Years)),
			(s.term_structure_3y, Period(3,Years)),
			(s.term_structure_5y, Period(5,Years)),
			(s.term_structure_7y, Period(7,Years)),
			(s.term_structure_10y, Period(10,Years)),
			(s.term_structure_20y, Period(20,Years)),
			(s.term_structure_30y, Period(30,Years))
		]

	zcHelpers = [ DepositRateHelper(QuoteHandle(SimpleQuote(r)),
			                tenor, 
					fixingDays,
			                calendar, 
					ModifiedFollowing,
			        	True, 
					dayCounter)
	      	for (r,tenor) in zcQuotes ]

	bondDiscountingTermStructure = PiecewiseFlatForward(	valuation_date_ql, 
								zcHelpers,
								dayCounter)


	discountTermStructure = RelinkableYieldTermStructureHandle()
	discountTermStructure.linkTo(bondDiscountingTermStructure)



	#######################################################################
	## Libor/Reference curve set up

	zcQuotes2 = [	(s.reference_index_term_structure_1m, Period(1,Months)),
			(s.reference_index_term_structure_3m, Period(3,Months)),		
			(s.reference_index_term_structure_6m, Period(6,Months)),
			(s.reference_index_term_structure_1y, Period(1,Years)),
			(s.reference_index_term_structure_2y, Period(2,Years)),
			(s.reference_index_term_structure_3y, Period(3,Years)),
			(s.reference_index_term_structure_5y, Period(5,Years)),
			(s.reference_index_term_structure_7y, Period(7,Years)),
			(s.reference_index_term_structure_10y, Period(10,Years)),
			(s.reference_index_term_structure_20y, Period(20,Years)),
			(s.reference_index_term_structure_30y, Period(30,Years))
		]

	zcHelpers2 = [ DepositRateHelper(QuoteHandle(SimpleQuote(r)),
			                tenor, fixingDays,
			                calendar, ModifiedFollowing,
		        	        True, dayCounter)
	      	for (r,tenor) in zcQuotes2 ]


	bondDiscountingTermStructure2 = PiecewiseFlatForward(	valuation_date_ql, 
								zcHelpers2,
								dayCounter)

	forecastTermStructure = RelinkableYieldTermStructureHandle()
	forecastTermStructure.linkTo(bondDiscountingTermStructure2)


	index = Euribor(floatingLegTenor,forecastTermStructure)
	floatingLegDayCounter = index.dayCounter()



	#######################################################################
	## 4) Setup initial swap

	# swaps to be priced

	swapEngine = DiscountingSwapEngine(discountTermStructure)

	#is this forward starting or not?
	if start_date_ql > settlementDate_ql:
		ss_date = start_date_ql
	else:
		ss_date = settlementDate_ql

	fixedSchedule = Schedule(ss_date, maturity_date_ql,
	                         fixedLegTenor, calendar,
	                         fixedLegAdjustment, fixedLegAdjustment,
	                         DateGeneration.Backward, False)
	 
	floatingSchedule = Schedule(ss_date, maturity_date_ql,
	                            floatingLegTenor, calendar,
	                            floatingLegAdjustment, floatingLegAdjustment,
	                            DateGeneration.Backward, False)

	forward = VanillaSwap(VanillaSwap.Receiver, s.face,
	                      fixedSchedule, s.fixed_rate, dayCounter,
	                      floatingSchedule, index, s.spread,
	                      dayCounter)
      
      
	forward.setPricingEngine(swapEngine)


	#######################################################################
	## 5) Calibrate and find spread

	#if receive fixed then counterparty credit risk might cause fixed leg to actually be lower
	#which means a zspread should be added to discount away difference...

	#if pay fixed, then receive float

	calibration_spread = (s.market_value - forward.NPV()) / (forward.fixedLegBPS() * 10000)


	forward = VanillaSwap(VanillaSwap.Receiver, s.face,
	                      fixedSchedule, s.fixed_rate + calibration_spread, dayCounter,
	                      floatingSchedule, index, s.spread,
	                      dayCounter)
		      
      
	forward.setPricingEngine(swapEngine)  


	#######################################################################
	## 6) Collate results
	
	s.result_npv			= forward.NPV()
	s.result_fixed_leg_bps		= forward.fixedLegBPS()
	s.result_fair_spread		= forward.fairSpread()
	s.result_spread			= calibration_spread
	s.result_floating_leg_bps	= forward.floatingLegBPS()
	s.result_fair_rate		= forward.fairRate()
	
	s.save()
	
	return s
	
	
	
	


def modelSwap_Value(s):

	#Assumptions
	floatingLegAdjustment = ModifiedFollowing
	compounding = QuantLib.Compounded
	dayCounter =  ActualActual(ActualActual.ISDA)
	settlementDays = 2
	fixingDays = 2
	fixedLegAdjustment = Unadjusted


	valuation_date_ql 	= Date(s.valuation_date.day,s.valuation_date.month,s.valuation_date.year)
	#not really necessary for swaps which have already started
	start_date_ql 	= Date(s.start_date.day,s.start_date.month,s.start_date.year)
	maturity_date_ql 	= Date(s.maturity_date.day,s.maturity_date.month,s.maturity_date.year)


	if s.fixed_leg_frequency == 'once':
		fixed_leg_frequency_ql = QuantLib.Once
	elif s.fixed_leg_frequency == 'annual':
		fixed_leg_frequency_ql = QuantLib.Annual
	elif s.fixed_leg_frequency == 'semiannual':
		fixed_leg_frequency_ql = QuantLib.Semiannual
	elif s.fixed_leg_frequency == 'quarterly':
		fixed_leg_frequency_ql = QuantLib.Quarterly
	elif s.fixed_leg_frequency == 'bimonthly':
		fixed_leg_frequency_ql = QuantLib.Bimonthly
	elif s.fixed_leg_frequency == 'monthly':
		fixed_leg_frequency_ql = QuantLib.Monthly
	elif s.fixed_leg_frequency == 'weekly':
		fixed_leg_frequency_ql = QuantLib.Weekly
	elif s.fixed_leg_frequency == 'daily':
		fixed_leg_frequency_ql = QuantLib.Daily


	if s.floating_leg_frequency == 'once':
		floating_leg_frequency_ql = QuantLib.Once
	elif s.floating_leg_frequency == 'annual':
		floating_leg_frequency_ql = QuantLib.Annual
	elif s.floating_leg_frequency == 'semiannual':
		floating_leg_frequency_ql = QuantLib.Semiannual
	elif s.floating_leg_frequency == 'quarterly':
		floating_leg_frequency_ql = QuantLib.Quarterly
	elif s.floating_leg_frequency == 'bimonthly':
		floating_leg_frequency_ql = QuantLib.Bimonthly
	elif s.floating_leg_frequency == 'monthly':
		floating_leg_frequency_ql = QuantLib.Monthly
	elif s.floating_leg_frequency == 'weekly':
		floating_leg_frequency_ql = QuantLib.Weekly
	elif s.floating_leg_frequency == 'daily':
		floating_leg_frequency_ql = QuantLib.Daily


	fixedLegTenor = Period(fixed_leg_frequency_ql)
	floatingLegTenor = Period(floating_leg_frequency_ql)


	#######################################################################
	## 2) Date setup


	calendar = TARGET()

	#Assume settlement is +2
	settlementDate_ql = calendar.advance(valuation_date_ql,2,Days)
	Settings.instance().evaluationDate = valuation_date_ql



	#######################################################################
	## 3) Construct yield term structure

	## Discounting setup

	zcQuotes = [	(s.term_structure_1m, Period(1,Months)),
			(s.term_structure_3m, Period(3,Months)),		
			(s.term_structure_6m, Period(6,Months)),
			(s.term_structure_1y, Period(1,Years)),
			(s.term_structure_2y, Period(2,Years)),
			(s.term_structure_3y, Period(3,Years)),
			(s.term_structure_5y, Period(5,Years)),
			(s.term_structure_7y, Period(7,Years)),
			(s.term_structure_10y, Period(10,Years)),
			(s.term_structure_20y, Period(20,Years)),
			(s.term_structure_30y, Period(30,Years))
		]

	zcHelpers = [ DepositRateHelper(QuoteHandle(SimpleQuote(r)),
			                tenor, 
					fixingDays,
			                calendar, 
					ModifiedFollowing,
			        	True, 
					dayCounter)
	      	for (r,tenor) in zcQuotes ]

	bondDiscountingTermStructure = PiecewiseFlatForward(	valuation_date_ql, 
								zcHelpers,
								dayCounter)


	discountTermStructure = RelinkableYieldTermStructureHandle()
	discountTermStructure.linkTo(bondDiscountingTermStructure)



	#######################################################################
	## Libor/Reference curve set up

	zcQuotes2 = [	(s.reference_index_term_structure_1m, Period(1,Months)),
			(s.reference_index_term_structure_3m, Period(3,Months)),		
			(s.reference_index_term_structure_6m, Period(6,Months)),
			(s.reference_index_term_structure_1y, Period(1,Years)),
			(s.reference_index_term_structure_2y, Period(2,Years)),
			(s.reference_index_term_structure_3y, Period(3,Years)),
			(s.reference_index_term_structure_5y, Period(5,Years)),
			(s.reference_index_term_structure_7y, Period(7,Years)),
			(s.reference_index_term_structure_10y, Period(10,Years)),
			(s.reference_index_term_structure_20y, Period(20,Years)),
			(s.reference_index_term_structure_30y, Period(30,Years))
		]

	zcHelpers2 = [ DepositRateHelper(QuoteHandle(SimpleQuote(r)),
			                tenor, fixingDays,
			                calendar, ModifiedFollowing,
		        	        True, dayCounter)
	      	for (r,tenor) in zcQuotes2 ]


	bondDiscountingTermStructure2 = PiecewiseFlatForward(	valuation_date_ql, 
								zcHelpers2,
								dayCounter)

	forecastTermStructure = RelinkableYieldTermStructureHandle()
	forecastTermStructure.linkTo(bondDiscountingTermStructure2)


	index = Euribor(floatingLegTenor,forecastTermStructure)
	floatingLegDayCounter = index.dayCounter()



	#######################################################################
	## 4) Setup initial swap

	# swaps to be priced

	swapEngine = DiscountingSwapEngine(discountTermStructure)

	#is this forward starting or not?
	if start_date_ql > settlementDate_ql:
		ss_date = start_date_ql
	else:
		ss_date = settlementDate_ql

	fixedSchedule = Schedule(ss_date, maturity_date_ql,
	                         fixedLegTenor, calendar,
	                         fixedLegAdjustment, fixedLegAdjustment,
	                         DateGeneration.Backward, False)
	 
	floatingSchedule = Schedule(ss_date, maturity_date_ql,
	                            floatingLegTenor, calendar,
	                            floatingLegAdjustment, floatingLegAdjustment,
	                            DateGeneration.Backward, False)



	#######################################################################
	## 5) price with credit spread

	forward = VanillaSwap(VanillaSwap.Receiver, s.face,
	                      fixedSchedule, s.fixed_rate + s.credit_spread, dayCounter,
	                      floatingSchedule, index, s.spread,
	                      dayCounter)
		      
      
	forward.setPricingEngine(swapEngine)  


	#######################################################################
	## 6) Collate results
	
	s.result_npv			= forward.NPV()
	s.result_fixed_leg_bps		= forward.fixedLegBPS()
	s.result_fair_spread		= forward.fairSpread()
	s.result_floating_leg_bps	= forward.floatingLegBPS()
	s.result_fair_rate		= forward.fairRate()
	
	s.save()
	
	return s
