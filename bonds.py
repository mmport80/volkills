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
from volkills.models import Fixed_Rate_Bond, FRN

def YieldQuoteTermStructureToArray(f):
	return [(f.term_structure_1m, Period(1,Months)),
		(f.term_structure_3m, Period(3,Months)),		
		(f.term_structure_6m, Period(6,Months)),
		(f.term_structure_1y, Period(1,Years)),
		(f.term_structure_2y, Period(2,Years)),
		(f.term_structure_3y, Period(3,Years)),
		(f.term_structure_5y, Period(5,Years)),
		(f.term_structure_7y, Period(7,Years)),
		(f.term_structure_10y, Period(10,Years)),
		(f.term_structure_20y, Period(20,Years)),
		(f.term_structure_30y, Period(30,Years)) ]

def YieldQuoteRefIndexToArray(f):
	return [(f.reference_index_term_structure_1m, Period(1,Months)),
		(f.reference_index_term_structure_3m, Period(3,Months)),		
		(f.reference_index_term_structure_6m, Period(6,Months)),
		(f.reference_index_term_structure_1y, Period(1,Years)),
		(f.reference_index_term_structure_2y, Period(2,Years)),
		(f.reference_index_term_structure_3y, Period(3,Years)),
		(f.reference_index_term_structure_5y, Period(5,Years)),
		(f.reference_index_term_structure_7y, Period(7,Years)),
		(f.reference_index_term_structure_10y, Period(10,Years)),
		(f.reference_index_term_structure_20y, Period(20,Years)),
		(f.reference_index_term_structure_30y, Period(30,Years)) ]


def fRNCalibration(f):
	valuation_date_ql = Date(f.valuation_date.day,f.valuation_date.month,f.valuation_date.year)
        maturity_date_ql = Date(f.maturity_date.day,f.maturity_date.month,f.maturity_date.year)

	payment_frequency_ql = getFrequency(f.payment_frequency)

	#######################################################################
	### Global assumptions

	calendar = UnitedStates()

	day_counter =  ActualActual(ActualActual.ISMA)

	payment_convention = ModifiedFollowing
	compounding = QuantLib.Compounded

	#######################################################################
	###Date setup
	Settings.instance().evaluationDate = valuation_date_ql

	#######################################################################
	## 3) Construct yield term structure
	# Create a dictionary of yield quotes by tenor
	zcQuotes = YieldQuoteTermStructureToArray(f)

	#######################################################################
	## Libor/Reference curve set up

	zcQuotes2 = YieldQuoteRefIndexToArray(f)

	# Handle for the term structure linked to flat forward curve
	# I think this is used so that curves can be swapped in and out
	# Unsure how to do that yet though
	bondDiscountingTermStructure = getTermStructure(valuation_date_ql, zcQuotes, calendar, payment_convention, day_counter)

	bondDiscountingTermStructure2 = getTermStructure(valuation_date_ql, zcQuotes2, calendar, payment_convention, day_counter)

	floatingRateBond = getFloatingRateBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, f.face, f.spread,  payment_convention, f.current_floating_rate, day_counter, bondDiscountingTermStructure, bondDiscountingTermStructure2 )
	
	#net credit spread with contract spread
	#probably not correct if we have a proper libor index...
	f.result_spread = CashFlows.zSpread(	floatingRateBond.cashflows(),                                                        
						f.market_value + floatingRateBond.accruedAmount(),
						bondDiscountingTermStructure,
						day_counter,                                
						compounding,
						payment_frequency_ql,
						True)					
	f.save()
	
	floatingRateBond = getFloatingRateBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, f.face, f.spread,  payment_convention, f.current_floating_rate, day_counter, bondDiscountingTermStructure, bondDiscountingTermStructure2, f.result_spread )
	
	return getFRNResults(floatingRateBond, compounding, f, day_counter, payment_frequency_ql)


