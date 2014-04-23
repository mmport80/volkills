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
from django.db import models


class CDS(models.Model):
        valuation_date 			= models.DateField()
        maturity_date 			= models.DateField()
	
	contract_spread 		= models.FloatField()
	
	nominal 			= models.FloatField()
	
        market_value 			= models.FloatField(null=True)
        default_probability		= models.FloatField(null=True)
	
        term_structure_1m 		=  models.FloatField()
        term_structure_3m 		=  models.FloatField()
        term_structure_6m 		=  models.FloatField()
        term_structure_1y 		=  models.FloatField()	
        term_structure_2y 		=  models.FloatField()
        term_structure_3y 		=  models.FloatField()
        term_structure_5y 		=  models.FloatField()
        term_structure_7y 		=  models.FloatField()
        term_structure_10y 		=  models.FloatField()
        term_structure_20y 		=  models.FloatField()
        term_structure_30y 		=  models.FloatField()

        result_npv 			= models.FloatField(null=True)
	result_coupon_leg_bps 		= models.FloatField(null=True)
	result_fair_spread		= models.FloatField(null=True)
	result_default_leg_npv		= models.FloatField(null=True)
	result_coupon_leg_npv 		= models.FloatField(null=True)
	result_running_spread 		= models.FloatField(null=True)
	result_implied_hazard_rate 	= models.FloatField(null=True)


        def sanity_check(self):#use this to calc npv...
                return self.val_date < self.expiry_date

        def __unicode__(self):  # Python 3: def __str__(self):
                return str(self.pk)



class IRS(models.Model):
        valuation_date = models.DateField()
        maturity_date = models.DateField()
        start_date = models.DateField()
	
	fixed_rate = models.FloatField()
	spread = models.FloatField()
	
	face = models.FloatField()
	
        market_value = models.FloatField(null=True)
        credit_spread = models.FloatField(null=True)
	
        term_structure_1m =  models.FloatField()
        term_structure_3m =  models.FloatField()
        term_structure_6m =  models.FloatField()
        term_structure_1y =  models.FloatField()	
        term_structure_2y =  models.FloatField()
        term_structure_3y =  models.FloatField()
        term_structure_5y =  models.FloatField()
        term_structure_7y =  models.FloatField()
        term_structure_10y =  models.FloatField()
        term_structure_20y =  models.FloatField()
        term_structure_30y =  models.FloatField()

        reference_index_term_structure_1m =  models.FloatField()
        reference_index_term_structure_3m =  models.FloatField()
        reference_index_term_structure_6m =  models.FloatField()
        reference_index_term_structure_1y =  models.FloatField()
        reference_index_term_structure_2y =  models.FloatField()
        reference_index_term_structure_3y =  models.FloatField()
        reference_index_term_structure_5y =  models.FloatField()
        reference_index_term_structure_7y =  models.FloatField()
        reference_index_term_structure_10y =  models.FloatField()
        reference_index_term_structure_20y =  models.FloatField()
        reference_index_term_structure_30y =  models.FloatField()

        fixed_leg_frequency_choice = (
		('once','Once'),
		('annual','Annual'),
		('semiannual','Semiannual'),
		('quarterly','Quarterly'),
		('bimonthly','Bimonthly'),
		('monthly','Monthly'),
		('weekly','Weekly'),
		('daily','Daily')
		)

        fixed_leg_frequency =  models.CharField(max_length=10,choices=fixed_leg_frequency_choice)
	
        floating_leg_frequency_choice = (
		('once','Once'),
		('annual','Annual'),
		('semiannual','Semiannual'),
		('quarterly','Quarterly'),
		('bimonthly','Bimonthly'),
		('monthly','Monthly'),
		('weekly','Weekly'),
		('daily','Daily')
		)

        floating_leg_frequency =  models.CharField(max_length=10,choices=floating_leg_frequency_choice)

        result_npv = models.FloatField(null=True)
	result_fixed_leg_bps = models.FloatField(null=True)
	result_floating_leg_bps = models.FloatField(null=True)
	result_fair_rate = models.FloatField(null=True)
	result_fair_spread = models.FloatField(null=True)

        result_spread = models.FloatField(null=True)
        result_duration = models.FloatField(null=True)
        result_convexity = models.FloatField(null=True)
	result_clean_price = models.FloatField(null=True)
	result_bps = models.FloatField(null=True)
	result_basis_pt_value = models.FloatField(null=True)
	result_yield_value_bp = models.FloatField(null=True)

        def sanity_check(self):#use this to calc npv...
                return self.val_date < self.expiry_date

        def __unicode__(self):  # Python 3: def __str__(self):
                return str(self.pk)



