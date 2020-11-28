from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI
from api.local_stocks.TickerWrapper import TickerWrapper
from cli.utils import is_forced, is_verbose
from db.SqlExecutor import SqlExecutor
from datetime import date

UPDATE_TICKER = 'update-ticker'
UPDATE_LATENCY_DAYS = 30  # number of days to wait before refreshing a ticker's overview


def update_ticker(args):
	"""
	Update the provided ticker if it already exists
	"""
	if args is None:
		args = []

	do_forced = is_forced(args)
	do_verbose = is_verbose(args)
	if len(args) < 1:
		print("ERROR: Please provide a ticker to update")
		return 1

	ticker_to_update = args[0]
	print('Updating ticker metadata for: %s' % ticker_to_update)
	if do_forced:
		print('Doing forced update for this ticker\'s metadata...')

	found_ticker = TickerWrapper.get(ticker_to_update)
	if found_ticker is None:
		print('ERROR: The ticker %s does not exist in the database' % ticker_to_update)
		print('ERROR: If you think it should, use add-ticker to add it to the database instead!')
		return 1

	# if a ticker doesn't even have a last_updated date, just update now
	if found_ticker.last_updated is not None:
		# if the update_date is before UPDATE_LATENCY_DAYS ago, don't bother doing another update unless we're being forced
		iso_update_date = date.fromisoformat(found_ticker.last_updated).toordinal()
		if _is_before(iso_update_date, date.today().toordinal() - UPDATE_LATENCY_DAYS) and not do_forced:
			print('This ticker was updated on %s, so we won\'t update now. If an update is required, use the --force flag.' %
				  found_ticker.last_updated)
			return 0

	print('Ticker out date... updating now')
	retrieved_json = retrieve_ticker_meta(ticker_to_update)
	if retrieved_json is None:
		# retrieve_ticker_meta does the common logging for us
		return 1

	do_ticker_update(ticker_to_update, retrieved_json)
	print('Data successfully updated!')
	if do_verbose:
		TickerWrapper.get(ticker_to_update).pretty_print()


def do_ticker_update(ticker_name, ticker_json):
	update_sql_template = "UPDATE `COMPANY` " \
						  "SET NAME=?, DESCRIPTION=?, SECTOR=?, INDUSTRY=?, EMPLOYEES=?, REVENUE=?, NET_INCOME=?," \
						  "FORWARD_PE=?, TRAILING_PE=?, PRICE_TO_BOOK=?, COUNTRY=?, LAST_TARGET_PRICE=?," \
						  "RESOURCE_URL=?," \
						  "LAST_RETRIEVED=CURRENT_DATE " \
						  "WHERE TICKER=?;"

	"""`PRICE_TO_BOOK` VARCHAR(50) DEFAULT NULL,
   `COUNTRY` VARCHAR(50) DEFAULT NULL,
   `LAST_TARGET_PRICE` VARCHAR(50) DEFAULT NULL"""

	executor = SqlExecutor()
	executor.exec_insert(update_sql_template, (ticker_json.get('Name'), ticker_json.get('Description'),
													ticker_json.get('Sector'), ticker_json.get('Industry'),
													ticker_json.get('FullTimeEmployees'),
													ticker_json.get('RevenueTTM'),
													ticker_json.get('GrossProfitTTM'),
													ticker_json.get('ForwardPE'),
													ticker_json.get('TrailingPE'),
													ticker_json.get('PriceToBookRatio'),
													ticker_json.get('Country'),
													ticker_json.get('AnalystTargetPrice'),
													ticker_json.get('resource_url'), ticker_name))
	executor.close()


def retrieve_ticker_meta(ticker_name):
	retrieved_json = AlphaVantageAPI().get_overview(ticker_name)
	if retrieved_json is None:
		print('ERROR: Failed to retrieve data for the ticker %s' % ticker_name)
		print('ERROR: Please check that the ticker name is correct and retry.')
		return None

	return retrieved_json


def _is_before(date1, date2):
	return date1 >= date2