def fRNValuation(f):
	valuation_date_ql = Date(f.valuation_date.day,f.valuation_date.month,f.valuation_date.year)
        maturity_date_ql = Date(f.maturity_date.day,f.maturity_date.month,f.maturity_date.year)

	payment_frequency_ql = getFrequency(f.payment_frequency)

	#######################################################################
	### Global assumptions

	calendar = UnitedStates()

	day_counter =  ActualActual(ActualActual.ISMA)

	payment_convention = ModifiedFollowing
	compounding = QuantLib.Compounded

	#######################################################################
	###Date setup
	Settings.instance().evaluationDate = valuation_date_ql

	#######################################################################
	## 3) Construct yield term structure
	# Create a dictionary of yield quotes by tenor
	zcQuotes = YieldQuoteTermStructureToArray(f)

	#######################################################################
	## Libor/Reference curve set up

	zcQuotes2 = YieldQuoteRefIndexToArray(f)

	# Handle for the term structure linked to flat forward curve
	# I think this is used so that curves can be swapped in and out
	# Unsure how to do that yet though
	bondDiscountingTermStructure = getTermStructure(valuation_date_ql, zcQuotes, calendar, payment_convention, day_counter)

	bondDiscountingTermStructure2 = getTermStructure(valuation_date_ql, zcQuotes2, calendar, payment_convention, day_counter)

	floatingRateBond = getFloatingRateBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, f.face, f.spread,  payment_convention, f.current_floating_rate, day_counter, bondDiscountingTermStructure, bondDiscountingTermStructure2, f.credit_spread )
	
	return getFRNResults(floatingRateBond, compounding, f, day_counter, payment_frequency_ql)


def getFloatingRateBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, face, spread, payment_convention, current_floating_rate, day_counter, bondDiscountingTermStructure, bondDiscountingTermStructure2, credit_spread = 0 ):

	issueDate = calendar.advance(valuation_date_ql,-1, Years)
	
	discountingTermStructure = RelinkableYieldTermStructureHandle()
	discountingTermStructure.linkTo(bondDiscountingTermStructure)
	
	liborTermStructure = RelinkableYieldTermStructureHandle()
	liborTermStructure.linkTo(bondDiscountingTermStructure2)
	
	#######################################################################
	## Bond set up

	floatingBondSchedule = Schedule(issueDate,
                                	maturity_date_ql, 
					Period(payment_frequency_ql),
                                	calendar,
                                	Unadjusted, 
					Unadjusted,
                                	DateGeneration.Backward, 
					True);

	#Should move to global data???
	libor3m = USDLibor(Period(payment_frequency_ql),liborTermStructure)

	#need to fix!
	libor3m.addFixing(issueDate,current_floating_rate)

	floatingRateBond = FloatingRateBond(	0,
                                    		face,
                                    	    	floatingBondSchedule,
                                    	    	libor3m,
                                   	     	day_counter,
                                   	     	payment_convention,
                                   	     	2,#??
                                   	     	[1.0],   # Gearings
				   	     	[spread],  # Spreads
                                  	      	[],      # Caps
                                    	    	[],      # Floors
                                    	    	True,    # Fixing in arrears
                                    	    	100,	#Recovery rate
                                    	    	issueDate)
	############################
	##Dummy but necessary(?) code...
	# coupon pricers
	pricer = BlackIborCouponPricer()
	# optionlet volatilities
	volatility = 0.0;
	vol = ConstantOptionletVolatility(	0,
						calendar,
                    				payment_convention,
                                  		volatility,
                                  		day_counter)
	pricer.setCapletVolatility(OptionletVolatilityStructureHandle(vol))
	setCouponPricer(floatingRateBond.cashflows(),pricer)
	
	#########################################################################
	#Use Z spread to price

	#add spread to term structure
	#need to add contract spread here? probably not..
	zSpreadQuoteHandle = QuoteHandle( SimpleQuote( credit_spread) )	
	zSpreadedTermStructure = ZeroSpreadedTermStructure(discountingTermStructure,zSpreadQuoteHandle)

	#set engine to use z spreaded term structure
	zSpreadRelinkableHandle = RelinkableYieldTermStructureHandle()
	zSpreadRelinkableHandle.linkTo(zSpreadedTermStructure)

	bondEngine_w_credit_spread = DiscountingBondEngine(zSpreadRelinkableHandle)
	
	floatingRateBond.setPricingEngine(bondEngine_w_credit_spread)
	
	return floatingRateBond


#######################################################################
## 6) Collate results

