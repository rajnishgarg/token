# All the logics to create TPAN, VPAN, NTT etc..

from mapping import *
import requests
import json
import logging

"""
TODO:
 1. Exception handling for each event.
 2. Add logging.
 
Open Questions:
 1. Do we need to create everytime a new user, if someone is using this?
 2. 
"""

class my_responses(object):

	def __init__(self):
		self.responses = []

responses = my_responses().responses

def call_http_post(REQUEST_INFO):

	res = None
	#Make a HTTP POST request
	try:
		r = requests.post(REQUEST_INFO.url, data=REQUEST_INFO.payload, headers= REQUEST_INFO.headers)
		if r.status_code != 200:
			raise Exception("Error HTTP Post Failed, status code: {}, payload: {} , url: {}".format(r.status_code, REQUEST_INFO.payload, REQUEST_INFO.url) ) 
		res = r
		
	except Exception, e:
		# logging.info(e)
		print("Print is:" + str(e))
		res = str(e)

	#Log to the workflow
	responses.append(res)
	return res

#TODO: Make this function more generic, **args
def __run_token(token_type, product_name, encrypt_account_id, account_number, vpan=False):
	
	REQUEST_CLASS = PRODUCT.INFO_CLASS[token_type]

	if vpan:
		request_info = REQUEST_CLASS(product_name, encrypt_account_id, account_number, vpan)
	else:
		request_info = REQUEST_CLASS(product_name, encrypt_account_id, account_number)
	r = call_http_post(request_info)

	return r

def run_ims(form):

	#responses = []
	# Get the product name from the Web Form 
	PRODUCT_NAME = form.select.data

	#Find Product Structure
	product_mapping = MAPPING_DICT[PRODUCT_NAME]
	responses.append({PRODUCT_NAME: product_mapping })
	
	########################################################################################
	# Create an account
	account_obj = call_http_post(CREATE_ACCOUNT_REQUEST())
	account_number = "" #TODO: get from the response: account_obj
	
	# Call external API call to encrypt account name
	encrypt_account_id = call_http_post(ENCRYPT_ACCOUNT_REQUEST(account_number))
	########################################################################################

	vpan = False
	MY_TOKENS = product_mapping["depedency"]
	FIRST_LEVEL_TOKEN = product_mapping['type']

	if PRODUCT.NTT in MY_TOKENS:
		r = __run_token(PRODUCT.NTT, MY_TOKENS[PRODUCT.NTT], encrypt_account_id, account_number)

	if PRODUCT.VPAN in MY_TOKENS:
		r = __run_token(PRODUCT.VPAN, MY_TOKENS[PRODUCT.VPAN], encrypt_account_id, account_number)
		vpan = True

	#It will run high level, TPAN, VPAN, NTT case
	r = __run_token(FIRST_LEVEL_TOKEN, PRODUCT_NAME, encrypt_account_id, account_number, vpan)

	return responses