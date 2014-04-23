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




from models import *
from django.views.generic import ListView
from datetime import *

from equity_option import *
from bonds import *
from swap import *
from cds import *

##1) Get URL data
##2) Check for results cached in DB
##3) Calculate new results
##


class Cds_Results_Value(ListView):
	model = CDS
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Cds_Results_Value, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		c = CDS(valuation_date 		= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
			maturity_date 		= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),        
		        term_structure_1m 	= float(self.kwargs['term_structure_1m']),
		        term_structure_3m 	= float(self.kwargs['term_structure_3m']),
		        term_structure_6m 	= float(self.kwargs['term_structure_6m']),
		        term_structure_1y 	= float(self.kwargs['term_structure_1y']),
		        term_structure_2y 	= float(self.kwargs['term_structure_2y']),
		        term_structure_3y 	= float(self.kwargs['term_structure_3y']),
		        term_structure_5y 	= float(self.kwargs['term_structure_5y']),
		        term_structure_7y 	= float(self.kwargs['term_structure_7y']),
		        term_structure_10y 	= float(self.kwargs['term_structure_10y']),
		        term_structure_20y 	= float(self.kwargs['term_structure_20y']),
		        term_structure_30y 	= float(self.kwargs['term_structure_30y']),
		        nominal 		= float(self.kwargs['nominal']),
			default_probability	= float(self.kwargs['default_probability']),
			contract_spread 	= float(self.kwargs['contract_spread'])
			)
		#Look for previous calculations
		results = CDS.objects.filter(	valuation_date 		= c.valuation_date,
					        term_structure_1m 	= c.term_structure_1m,
					        term_structure_3m 	= c.term_structure_3m,
					        term_structure_6m 	= c.term_structure_6m,
					        term_structure_1y 	= c.term_structure_1y,
					        term_structure_2y 	= c.term_structure_2y,
					        term_structure_3y 	= c.term_structure_3y,
					        term_structure_5y 	= c.term_structure_5y,
					        term_structure_7y 	= c.term_structure_7y,
					        term_structure_10y 	= c.term_structure_10y,
					        term_structure_20y 	= c.term_structure_20y,
					        term_structure_30y 	= c.term_structure_30y,
					        nominal			= c.nominal,
					        maturity_date 		= c.maturity_date,
						default_probability	= c.default_probability,
						contract_spread 	= c.contract_spread
						)
		#if new instrument
		if len(results) == 0:
			results = []
			results.append( modelCds_Value(c) )
			
		context.update({'instrument' : results[0]})	
		return context


class Cds_Results_Calibrate(ListView):
	model = CDS
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Cds_Results_Calibrate, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		c = CDS(valuation_date 		= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
			maturity_date 		= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),        
		        term_structure_1m 	= float(self.kwargs['term_structure_1m']),
		        term_structure_3m 	= float(self.kwargs['term_structure_3m']),
		        term_structure_6m 	= float(self.kwargs['term_structure_6m']),
		        term_structure_1y 	= float(self.kwargs['term_structure_1y']),
		        term_structure_2y 	= float(self.kwargs['term_structure_2y']),
		        term_structure_3y 	= float(self.kwargs['term_structure_3y']),
		        term_structure_5y 	= float(self.kwargs['term_structure_5y']),
		        term_structure_7y 	= float(self.kwargs['term_structure_7y']),
		        term_structure_10y 	= float(self.kwargs['term_structure_10y']),
		        term_structure_20y 	= float(self.kwargs['term_structure_20y']),
		        term_structure_30y 	= float(self.kwargs['term_structure_30y']),
		        nominal 		= float(self.kwargs['nominal']),
			market_value		= float(self.kwargs['market_value']),
			contract_spread 	= float(self.kwargs['contract_spread'])
			)
		#Look for previous calculations
		results = CDS.objects.filter(	valuation_date 		= c.valuation_date,
					        term_structure_1m 	= c.term_structure_1m,
					        term_structure_3m 	= c.term_structure_3m,
					        term_structure_6m 	= c.term_structure_6m,
					        term_structure_1y 	= c.term_structure_1y,
					        term_structure_2y 	= c.term_structure_2y,
					        term_structure_3y 	= c.term_structure_3y,
					        term_structure_5y 	= c.term_structure_5y,
					        term_structure_7y 	= c.term_structure_7y,
					        term_structure_10y 	= c.term_structure_10y,
					        term_structure_20y 	= c.term_structure_20y,
					        term_structure_30y 	= c.term_structure_30y,
					        nominal			= c.nominal,
					        maturity_date 		= c.maturity_date,
						market_value		= c.market_value,
						contract_spread 	= c.contract_spread
						)
		#if new instrument
		if len(results) == 0:
			results = []
			results.append( modelCds_Calibrate(c) )
			
		context.update({'instrument' : results[0]})	
		return context



