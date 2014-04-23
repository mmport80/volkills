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

from volkills.models import FRN



class modelFrn():
	
	
	
	#######################################################################
	###global data inputs
	def __init__(	self,
			payment_frequency,
			valuation_date,
		        maturity_date,
		        term_structure_1m,
		        term_structure_3m,
		        term_structure_6m,
		        term_structure_1y,
		        term_structure_2y,
		        term_structure_3y,
		        term_structure_5y,
		        term_structure_7y,
		        term_structure_10y,
		        term_structure_20y,
		        term_structure_30y,
		        face,
			coupon,
			market_value):
		
		self.valuation_date = Date(valuation_date.day,valuation_date.month,valuation_date.year)
	        self.selmaturity_date = Date(maturity_date.day,maturity_date.month,maturity_date.year)
		

	        self.term_structure_1m = term_structure_1m
	        self.term_structure_3m = term_structure_3m
	        self.term_structure_6m = term_structure_6m
	        self.term_structure_1y = term_structure_1y	
	        self.term_structure_2y = term_structure_2y
	        self.term_structure_3y = term_structure_3y
	        self.term_structure_5y = term_structure_5y
	        self.term_structure_7y = term_structure_7y
	        self.term_structure_10y = term_structure_10y
	        self.term_structure_20y = term_structure_20y
	        self.term_structure_30y = term_structure_30y


	        self.reference_index_term_structure_1m = reference_index_term_structure_1m
	        self.reference_index_term_structure_3m = reference_index_term_structure_3m
	        self.reference_index_term_structure_6m = reference_index_term_structure_6m
	        self.reference_index_term_structure_1y = reference_index_term_structure_1y
	        self.reference_index_term_structure_2y = reference_index_term_structure_2y
	        self.reference_index_term_structure_3y = reference_index_term_structure_3y
	        self.reference_index_term_structure_5y = reference_index_term_structure_5y
	        self.reference_index_term_structure_7y = reference_index_term_structure_7y
	        self.reference_index_term_structure_10y = reference_index_term_structure_10y
	        self.reference_index_term_structure_20y = reference_index_term_structure_20y
	        self.reference_index_term_structure_30y = reference_index_term_structure_30y



		self.face =face
	  	self.market_value = market_value

		#e.g. 10% = 0.1 here
		self.spread = [spread]
		self.current_floating_rate = current_floating_rate
 
		if payment_frequency == 'once':
			self.payment_frequency = QuantLib.Once
		elif payment_frequency == 'annual':
			self.payment_frequency = QuantLib.Annual
		elif payment_frequency == 'semiannual':
			self.payment_frequency = QuantLib.Semiannual
		elif payment_frequency == 'quarterly':
			self.payment_frequency = QuantLib.Quarterly
		elif payment_frequency == 'bimonthly':
			self.payment_frequency = QuantLib.Bimonthly
		elif payment_frequency == 'monthly':
			self.payment_frequency = QuantLib.Monthly
		elif payment_frequency == 'weekly':
			self.payment_frequency = QuantLib.Weekly
		elif payment_frequency == 'daily':
			self.payment_frequency = QuantLib.Daily
	
	
	
	#######################################################################
	###collate results
	
	def collateResults(self):

		#Initial instance
		original_results = self.modelFrn(0,0)

		
		
		###Duration Calc
		#Shock and reprice
		shocked_up_results = self.modelFrn(original_results['Z Spread'],0.0001)

		#Modified duration
		mod_duration = -1 * (shocked_up_results['NPV'] - original_results['NPV']) * (10000 / original_results['NPV'])
		
		#Update original duration result
		original_results['Duration'] = mod_duration
		
		
		
		###Convexity Calc
		#Shock and reprice
		shocked_down_results = self.modelFrn(original_results['Z Spread'],-0.0001)
		
		#Shock rates down 1bp
		mod_duration_2 = -1 * (shocked_down_results['NPV'] - original_results['NPV']) * (10000 / original_results['NPV']) 
		
		#Update original convexity result
		original_results['Convexity'] = (mod_duration_2 + mod_duration) / (2 * 0.0001)
		
		
		
		return original_results


	def modelFrn(self,z_spread,basis_point_shock):





		#######################################################################
		### Global assumptions
		calendar = TARGET()

		fixingDays = 3
		settlementDays = 3
		redemption = 100
	
		dayCounter =  ActualActual(ActualActual.ISDA)



		#######################################################################
		###Date setup


		settlementDate = calendar.advance(self.valuation_date,settlementDays, Days)

		todaysDate = calendar.adjust(self.valuation_date)
		Settings.instance().evaluationDate = todaysDate

		issueDate = calendar.advance(self.valuation_date,-1, Years)
	
	
	
		#######################################################################
		## Construct zero coupon bond yield curve
	

		zcQuotes = [	(self.term_structure_1m, Period(1,Months)),
				(self.term_structure_3m, Period(3,Months)),		
				(self.term_structure_6m, Period(6,Months)),
				(self.term_structure_1y, Period(1,Years)),
				(self.term_structure_2y, Period(2,Years)),
				(self.term_structure_3y, Period(3,Years)),
				(self.term_structure_5y, Period(5,Years)),
				(self.term_structure_7y, Period(7,Years)),
				(self.term_structure_10y, Period(10,Years)),
				(self.term_structure_20y, Period(20,Years)),
				(self.term_structure_30y, Period(30,Years))
			]

		zcHelpers = [ DepositRateHelper(QuoteHandle(SimpleQuote(r + basis_point_shock)),
				                tenor, fixingDays,
				                calendar, ModifiedFollowing,
			        	        True, dayCounter)
		      	for (r,tenor) in zcQuotes ]

		bondDiscountingTermStructure = PiecewiseFlatForward(	self.valuation_date, 
									zcHelpers,
									dayCounter)


		discountingTermStructure = RelinkableYieldTermStructureHandle()
		discountingTermStructure.linkTo(bondDiscountingTermStructure)



		#######################################################################
		## Libor/Reference curve set up

		zcQuotes2 = [	(self.reference_index_term_structure_1m, Period(1,Months)),
				(self.reference_index_term_structure_3m, Period(3,Months)),		
				(self.reference_index_term_structure_6m, Period(6,Months)),
				(self.reference_index_term_structure_1y, Period(1,Years)),
				(self.reference_index_term_structure_2y, Period(2,Years)),
				(self.reference_index_term_structure_3y, Period(3,Years)),
				(self.reference_index_term_structure_5y, Period(5,Years)),
				(self.reference_index_term_structure_7y, Period(7,Years)),
				(self.reference_index_term_structure_10y, Period(10,Years)),
				(self.reference_index_term_structure_20y, Period(20,Years)),
				(self.reference_index_term_structure_30y, Period(30,Years))
			]

		zcHelpers2 = [ DepositRateHelper(QuoteHandle(SimpleQuote(r + basis_point_shock)),
				                tenor, fixingDays,
				                calendar, ModifiedFollowing,
			        	        True, dayCounter)
		      	for (r,tenor) in zcQuotes2 ]


		bondDiscountingTermStructure2 = PiecewiseFlatForward(
			self.valuation_date, zcHelpers2,
			dayCounter)
	
		liborTermStructure = RelinkableYieldTermStructureHandle()
		liborTermStructure.linkTo(bondDiscountingTermStructure2)



		#######################################################################
		## Bond set up

	
		floatingBondSchedule = Schedule(issueDate,
	                                self.maturity_date, 
					Period(self.payment_frequency),
	                                calendar,
	                                Unadjusted, 
					Unadjusted,
	                                DateGeneration.Backward, 
					True);

		#Should move to global data???
		libor3m = USDLibor(Period(self.payment_frequency),liborTermStructure)
		
		#need to fix!
		#libor3m.addFixing(Date(2, August, 2006),0.0278625)
		#libor3m.addFixing(Date(2, February, 2006),0.0278625)
		libor3m.addFixing(issueDate,self.current_floating_rate)

		floatingRateBond = FloatingRateBond(settlementDays,
	                                    self.face,
	                                    floatingBondSchedule,
	                                    libor3m,
	                                    dayCounter,
	                                    ModifiedFollowing,
	                                    2,
	                                    [1.0],   # Gearings
					    self.spread,  # Spreads
	                                    [],      # Caps
	                                    [],      # Floors
	                                    True,    # Fixing in arrears
	                                    redemption,
	                                    issueDate)



		############################
		##Dummy but necessary(?) code...
		# coupon pricers
		pricer = BlackIborCouponPricer()
		# optionlet volatilities
		volatility = 0.0;
		vol = ConstantOptionletVolatility(	settlementDays,
							calendar,
	                    				ModifiedFollowing,
	                                  		volatility,
	                                  		dayCounter)
		pricer.setCapletVolatility(OptionletVolatilityStructureHandle(vol))
		setCouponPricer(floatingRateBond.cashflows(),pricer)
		###########################



		# pricing engine
		bondEngine = DiscountingBondEngine(discountingTermStructure)
		floatingRateBond.setPricingEngine(bondEngine)



		#########################################################################
		#Calculate Z spread and reprice

		#find accrued - because z spread is calibrated to npv
		accrued = floatingRateBond.accruedAmount()


		if z_spread == 0:
			#calbrate the market value + accrued (assuming mv is quoted clean)
			z_spread = CashFlows.zSpread(floatingRateBond.cashflows(),                                                        
					self.market_value + accrued,
					bondDiscountingTermStructure,
					dayCounter,                                
					QuantLib.Compounded,
					self.payment_frequency,
					False)

		#add spread to term structure
		zSpreadQuoteHandle = QuoteHandle( SimpleQuote(z_spread) )	
		zSpreadedTermStructure = ZeroSpreadedTermStructure(discountingTermStructure,zSpreadQuoteHandle)
	
	
		#set engine to use z spreaded term structure

		zSpreadRelinkableHandle = RelinkableYieldTermStructureHandle()
		zSpreadRelinkableHandle.linkTo(zSpreadedTermStructure)
	
		bondEngine_w_credit_spread = DiscountingBondEngine(zSpreadRelinkableHandle)
		floatingRateBond.setPricingEngine(bondEngine_w_credit_spread)
	
	

		#######################################################################
		##Collate results
	
		yieldx = floatingRateBond.bondYield(dayCounter,QuantLib.Compounded,self.payment_frequency,0.0001,100)
		
		#Yield needs to be an interest rate object
		y = InterestRate(yieldx,dayCounter,Compounded,Annual)
	
		return 	{
			'Accrued'	: accrued,
			'NPV'		: floatingRateBond.NPV(),
			'Z Spread'	: z_spread,
			'Yield'		: yieldx,
			'Convexity'	: BondFunctions.convexity(floatingRateBond,y),
			'BPS'		: BondFunctions.bps(floatingRateBond,y),
			'Basis Pt Val'  : BondFunctions.basisPointValue(floatingRateBond,y),
			'Yield Val BP'	: BondFunctions.yieldValueBasisPoint(floatingRateBond,y)
			}
