from api.local_stocks.Ticker import Ticker
import json


class TickerWrapper:
	"""
	A wrapper for the Company DB Table so that the fields of the table can be comprehensively interacted with
	"""
	def __init__(self, db_object):
		self.ticker = db_object[0]
		self.name = db_object[1]
		self.description = db_object[2]
		self.industry = db_object[3]
		self.sector = db_object[4]
		self.revenue = db_object[5]
		self.gross_income = db_object[6]
		self.employees = db_object[7]
		self._resource_url = db_object[8]
		self.last_updated = db_object[9]
		self.asset_class = db_object[10]
		self.forward_pe = db_object[11]
		self.trailing_pe = db_object[12]
		self.price_to_book = db_object[13]
		self.country = db_object[14]
		self.last_target_price = db_object[15]

	@staticmethod
	def get(ticker):
		db_ticker = Ticker().get_ticker(ticker)
		if db_ticker is None:
			return None

		return TickerWrapper(db_ticker)

	@staticmethod
	def resolve_pretty_number(to_resolve):
		"""
		Pretty print the provided number in 100s, k, Ms, or Bs depending on the magnitude
		:param to_resolve:
		:return:
		"""
		if to_resolve is None or to_resolve == '-':
			return "Not Found"

		try:
			num = int(to_resolve)
		except ValueError:
			return to_resolve

		magnitude = abs(num)
		if magnitude > 10**9:
			return "%.2fB" % (num / 10 ** 9)
		elif magnitude > 10**6:
			return "%.2fM" % (num / 10 ** 6)
		elif magnitude > 10**3:
			return "%.2fk" % (num / 10 ** 3)
		else:
			return str(num)

	def to_json(self):
		return json.dumps({
			'ticker': self.ticker,
			'Name': self.name,
			'Description': self.description,
			'Industry': self.industry,
			'Sector': self.sector,
			'Revenue': self.resolve_pretty_number(self.revenue),
			'Gross Income': self.resolve_pretty_number(self.gross_income),
			'Employees': self.resolve_pretty_number(self.employees),
			'Asset Class': self.asset_class,
			'Forward PE': self.forward_pe,
			'Trailing PE': self.trailing_pe,
			'Price-to-Book': self.price_to_book,
			'Country': self.country,
			'Analyst Price Target': self.last_target_price,
			'Last Updated': self.last_updated
		})

	def pretty_print(self):
		"""
		Print metadata about a ticker in a nice tabular format
		:return: None
		"""
		print('')
		print('| - ------------ | ------------------------------------------------')
		print('| - Ticker       | %s' % self.ticker)
		print('| - ------------ | ------------------------------------------------')
		print('| - Company Name | %s' % self.name)
		print('| - Industry     | %s' % self.industry)
		print('| - Sector       | %s' % self.sector)
		print('| - Asset Class  | %s' % self.asset_class)
		print('| - Country      | %s' % self.country)
		print('| - Employees    | %s' % self.resolve_pretty_number(self.employees))
		print('| - Last updated | %s' % self.last_updated)
		print('| - Description  | %s' % self.description)

	def pretty_print_financials(self):
		print('')
		print('| - -------------- | ------------------------------------------------')
		print('| - Ticker         | %s' % self.ticker)
		print('| - -------------- | ------------------------------------------------')
		print('| - Company Name   | %s' % self.name)
		print('| - Forward PE     | %s' % self.forward_pe)
		print('| - Trailing PE    | %s' % self.trailing_pe)
		print('| - Price to Book  | %s' % self.price_to_book)
		print('| - Analyst Target | %s' % self.name)
		print('| - Last updated   | %s' % self.last_updated)
		print('| - Revenue        | %s' % self.resolve_pretty_number(self.revenue))
		print('| - Net Income     | %s' % self.resolve_pretty_number(self.gross_income))