class Irs_Results_Value(ListView):
	model = IRS
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Irs_Results_Value, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		s = IRS(term_structure_1m 			= float(self.kwargs['term_structure_1m']),
			term_structure_3m 			= float(self.kwargs['term_structure_3m']),
		        term_structure_6m 			= float(self.kwargs['term_structure_6m']),
		        term_structure_1y 			= float(self.kwargs['term_structure_1y']),
		        term_structure_2y 			= float(self.kwargs['term_structure_2y']),
		        term_structure_3y 			= float(self.kwargs['term_structure_3y']),
		        term_structure_5y 			= float(self.kwargs['term_structure_5y']),
		        term_structure_7y 			= float(self.kwargs['term_structure_7y']),
		        term_structure_10y 			= float(self.kwargs['term_structure_10y']),
		        term_structure_20y 			= float(self.kwargs['term_structure_20y']),
		        term_structure_30y 			= float(self.kwargs['term_structure_30y']),
		        face 					= float(self.kwargs['face']),
			credit_spread				= float(self.kwargs['credit_spread']),
			fixed_rate	 			= float(self.kwargs['fixed_rate']),
			spread 					= float(self.kwargs['spread']),
		        reference_index_term_structure_1m 	= float(self.kwargs['reference_index_term_structure_1m']),
		        reference_index_term_structure_3m 	= float(self.kwargs['reference_index_term_structure_3m']),
		        reference_index_term_structure_6m 	= float(self.kwargs['reference_index_term_structure_6m']),
		        reference_index_term_structure_1y 	= float(self.kwargs['reference_index_term_structure_1y']),
		        reference_index_term_structure_2y 	= float(self.kwargs['reference_index_term_structure_2y']),
		        reference_index_term_structure_3y 	= float(self.kwargs['reference_index_term_structure_3y']),
		        reference_index_term_structure_5y 	= float(self.kwargs['reference_index_term_structure_5y']),
		        reference_index_term_structure_7y 	= float(self.kwargs['reference_index_term_structure_7y']),
		        reference_index_term_structure_10y 	= float(self.kwargs['reference_index_term_structure_10y']),
		        reference_index_term_structure_20y 	= float(self.kwargs['reference_index_term_structure_20y']),
		        reference_index_term_structure_30y 	= float(self.kwargs['reference_index_term_structure_30y']),
		        floating_leg_frequency 			= self.kwargs['floating_leg_frequency'],
			fixed_leg_frequency 			= self.kwargs['fixed_leg_frequency'],
			valuation_date 				= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
			maturity_date 				= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),        
		        start_date 				= date(int(self.kwargs['start_year']),int(self.kwargs['start_month']),int(self.kwargs['start_day'])) 
			)
	
	
		#Look for previous calculations
		results = IRS.objects.filter(	valuation_date 				= s.valuation_date,
					        term_structure_1m 			= s.term_structure_1m,
					        term_structure_3m 			= s.term_structure_3m,
					        term_structure_6m 			= s.term_structure_6m,
					        term_structure_1y 			= s.term_structure_1y,
					        term_structure_2y 			= s.term_structure_2y,
					        term_structure_3y 			= s.term_structure_3y,
					        term_structure_5y 			= s.term_structure_5y,
					        term_structure_7y 			= s.term_structure_7y,
					        term_structure_10y 			= s.term_structure_10y,
					        term_structure_20y 			= s.term_structure_20y,
					        term_structure_30y 			= s.term_structure_30y,
					        face 					= s.face,
					        maturity_date 				= s.maturity_date,
						credit_spread				= s.credit_spread,
					        start_date 				= s.start_date,
						floating_leg_frequency 			= s.floating_leg_frequency,
						fixed_leg_frequency 			= s.fixed_leg_frequency,
						fixed_rate	 			= s.fixed_rate,
						spread 					= s.spread,
					        reference_index_term_structure_1m 	= s.reference_index_term_structure_1m,
					        reference_index_term_structure_3m 	= s.reference_index_term_structure_3m,
					        reference_index_term_structure_6m 	= s.reference_index_term_structure_6m,
					        reference_index_term_structure_1y 	= s.reference_index_term_structure_1y,
					        reference_index_term_structure_2y 	= s.reference_index_term_structure_2y,
					        reference_index_term_structure_3y 	= s.reference_index_term_structure_3y,
					        reference_index_term_structure_5y 	= s.reference_index_term_structure_5y,
					        reference_index_term_structure_7y 	= s.reference_index_term_structure_7y,
					        reference_index_term_structure_10y 	= s.reference_index_term_structure_10y,
					        reference_index_term_structure_20y 	= s.reference_index_term_structure_20y,
					        reference_index_term_structure_30y 	= s.reference_index_term_structure_30y
						)
		#if new instrument
		if len(results) == 0:
			
			results = []
			x = modelSwap_Value(s)
			results.append( x )
			
		context.update({'instrument' : results[0]})	
		return context