def getFRNResults(floatingRateBond, compounding, f, day_counter, payment_frequency_ql):
	#find yield
	yield_rate = floatingRateBond.bondYield(day_counter,compounding,payment_frequency_ql)
	#convert yield to interest rate object
	y = InterestRate(yield_rate,day_counter,compounding,payment_frequency_ql)

	f.result_bps			= BondFunctions.bps(floatingRateBond,y)
	f.result_basis_pt_value		= BondFunctions.basisPointValue(floatingRateBond,y)
	f.result_npv			= floatingRateBond.NPV()
	f.result_yield_value_bp		= BondFunctions.yieldValueBasisPoint(floatingRateBond,y)
	f.result_yield_to_maturity	= yield_rate
	f.result_accrued 		= floatingRateBond.accruedAmount()
	
	f.save()
	
	return f


#######################################################################
## 3) Construct yield term structure

def getTermStructure(valuation_date, zcQuotes, calendar, payment_convention, day_counter):
	# Create deposit rate helpers
	zcHelpers = [ DepositRateHelper(QuoteHandle(SimpleQuote(r)),
			                tenor, 
					0,#fixing days
					calendar, 
					payment_convention,
					True, 
					day_counter)
	      	for (r,tenor) in zcQuotes ]
	
	# Term structure to be used in discounting bond cash flows
	return PiecewiseFlatForward(valuation_date, zcHelpers, day_counter)
	

#######################################################################
## 4) Setup initial bond

def getBond( valuation_date, maturity_date, payment_frequency, calendar, face, coupon, payment_convention, bondDiscountingTermStructure, z_spread = 0):
	
	#move back a year in order to capture all accrued interest
	#may be caught out if there's an irregular coupon payment at beginning
	issue_date = calendar.advance(valuation_date,-1,Years)
	
	#Bond schedule T&Cs
	fixedBondSchedule = Schedule(	issue_date,
	    	                	maturity_date, 
					Period(payment_frequency),
	                     		calendar,
	                     		Unadjusted, 
					Unadjusted,
	                     		DateGeneration.Backward, 
					False)
	#Bond T&Cs
	fixedRateBond = FixedRateBond(	0,
	                       		face,
	                       		fixedBondSchedule,
	                       		[coupon],
	                       	 	bondDiscountingTermStructure.dayCounter(),
	                       		payment_convention,
	                       		100,
					issue_date)

	#Zero spread needs to be a 'quote handle' object whatever that is
	zSpreadQuoteHandle = QuoteHandle( SimpleQuote(z_spread) )

	discountingTermStructure = RelinkableYieldTermStructureHandle()
	discountingTermStructure.linkTo(bondDiscountingTermStructure)	
	
	zSpreadedTermStructure = ZeroSpreadedTermStructure(discountingTermStructure, zSpreadQuoteHandle)

	#Create new relinkable handle for calibrated zero spread
	zSpreadRelinkableHandle = RelinkableYieldTermStructureHandle()

	#Link up
	zSpreadRelinkableHandle.linkTo(zSpreadedTermStructure)
	bondEngine_with_added_zspread = DiscountingBondEngine(zSpreadRelinkableHandle)

	#Set new bond engine
	#Ready for use
	fixedRateBond.setPricingEngine(bondEngine_with_added_zspread)
	
	return fixedRateBond


#######################################################################
## 6) Collate results

def getBondResults(fixedRateBond, compounding, b):
	#find yield
	yield_rate = fixedRateBond.bondYield(fixedRateBond.dayCounter(),compounding,fixedRateBond.frequency())
	#convert yield to interest rate object
	y = InterestRate(yield_rate,fixedRateBond.dayCounter(),compounding,fixedRateBond.frequency())

	b.result_duration		= BondFunctions.duration(fixedRateBond,y)
	b.result_convexity		= BondFunctions.convexity(fixedRateBond,y)
	b.result_bps			= BondFunctions.bps(fixedRateBond,y)
	b.result_basis_pt_value		= BondFunctions.basisPointValue(fixedRateBond,y)
	b.result_npv			= fixedRateBond.NPV()
	b.result_yield_value_bp		= BondFunctions.yieldValueBasisPoint(fixedRateBond,y)
	b.result_yield_to_maturity	= yield_rate
	b.result_accrued_amount		= fixedRateBond.accruedAmount()
	
	b.save()
	
	return b


