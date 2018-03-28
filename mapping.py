import json, pprint

# Constant mapping file


"""
1. Make one parent request class
2. string print of the class
3. Is there any security tokens here, that needs to hide?
4. Is `X-PAYPAL-SECURITY-CONTEXT` (except 2 variable columns) same for NTT, VPAN ?

"""
class CREATE_ACCOUNT_REQUEST(object):

	def __init__(self):
		raw_payload =  {
		  "home_zip" : "95131",
		  "biz_zip" : "95134",
		  "country" : "US",
		  "currency" : "USD",
		  "home_state" : "CA",
		  "confirm_email" : True,
		  "account_type" : "BUSINESS",
		  "bank" : [ ],
		  "home_city" : "San Jose",
		  "fund" : [ ]
		}

		self.payload = json.dumps(raw_payload)
		self.headers = {'Content-Type': 'application/json', 'hostName': 'msmaster.qa.paypal.com'}
		self.url = 'http://jaws.qa.paypal.com/v1/QIJawsServices/restservices/user'


class ENCRYPT_ACCOUNT_REQUEST(object):

	def __init__(self, account_number):

		raw_payload = { 
			"id_list" : account_number, 
			"button"  : "JSON",
			"type"    : "6",
			"action"  : "enc13",
			"storage" : "N",
			"standin" : "N"
		}

		self.payload = "&".join(map(lambda item: '{}={}'.format(item[0], item[1]), raw_payload.iteritems() )) #TODO: Test it
		self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		self.url = 'http://sretools02.qa.paypal.com/cgi-bin/decrypt_adv2.py'

	

class NTT_REQUEST(object):

	def __init__(self, product_name, encrypted_account_number, account_number):
		
		## INFO:
		# wallet_id = encrypted_account_number

		self.payload = {
		  "value_to_tokenize" : "???",
		  "product_name" : product_name, 
		  "wallet_id" : encrypted_account_number,
		  "additional_attributes" : [ ]
		}

		self.headers =  {
			'Content-Type': 'application/json',

			'x-paypal-security-context': {
			  "version": "1.2",
			  "actor": {
			    "auth_claims": [
			      "CLIENT_ID_SECRET"
			    ],
			    "auth_state": "LOGGEDIN",
			    "account_number": "1949159234778201672",
			    "encrypted_account_number": "DYREUEDHL8UQS",
			    "party_id": "1949159234778201672",
			    "user_type": "API_CALLER"
			  },
			  "auth_token": "AUTHENTICATED_TOKEN_AS_RETURNED_BY_ADMINAUTHSERV",
			  "auth_token_type": "ACCESS_TOKEN",
			  "scopes": [
			    "https://uri.paypal.com/services/issuance/tokens/execute",
			    "https://uri.paypal.com/services/issuance/tokens/read",
			    "https://uri.paypal.com/services/issuance/tokens/readwrite",
			    "https://uri.paypal.com/services/wallet/card-accounts/update",
			    "*"
			  ]
			}
		}

		#TODO: Verify, if this localhost need to be converted to other prod endpoint
		self.url = 'http://localhost:8080/v1/issuance/tokens'

class VPAN_REQUEST(object):

	def __init__(self, product_name, encrypted_account_number, account_number ):

		payload = {
		  "value_to_tokenize" : "???", #TODO:
		  "product_name" : product_name,
		  "wallet_id" : encrypted_account_number,
		  "additional_attributes" : [ ]
		}

		headers = {
			'Content-Type': 'application/json',

			'x-paypal-security-context': {
			  "version": "1.2",
			  "actor": {
			    "auth_claims": [
			      "CLIENT_ID_SECRET"
			    ],
			    "auth_state": "LOGGEDIN",
			    "account_number": "9874321987548724921",
			    "encrypted_account_number": "CZ477866EEXKQ",
			    "party_id": "9874321987548724921",
			    "user_type": "API_CALLER"
			  },
			  "auth_token": "AUTHENTICATED_TOKEN_AS_RETURNED_BY_ADMINAUTHSERV",
			  "auth_token_type": "ACCESS_TOKEN",
			  "scopes": [
			    "https://uri.paypal.com/services/issuance/tokens/execute",
			    "https://uri.paypal.com/services/issuance/tokens/read",
			    "https://uri.paypal.com/services/issuance/tokens/readwrite",
			    "https://uri.paypal.com/services/wallet/card-accounts/read"
			  ],
			  "subjects": []
			}
		}

		url = 'https://msmaster.qa.paypal.com:15248/v1/issuance/tokens'


class TPAN_REQUEST(object):

	def __init__(self, product_name, encrypted_account_number, account_number, vpan=False):

		self.payload = {
		  "value_to_tokenize" : None, #F(NTT), #TODO:
		  "product_name" : product_name,
		  "issuance_funding_instrument_id" : None, #F(VPAN),
		  "additional_attributes" : [ ]
		}

		#If consumer info, if it has VPAN too.
		if vpan:  self.payload["consumer"] = { "user_id" : "??" }


		self.headers = {
			'Content-Type': 'application/json',

			'x-paypal-security-context': {
			  "version": "1.2",
			  "actor": {
			    "auth_claims": [
			      "CLIENT_ID_SECRET"
			    ],
			    "auth_state": "LOGGEDIN",
			    "account_number": "1949159234778201672",
			    "encrypted_account_number": "DYREUEDHL8UQS",
			    "user_type": "API_CALLER"
			  },
			  "auth_token": "A005",
			  "auth_token_type": "ACCESS_TOKEN",
			  "scopes": [
			    "https://uri.paypal.com/services/issuance/tokens/readwrite"
			  ],
			  "subjects": [
			    {
			      "subject": {
			        "account_number": account_number, 
			        "encrypted_account_number": encrypted_account_number,
			        "user_type": "CONSUMER"
			      },
			      "features": []
			    }
			  ]
			}
		}
		self.url = "http://localhost:8080/v1/issuance/tokens"


class PRODUCT:
	TPAN = 'TPAN'
	NTT = 'NTT'
	VPAN = 'VPAN'
	# #TODO
	# Primary = None
	# Secondary = None

	INFO_CLASS = {
		TPAN: TPAN_REQUEST,
		VPAN: VPAN_REQUEST,
		NTT : NTT_REQUEST 
	}


MAPPING_DICT = {
    
   "FACEBOOK_US_SINGLEUSETOKEN" : {
   		"type": "TPAN", 
   		"country": "US", 
   		"depedency":  { 
   			  "NTT" :  "FACEBOOKFIVAULT_US_NONTRANSACTABLETOKEN"
   		}
   		
   	},


   "FACEBOOKFIVAULT_US_NONTRANSACTABLETOKEN": {
   		"type": "NTT", 
   		"country": "US", 
   		"depedency": {}
   	}
}