class Irs_Results_Calibrate(ListView):
	model = IRS
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Irs_Results_Calibrate, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		s = IRS(term_structure_1m 			= float(self.kwargs['term_structure_1m']),
			term_structure_3m 			= float(self.kwargs['term_structure_3m']),
		        term_structure_6m 			= float(self.kwargs['term_structure_6m']),
		        term_structure_1y 			= float(self.kwargs['term_structure_1y']),
		        term_structure_2y 			= float(self.kwargs['term_structure_2y']),
		        term_structure_3y 			= float(self.kwargs['term_structure_3y']),
		        term_structure_5y 			= float(self.kwargs['term_structure_5y']),
		        term_structure_7y 			= float(self.kwargs['term_structure_7y']),
		        term_structure_10y 			= float(self.kwargs['term_structure_10y']),
		        term_structure_20y 			= float(self.kwargs['term_structure_20y']),
		        term_structure_30y 			= float(self.kwargs['term_structure_30y']),
		        face 					= float(self.kwargs['face']),
			market_value				= float(self.kwargs['market_value']),
			fixed_rate	 			= float(self.kwargs['fixed_rate']),
			spread 					= float(self.kwargs['spread']),
		        reference_index_term_structure_1m 	= float(self.kwargs['reference_index_term_structure_1m']),
		        reference_index_term_structure_3m 	= float(self.kwargs['reference_index_term_structure_3m']),
		        reference_index_term_structure_6m 	= float(self.kwargs['reference_index_term_structure_6m']),
		        reference_index_term_structure_1y 	= float(self.kwargs['reference_index_term_structure_1y']),
		        reference_index_term_structure_2y 	= float(self.kwargs['reference_index_term_structure_2y']),
		        reference_index_term_structure_3y 	= float(self.kwargs['reference_index_term_structure_3y']),
		        reference_index_term_structure_5y 	= float(self.kwargs['reference_index_term_structure_5y']),
		        reference_index_term_structure_7y 	= float(self.kwargs['reference_index_term_structure_7y']),
		        reference_index_term_structure_10y 	= float(self.kwargs['reference_index_term_structure_10y']),
		        reference_index_term_structure_20y 	= float(self.kwargs['reference_index_term_structure_20y']),
		        reference_index_term_structure_30y 	= float(self.kwargs['reference_index_term_structure_30y']),
		        floating_leg_frequency 			= self.kwargs['floating_leg_frequency'],
			fixed_leg_frequency 			= self.kwargs['fixed_leg_frequency'],
			valuation_date 				= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
			maturity_date 				= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),        
		        start_date 				= date(int(self.kwargs['start_year']),int(self.kwargs['start_month']),int(self.kwargs['start_day'])) 
			)
	
	
		#Look for previous calculations
		results = IRS.objects.filter(	valuation_date 				= s.valuation_date,
					        term_structure_1m 			= s.term_structure_1m,
					        term_structure_3m 			= s.term_structure_3m,
					        term_structure_6m 			= s.term_structure_6m,
					        term_structure_1y 			= s.term_structure_1y,
					        term_structure_2y 			= s.term_structure_2y,
					        term_structure_3y 			= s.term_structure_3y,
					        term_structure_5y 			= s.term_structure_5y,
					        term_structure_7y 			= s.term_structure_7y,
					        term_structure_10y 			= s.term_structure_10y,
					        term_structure_20y 			= s.term_structure_20y,
					        term_structure_30y 			= s.term_structure_30y,
					        face 					= s.face,
					        maturity_date 				= s.maturity_date,
						market_value				= s.market_value,
					        start_date 				= s.start_date,
						floating_leg_frequency 			= s.floating_leg_frequency,
						fixed_leg_frequency 			= s.fixed_leg_frequency,
						fixed_rate	 			= s.fixed_rate,
						spread 					= s.spread,
					        reference_index_term_structure_1m 	= s.reference_index_term_structure_1m,
					        reference_index_term_structure_3m 	= s.reference_index_term_structure_3m,
					        reference_index_term_structure_6m 	= s.reference_index_term_structure_6m,
					        reference_index_term_structure_1y 	= s.reference_index_term_structure_1y,
					        reference_index_term_structure_2y 	= s.reference_index_term_structure_2y,
					        reference_index_term_structure_3y 	= s.reference_index_term_structure_3y,
					        reference_index_term_structure_5y 	= s.reference_index_term_structure_5y,
					        reference_index_term_structure_7y 	= s.reference_index_term_structure_7y,
					        reference_index_term_structure_10y 	= s.reference_index_term_structure_10y,
					        reference_index_term_structure_20y 	= s.reference_index_term_structure_20y,
					        reference_index_term_structure_30y 	= s.reference_index_term_structure_30y
						)
		#if new instrument
		if len(results) == 0:			
			results = []
			x = modelSwap_Calibrate(s)
			results.append( x )
			
		context.update({'instrument' : results[0]})	
		return context