def getFrequency(payment_frequency):
	
	if payment_frequency == 'once':
		payment_frequency_ql = Once
	elif payment_frequency == 'annual':
		payment_frequency_ql = Annual
	elif payment_frequency == 'semiannual':
		payment_frequency_ql = Semiannual
	elif payment_frequency == 'quarterly':
		payment_frequency_ql = Quarterly
	elif payment_frequency == 'bimonthly':
		payment_frequency_ql = Bimonthly
	elif payment_frequency == 'monthly':
		payment_frequency_ql = Monthly
	elif payment_frequency == 'weekly':
		payment_frequency_ql = Weekly
	elif payment_frequency == 'daily':
		payment_frequency_ql = Daily
		
	return payment_frequency_ql


def bondCalibration( b ):


	#######################################################################
	## 1) Global data

	payment_frequency_ql = getFrequency(b.payment_frequency)

	#Global data defaults
	day_counter = ActualActual(ActualActual.Bond)
	compounding = QuantLib.Compounded
	
	calendar = UnitedStates()
	payment_convention = ModifiedFollowing


	#######################################################################
	## 2) Date setup
	
	#switch to quantlib date object
	valuation_date_ql = Date(b.valuation_date.day,b.valuation_date.month,b.valuation_date.year)
        maturity_date_ql = Date(b.maturity_date.day,b.maturity_date.month,b.maturity_date.year)

	Settings.instance().evaluationDate = valuation_date_ql

	
	#######################################################################
	## 3) Construct yield term structure

	# Create a dictionary of yield quotes by tenor
	zcQuotes = YieldQuoteTermStructureToArray(b)

	# Handle for the term structure linked to flat forward curve
	# I think this is used so that curves can be swapped in and out
	# Unsure how to do that yet though
	bondDiscountingTermStructure = getTermStructure(valuation_date_ql, zcQuotes, calendar, payment_convention, day_counter)

	fixedRateBond = getBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, b.face, b.coupon, payment_convention, bondDiscountingTermStructure)


	#######################################################################
	## 5) Calibrate and find spread

	b.result_spread = CashFlows.zSpread(	fixedRateBond.cashflows(),  
					#Assume market value input is quoted clean
					b.market_value + fixedRateBond.accruedAmount(),
					bondDiscountingTermStructure,
					fixedRateBond.dayCounter(),                                
					compounding,
					fixedRateBond.frequency(),
					True
					)

	b.save()

	fixedRateBond = getBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, b.face, b.coupon, payment_convention, bondDiscountingTermStructure, b.result_spread)

	return getBondResults(fixedRateBond, compounding, b)



def bondValuation( b ):


	#######################################################################
	## 1) Global data

	payment_frequency_ql = getFrequency(b.payment_frequency)

	#Global data defaults
	day_counter = ActualActual(ActualActual.Bond)
	compounding = QuantLib.Compounded
	
	calendar = UnitedStates()
	payment_convention = ModifiedFollowing


	#######################################################################
	## 2) Date setup
	
	#switch to quantlib date object
	valuation_date_ql = Date(b.valuation_date.day,b.valuation_date.month,b.valuation_date.year)
        maturity_date_ql = Date(b.maturity_date.day,b.maturity_date.month,b.maturity_date.year)
	
	#valuation_date_ql = calendar.advance(valuation_date_ql,0,Days)

	Settings.instance().evaluationDate = valuation_date_ql

	
	#######################################################################
	## 3) Construct yield term structure

	# Create a dictionary of yield quotes by tenor
	zcQuotes = [	(b.term_structure_1m, Period(1,Months)),
			(b.term_structure_3m, Period(3,Months)),		
			(b.term_structure_6m, Period(6,Months)),
			(b.term_structure_1y, Period(1,Years)),
			(b.term_structure_2y, Period(2,Years)),
			(b.term_structure_3y, Period(3,Years)),
			(b.term_structure_5y, Period(5,Years)),
			(b.term_structure_7y, Period(7,Years)),
			(b.term_structure_10y, Period(10,Years)),
			(b.term_structure_20y, Period(20,Years)),
			(b.term_structure_30y, Period(30,Years))
		]

	# Handle for the term structure linked to flat forward curve
	# I think this is used so that curves can be swapped in and out
	# Unsure how to do that yet though
	bondDiscountingTermStructure = getTermStructure(valuation_date_ql, zcQuotes, calendar, payment_convention, day_counter)

	fixedRateBond = getBond(valuation_date_ql, maturity_date_ql, payment_frequency_ql, calendar, b.face, b.coupon, payment_convention, bondDiscountingTermStructure, b.spread)

	return getBondResults(fixedRateBond, compounding, b)


