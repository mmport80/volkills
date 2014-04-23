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
from QuantLib import *
from volkills.models import Equity_Option


#######################################################################
## 1) Global data
## 2) Date setup
## 3) Construct curves and take care of market data
## 4) Setup initial option
## 5) Calibrate and find vols
## 6) Collate results



def convertDatetoQLFormat(date):
	return Date(date.day, date.month, date.year)
	

def getProcess(valuation_date, interest_rate, dividend_yield, volatility_rate, underlying_price):


	###################################################
	##2)
	#Date setup
	###################################################

	#Assumptions
	calendar = UnitedStates()
	day_counter = ActualActual()

	valuation_date_ql = convertDatetoQLFormat(valuation_date)

	Settings.instance().evaluation_date = valuation_date_ql


	###################################################
	##3)
	#Curve setup
	###################################################

	interest_curve = FlatForward(valuation_date_ql, interest_rate, day_counter )

	dividend_curve = FlatForward(valuation_date_ql, dividend_yield, day_counter )

	volatility_curve = BlackConstantVol(valuation_date_ql, calendar, volatility_rate, day_counter )

	#Collate market data together
	u = QuoteHandle(SimpleQuote(underlying_price)) 
	d = YieldTermStructureHandle(dividend_curve)
	r = YieldTermStructureHandle(interest_curve)
	v = BlackVolTermStructureHandle(volatility_curve)  
	
	return BlackScholesMertonProcess(u, d, r, v)

	
###################################################
##4)
#Option setup
###################################################
	
def getEuroOption(expiry_date, put_or_call, strike_price, process):
	
	expiry_date_ql = convertDatetoQLFormat(expiry_date)
	
	exercise = EuropeanExercise(expiry_date_ql)  
	
	if put_or_call == "call":
		payoff = PlainVanillaPayoff(Option.Call, strike_price)
	else:
		payoff = PlainVanillaPayoff(Option.Put, strike_price)
	

	#Option Setup
	option =  VanillaOption(payoff, exercise)
	
	engine = AnalyticEuropeanEngine(process)
	
	option.setPricingEngine(engine)
	
	return option


def getAmericanOption(valuation_date, expiry_date, put_or_call, strike_price, process):
	
	valuation_date_ql = convertDatetoQLFormat(valuation_date)
	expiry_date_ql = convertDatetoQLFormat(expiry_date)
	
	exercise = AmericanExercise(valuation_date_ql, expiry_date_ql)
	
	if put_or_call == "call":
		payoff = PlainVanillaPayoff(Option.Call, strike_price)
	else:
		payoff = PlainVanillaPayoff(Option.Put, strike_price)
	
	#Option Setup
	option =  VanillaOption(payoff, exercise)
	
	time_steps = 100
	grid_points = 100
	
	#engine = BinomialVanillaEngine(process,'crr',time_steps)
	engine = FDAmericanEngine(process,time_steps,grid_points)
	
	option.setPricingEngine(engine)
	
	return option


###################################################
##5)
##Collate results
###################################################

def getAmericanResults(o, option):
	o.result_npv			= option.NPV()
	o.result_delta			= option.delta()
	o.result_gamma			= option.gamma()
	#o.result_theta			= option.theta()

	o.save()
	
	return o
	
	
def getEuropeanResults(o, option):
	o.result_npv			= option.NPV()
	o.result_delta			= option.delta()
	o.result_gamma			= option.gamma()
	o.result_theta			= option.theta()
	o.result_vega			= option.vega()
	o.result_rho			= option.rho()
	o.result_dividend_rho 		= option.dividendRho()
	o.result_theta_per_day 		= option.thetaPerDay()
	o.result_strike_sensitivity 	= option.strikeSensitivity()
	
	o.save()
	
	return o


def europeanValuation(o):
	process = getProcess( o.valuation_date, o.interest_rate, o.dividend_yield, o.volatility_rate, o.underlying_price)

	eOption = getEuroOption( o.expiry_date, o.put_or_call, o.strike_price, process)

	return getEuropeanResults(o, eOption)
	
	
def americanValuation(o):

	process = getProcess( o.valuation_date, o.interest_rate, o.dividend_yield, o.volatility_rate, o.underlying_price)

	aOption = getAmericanOption( o.valuation_date, o.expiry_date, o.put_or_call, o.strike_price, process)

	return getAmericanResults(o, aOption)
	
	
def europeanCalibration(o):
	#pass dummy volatility
	process = getProcess( o.valuation_date, o.interest_rate, o.dividend_yield, 0.2, o.underlying_price)

	eOption = getEuroOption( o.expiry_date, o.put_or_call, o.strike_price, process)

	o.result_implied_volatility = eOption.impliedVolatility(o.market_value, process)

	calibrated_process = getProcess( o.valuation_date, o.interest_rate, o.dividend_yield, o.result_implied_volatility, o.underlying_price)

	calibrated_eOption = getEuroOption( o.expiry_date, o.put_or_call, o.strike_price, calibrated_process)

	return getEuropeanResults(o, calibrated_eOption)
	
	
def americanCalibration(o):
	#pass dummy volatility
	process = getProcess( o.valuation_date, o.interest_rate, o.dividend_yield, 0.2, o.underlying_price)

	aOption = getAmericanOption( o.valuation_date, o.expiry_date, o.put_or_call, o.strike_price, process)

	o.result_implied_volatility = aOption.impliedVolatility(o.market_value, process)

	calibrated_process = getProcess( o.valuation_date, o.interest_rate, o.dividend_yield, o.result_implied_volatility, o.underlying_price)

	calibrated_aOption = getAmericanOption( o.valuation_date, o.expiry_date, o.put_or_call, o.strike_price, calibrated_process)

	return getAmericanResults(o, calibrated_aOption)
	