class Frn_Results_Calibrate(ListView):
	model = FRN
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Frn_Results_Calibrate, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		f = FRN(	payment_frequency 			= self.kwargs['payment_frequency'],
				valuation_date 				= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
			        maturity_date 				= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),
			        term_structure_1m 			= float(self.kwargs['term_structure_1m']),
			        term_structure_3m 			= float(self.kwargs['term_structure_3m']),
			        term_structure_6m 			= float(self.kwargs['term_structure_6m']),
			        term_structure_1y 			= float(self.kwargs['term_structure_1y']),
			        term_structure_2y 			= float(self.kwargs['term_structure_2y']),
			        term_structure_3y 			= float(self.kwargs['term_structure_3y']),
			        term_structure_5y 			= float(self.kwargs['term_structure_5y']),
			        term_structure_7y 			= float(self.kwargs['term_structure_7y']),
			        term_structure_10y 			= float(self.kwargs['term_structure_10y']),
			        term_structure_20y 			= float(self.kwargs['term_structure_20y']),
			        term_structure_30y 			= float(self.kwargs['term_structure_30y']),
			        face 					= float(self.kwargs['face']),
				market_value				= float(self.kwargs['market_value']),
			        reference_index_term_structure_1m 	= float(self.kwargs['reference_index_term_structure_1m']),
			        reference_index_term_structure_3m 	= float(self.kwargs['reference_index_term_structure_3m']),
			        reference_index_term_structure_6m 	= float(self.kwargs['reference_index_term_structure_6m']),
			        reference_index_term_structure_1y 	= float(self.kwargs['reference_index_term_structure_1y']),
			        reference_index_term_structure_2y 	= float(self.kwargs['reference_index_term_structure_2y']),
			        reference_index_term_structure_3y 	= float(self.kwargs['reference_index_term_structure_3y']),
			        reference_index_term_structure_5y 	= float(self.kwargs['reference_index_term_structure_5y']),
			        reference_index_term_structure_7y 	= float(self.kwargs['reference_index_term_structure_7y']),
			        reference_index_term_structure_10y 	= float(self.kwargs['reference_index_term_structure_10y']),
			        reference_index_term_structure_20y 	= float(self.kwargs['reference_index_term_structure_20y']),
			        reference_index_term_structure_30y 	= float(self.kwargs['reference_index_term_structure_30y']),
				spread 					= float(self.kwargs['spread']),
				current_floating_rate 			= float(self.kwargs['current_floating_rate'])
				)
	
		#Look for previous calculations
		results = FRN.objects.filter(	payment_frequency 			= f.payment_frequency,
						valuation_date 				= f.valuation_date,
					        maturity_date 				= f.maturity_date,
					        term_structure_1m 			= f.term_structure_1m,
					        term_structure_3m 			= f.term_structure_3m,
					        term_structure_6m 			= f.term_structure_6m,
					        term_structure_1y 			= f.term_structure_1y,
					        term_structure_2y 			= f.term_structure_2y,
					        term_structure_3y 			= f.term_structure_3y,
					        term_structure_5y 			= f.term_structure_5y,
					        term_structure_7y 			= f.term_structure_7y,
					        term_structure_10y 			= f.term_structure_10y,
					        term_structure_20y 			= f.term_structure_20y,
					        term_structure_30y 			= f.term_structure_30y,
					        reference_index_term_structure_1m 	= f.reference_index_term_structure_1m,
					        reference_index_term_structure_3m 	= f.reference_index_term_structure_3m,
					        reference_index_term_structure_6m 	= f.reference_index_term_structure_6m,
					        reference_index_term_structure_1y 	= f.reference_index_term_structure_1y,
					        reference_index_term_structure_2y 	= f.reference_index_term_structure_2y,
					        reference_index_term_structure_3y 	= f.reference_index_term_structure_3y,
					        reference_index_term_structure_5y 	= f.reference_index_term_structure_5y,
					        reference_index_term_structure_7y 	= f.reference_index_term_structure_7y,
					        reference_index_term_structure_10y 	= f.reference_index_term_structure_10y,
					        reference_index_term_structure_20y 	= f.reference_index_term_structure_20y,
					        reference_index_term_structure_30y 	= f.reference_index_term_structure_30y,
					        face 					= f.face,
						spread 					= f.spread,
						current_floating_rate			= f.current_floating_rate,
						market_value 				= f.market_value
						)
		#if new instrument
		if len(results) == 0:
			results = []
			x = fRNCalibration(f)
			results.append(x)
			
		context.update({'instrument' : results[0]})	
		return context