class FRN(models.Model):	
        valuation_date = models.DateField()
        maturity_date = models.DateField()
        face = models.FloatField()

        term_structure_1m =  models.FloatField()
        term_structure_3m =  models.FloatField()
        term_structure_6m =  models.FloatField()
        term_structure_1y =  models.FloatField()	
        term_structure_2y =  models.FloatField()
        term_structure_3y =  models.FloatField()
        term_structure_5y =  models.FloatField()
        term_structure_7y =  models.FloatField()
        term_structure_10y =  models.FloatField()
        term_structure_20y =  models.FloatField()
        term_structure_30y =  models.FloatField()

        reference_index_term_structure_1m =  models.FloatField()
        reference_index_term_structure_3m =  models.FloatField()
        reference_index_term_structure_6m =  models.FloatField()
        reference_index_term_structure_1y =  models.FloatField()
        reference_index_term_structure_2y =  models.FloatField()
        reference_index_term_structure_3y =  models.FloatField()
        reference_index_term_structure_5y =  models.FloatField()
        reference_index_term_structure_7y =  models.FloatField()
        reference_index_term_structure_10y =  models.FloatField()
        reference_index_term_structure_20y =  models.FloatField()
        reference_index_term_structure_30y =  models.FloatField()


        payment_frequency_choice = (
		('once','Once'),
		('annual','Annual'),
		('semiannual','Semiannual'),
		('quarterly','Quarterly'),
		('bimonthly','Bimonthly'),
		('monthly','Monthly'),
		('weekly','Weekly'),
		('daily','Daily')
		)

        payment_frequency =  models.CharField(max_length=10,choices=payment_frequency_choice)


	current_floating_rate = models.FloatField(null=True)
	spread = models.FloatField(null=True)
	
	credit_spread = models.FloatField(null=True)
        market_value = models.FloatField(null=True)

        result_npv = models.FloatField(null=True)
	result_clean_price = models.FloatField(null=True)
	result_bps = models.FloatField(null=True)
	result_basis_pt_value = models.FloatField(null=True)
	result_yield_value_bp = models.FloatField(null=True)
        result_spread = models.FloatField(null=True)
        result_yield_to_maturity = models.FloatField(null=True)
        result_accrued = models.FloatField(null=True)

        def sanity_check(self):#use this to calc npv...
                return self.val_date < self.expiry_date

        def __unicode__(self):  # Python 3: def __str__(self):
                return str(self.pk)


class Equity_Option(models.Model):

	style_choice = (('american','european'),('american','european'))
	put_or_call_choice = (('call','call'),('put','put'))
	
	
	#terms and conditions
	style =  models.CharField(max_length=8,choices=style_choice)
	valuation_date = models.DateField()
	expiry_date = models.DateField()
	strike_price =  models.FloatField()
	put_or_call =  models.CharField(max_length=4,choices=put_or_call_choice)


	#market data
	underlying_price = models.FloatField()
	interest_rate =  models.FloatField()
	dividend_yield =  models.FloatField()
	
	#either or
	market_value = models.FloatField(null=True)
	volatility_rate =  models.FloatField(null=True)


	result_delta = models.FloatField(null=True)
	result_gamma = models.FloatField(null=True)
	result_vega = models.FloatField(null=True)
	result_rho = models.FloatField(null=True)
	result_dividend_rho = models.FloatField(null=True)
	result_theta = models.FloatField(null=True)
	result_theta_per_day = models.FloatField(null=True)
	result_strike_sensitivity = models.FloatField(null=True)
	result_npv = models.FloatField(null=True)
	result_implied_volatility = models.FloatField(null=True)

	#not used right now
	result_itmCashProbability = models.FloatField(null=True)
	result_deltaForward = models.FloatField(null=True)
	result_elasticity = models.FloatField(null=True)



	def sanity_check(self):#use this to calc npv...
		return self.val_date < self.expiry_date
	
	def __unicode__(self):  # Python 3: def __str__(self):
		return str(self.pk)
		
		

class Fixed_Rate_Bond(models.Model):	
        valuation_date = models.DateField()
        maturity_date = models.DateField()
        face = models.FloatField()

        term_structure_1m =  models.FloatField()
        term_structure_3m =  models.FloatField()
        term_structure_6m =  models.FloatField()
        term_structure_1y =  models.FloatField()	
        term_structure_2y =  models.FloatField()
        term_structure_3y =  models.FloatField()
        term_structure_5y =  models.FloatField()
        term_structure_7y =  models.FloatField()
        term_structure_10y =  models.FloatField()
        term_structure_20y =  models.FloatField()
        term_structure_30y =  models.FloatField()

        payment_frequency_choice = (	('once','Once'),
					('annual','Annual'),
					('semiannual','Semiannual'),
					('quarterly','Quarterly'),
					('bimonthly','Bimonthly'),
					('monthly','Monthly'),
					('weekly','Weekly'),
					('daily','Daily')
					)

        payment_frequency 	= models.CharField(max_length=10,choices=payment_frequency_choice)

	coupon 			= models.FloatField(null=True)
	
        market_value 		= models.FloatField(null=True)
	spread 			= models.FloatField(null=True)

        result_npv 		= models.FloatField(null=True)
        result_spread 		= models.FloatField(null=True)
        result_duration 	= models.FloatField(null=True)
        result_convexity 	= models.FloatField(null=True)

	result_clean_price 	= models.FloatField(null=True)
	result_bps 		= models.FloatField(null=True)
	result_basis_pt_value 	= models.FloatField(null=True)
	result_yield_value_bp 	= models.FloatField(null=True)

        result_yield_to_maturity = models.FloatField(null=True)
	

        result_accrued_amount = models.FloatField(null=True)


        def sanity_check(self):#use this to calc npv...
                return self.val_date < self.expiry_date

        def __unicode__(self):  # Python 3: def __str__(self):
                return str(self.pk)