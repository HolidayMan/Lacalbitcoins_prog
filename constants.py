hmac_key = "c25ad1eecfdf0b49557332c396ffaad3"
hmac_secret = '9ec39c0705e6544188a72546789923b9ac140d6061dd01efb9448c25b675fe15'
class Account:
	def __init__(self, name, hmac_key, hmac_secret):
		self.name = name
		self.hmac_key = hmac_key
		self.hmac_secret = hmac_secret