class Frn_Results_Value(ListView):
	model = FRN
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Frn_Results_Value, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		f = FRN(payment_frequency 			= self.kwargs['payment_frequency'],
			valuation_date 				= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
			maturity_date 				= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),
			term_structure_1m 			= float(self.kwargs['term_structure_1m']),
		        term_structure_3m 			= float(self.kwargs['term_structure_3m']),
		        term_structure_6m 			= float(self.kwargs['term_structure_6m']),
		        term_structure_1y 			= float(self.kwargs['term_structure_1y']),
			term_structure_2y 			= float(self.kwargs['term_structure_2y']),
		        term_structure_3y 			= float(self.kwargs['term_structure_3y']),
		        term_structure_5y 			= float(self.kwargs['term_structure_5y']),
		        term_structure_7y 			= float(self.kwargs['term_structure_7y']),
		        term_structure_10y 			= float(self.kwargs['term_structure_10y']),
			term_structure_20y 			= float(self.kwargs['term_structure_20y']),
			term_structure_30y 			= float(self.kwargs['term_structure_30y']),
		        face 					= float(self.kwargs['face']),
			credit_spread				= float(self.kwargs['credit_spread']),
		        reference_index_term_structure_1m 	= float(self.kwargs['reference_index_term_structure_1m']),
		        reference_index_term_structure_3m 	= float(self.kwargs['reference_index_term_structure_3m']),
		        reference_index_term_structure_6m 	= float(self.kwargs['reference_index_term_structure_6m']),
		        reference_index_term_structure_1y 	= float(self.kwargs['reference_index_term_structure_1y']),
		        reference_index_term_structure_2y 	= float(self.kwargs['reference_index_term_structure_2y']),
		        reference_index_term_structure_3y 	= float(self.kwargs['reference_index_term_structure_3y']),
		        reference_index_term_structure_5y 	= float(self.kwargs['reference_index_term_structure_5y']),
		        reference_index_term_structure_7y 	= float(self.kwargs['reference_index_term_structure_7y']),
		        reference_index_term_structure_10y 	= float(self.kwargs['reference_index_term_structure_10y']),
		        reference_index_term_structure_20y 	= float(self.kwargs['reference_index_term_structure_20y']),
		        reference_index_term_structure_30y 	= float(self.kwargs['reference_index_term_structure_30y']),
			spread 					= float(self.kwargs['spread']),
			current_floating_rate 			= float(self.kwargs['current_floating_rate'])
			)
		#Look for previous calculations
		results = FRN.objects.filter(	payment_frequency 			= f.payment_frequency,
						valuation_date 				= f.valuation_date,
					        maturity_date 				= f.maturity_date,
					        term_structure_1m 			= f.term_structure_1m,
					        term_structure_3m 			= f.term_structure_3m,
					        term_structure_6m 			= f.term_structure_6m,
					        term_structure_1y 			= f.term_structure_1y,
					        term_structure_2y 			= f.term_structure_2y,
					        term_structure_3y 			= f.term_structure_3y,
					        term_structure_5y 			= f.term_structure_5y,
					        term_structure_7y 			= f.term_structure_7y,
					        term_structure_10y 			= f.term_structure_10y,
					        term_structure_20y 			= f.term_structure_20y,
					        term_structure_30y 			= f.term_structure_30y,
					        reference_index_term_structure_1m 	= f.reference_index_term_structure_1m,
					        reference_index_term_structure_3m 	= f.reference_index_term_structure_3m,
					        reference_index_term_structure_6m 	= f.reference_index_term_structure_6m,
					        reference_index_term_structure_1y 	= f.reference_index_term_structure_1y,
					        reference_index_term_structure_2y 	= f.reference_index_term_structure_2y,
					        reference_index_term_structure_3y 	= f.reference_index_term_structure_3y,
					        reference_index_term_structure_5y 	= f.reference_index_term_structure_5y,
					        reference_index_term_structure_7y 	= f.reference_index_term_structure_7y,
					        reference_index_term_structure_10y 	= f.reference_index_term_structure_10y,
					        reference_index_term_structure_20y 	= f.reference_index_term_structure_20y,
					        reference_index_term_structure_30y 	= f.reference_index_term_structure_30y,
					        face 					= f.face,
						spread 					= f.spread,
						current_floating_rate			= f.current_floating_rate,
						credit_spread 				= f.credit_spread
						)
		#if new instrument
		if len(results) == 0:
			results = []
			x = fRNValuation(f)
			results.append(x)
			
		context.update({'instrument' : results[0]})	
		return context





class Bond_Results_Calibrate(ListView):
	model = Fixed_Rate_Bond
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Bond_Results_Calibrate, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		b = Fixed_Rate_Bond(	payment_frequency 	= self.kwargs['payment_frequency'],
					valuation_date 		= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
				        maturity_date 		= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),
				        term_structure_1m 	= float(self.kwargs['term_structure_1m']),
				        term_structure_3m 	= float(self.kwargs['term_structure_3m']),
				        term_structure_6m 	= float(self.kwargs['term_structure_6m']),
				        term_structure_1y 	= float(self.kwargs['term_structure_1y']),
				        term_structure_2y 	= float(self.kwargs['term_structure_2y']),
				        term_structure_3y 	= float(self.kwargs['term_structure_3y']),
				        term_structure_5y 	= float(self.kwargs['term_structure_5y']),
				        term_structure_7y 	= float(self.kwargs['term_structure_7y']),
				        term_structure_10y 	= float(self.kwargs['term_structure_10y']),
				        term_structure_20y 	= float(self.kwargs['term_structure_20y']),
				        term_structure_30y 	= float(self.kwargs['term_structure_30y']),
				        face 			= float(self.kwargs['face']),
					coupon 			= float(self.kwargs['coupon']),
					market_value		= float(self.kwargs['market_value'])
					)
	
		#Look for previous calculations
		results = Fixed_Rate_Bond.objects.filter(	payment_frequency 	= b.payment_frequency,
								valuation_date 		= b.valuation_date,
							        maturity_date 		= b.maturity_date,
							        term_structure_1m 	= b.term_structure_1m,
							        term_structure_3m 	= b.term_structure_3m,
							        term_structure_6m 	= b.term_structure_6m,
							        term_structure_1y 	= b.term_structure_1y,
							        term_structure_2y 	= b.term_structure_2y,
							        term_structure_3y 	= b.term_structure_3y,
							        term_structure_5y 	= b.term_structure_5y,
							        term_structure_7y 	= b.term_structure_7y,
							        term_structure_10y 	= b.term_structure_10y,
							        term_structure_20y 	= b.term_structure_20y,
							        term_structure_30y 	= b.term_structure_30y,
							        face 			= b.face,
								coupon 			= b.coupon,
								market_value 		= b.market_value
								)	
		#if new instrument
		if len(results) == 0:
			x = bondCalibration( b )
			results = []
			results.append(x)
			
		context.update({'instrument' : results[0]})	
		return context



class Bond_Results_Value(ListView):

	##0) Create New Object
	##1) Get URL data
	##2) Check for results cached in DB
	##3) Calculate new results
	##4) Save down results and object
	##5) Show results
	model = Fixed_Rate_Bond
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Bond_Results_Value, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		b = Fixed_Rate_Bond(	payment_frequency 	= self.kwargs['payment_frequency'],
					valuation_date 		= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
				        maturity_date 		= date(int(self.kwargs['maturity_year']),int(self.kwargs['maturity_month']),int(self.kwargs['maturity_day'])),
				        term_structure_1m 	= float(self.kwargs['term_structure_1m']),
				        term_structure_3m 	= float(self.kwargs['term_structure_3m']),
				        term_structure_6m 	= float(self.kwargs['term_structure_6m']),
				        term_structure_1y 	= float(self.kwargs['term_structure_1y']),
				        term_structure_2y 	= float(self.kwargs['term_structure_2y']),
				        term_structure_3y 	= float(self.kwargs['term_structure_3y']),
				        term_structure_5y 	= float(self.kwargs['term_structure_5y']),
				        term_structure_7y 	= float(self.kwargs['term_structure_7y']),
				        term_structure_10y 	= float(self.kwargs['term_structure_10y']),
				        term_structure_20y 	= float(self.kwargs['term_structure_20y']),
				        term_structure_30y 	= float(self.kwargs['term_structure_30y']),
				        face 			= float(self.kwargs['face']),
					coupon 			= float(self.kwargs['coupon']),
					spread			= float(self.kwargs['spread'])
					)
		#Look for previous calculations
		results = Fixed_Rate_Bond.objects.filter(	payment_frequency 	= b.payment_frequency,
								valuation_date 		= b.valuation_date,
							        maturity_date 		= b.maturity_date,
							        term_structure_1m 	= b.term_structure_1m,
							        term_structure_3m 	= b.term_structure_3m,
							        term_structure_6m 	= b.term_structure_6m,
							        term_structure_1y 	= b.term_structure_1y,
							        term_structure_2y 	= b.term_structure_2y,
							        term_structure_3y 	= b.term_structure_3y,
							        term_structure_5y 	= b.term_structure_5y,
							        term_structure_7y 	= b.term_structure_7y,
							        term_structure_10y 	= b.term_structure_10y,
							        term_structure_20y 	= b.term_structure_20y,
							        term_structure_30y 	= b.term_structure_30y,
							        face 			= b.face,
								coupon 			= b.coupon,
								spread 			= b.spread
								)
		#if new instrument
		if len(results) == 0:
			if self.kwargs['spread'] != None:		
				x = bondValuation( b )
			results = []
			results.append(x)
			
		context.update({'instrument' : results[0]})	
		return context


class Equity_Option_Value_Results(ListView):
	##1) Get URL data
	##2) Check for results cached in DB
	##3) Create New Object
	##3) Calculate new results
	##4) Save down result and object
	##5) Show results
	
	model = Equity_Option
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Equity_Option_Value_Results, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		o = Equity_Option(	style 		= self.kwargs['style'],
					put_or_call 	= self.kwargs['put_or_call'],
					valuation_date 	= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
				        expiry_date 	= date(int(self.kwargs['expiry_year']),int(self.kwargs['expiry_month']),int(self.kwargs['expiry_day'])),
				        strike_price	= float(self.kwargs['strike_price']),
					underlying_price= float(self.kwargs['underlying_price']),
					interest_rate 	= float(self.kwargs['interest_rate']),
					dividend_yield 	= float(self.kwargs['dividend_yield']),
					volatility_rate	= float(self.kwargs['volatility_rate'])
					)
		#Look for previous calculations
		results = Equity_Option.objects.filter(	style 		= o.style,
							valuation_date 	= o.valuation_date,
							expiry_date 	= o.expiry_date,
							strike_price 	= o.strike_price,
							put_or_call 	= o.put_or_call,
							underlying_price= o.underlying_price,
							interest_rate 	= o.interest_rate,
							dividend_yield 	= o.dividend_yield,
							volatility_rate = o.volatility_rate
							)
		#if new instrument
		if len(results) == 0:
			if o.style == 'european':
				x = europeanValuation( o )
			else:
				x = americanValuation( o )
			results = []
			results.append(x)
	
		context.update({'instrument' : results[0]})
	
		return context
		

class Equity_Option_Calibrate_Results(ListView):
	model = Equity_Option
	
	extra_context = {}
	
	def get_context_data(self, **kwargs):
		
		context = super(Equity_Option_Calibrate_Results, self).get_context_data(**kwargs)
		context.update(self.extra_context)
		
		o = Equity_Option(	style 		= self.kwargs['style'],
					put_or_call 	= self.kwargs['put_or_call'],
					valuation_date 	= date(int(self.kwargs['valuation_year']),int(self.kwargs['valuation_month']),int(self.kwargs['valuation_day'])),
				        expiry_date 	= date(int(self.kwargs['expiry_year']),int(self.kwargs['expiry_month']),int(self.kwargs['expiry_day'])),
				        strike_price	= float(self.kwargs['strike_price']),
					underlying_price= float(self.kwargs['underlying_price']),
					interest_rate 	= float(self.kwargs['interest_rate']),
					dividend_yield 	= float(self.kwargs['dividend_yield']),
					market_value	= float(self.kwargs['market_value'])
					)
		#Look for previous calculations
		results = Equity_Option.objects.filter(	style 		= o.style,
							valuation_date 	= o.valuation_date,
							expiry_date 	= o.expiry_date,
							strike_price 	= o.strike_price,
							put_or_call 	= o.put_or_call,
							underlying_price= o.underlying_price,
							interest_rate 	= o.interest_rate,
							dividend_yield 	= o.dividend_yield,
							market_value 	= o.market_value
							)
		#if new instrument
		if len(results) == 0:
			if o.style == 'european':
				x = europeanCalibration( o )
			else:
				x = americanCalibration( o )
			results = []
			results.append(x)
	
		context.update({'instrument' : results[0]})
	
		return context