from api.local_stocks.Ticker import Ticker
from api.local_stocks.TickerWrapper import TickerWrapper
from cli.utils import is_verbose, if_present_pop
from cli.FLAGS import FLAG_FORCE
from cli.update_ticker import do_ticker_update, retrieve_ticker_meta

ADD_TICKER = 'add-ticker'
FLAG_FUND = '--fund'
FLAG_STOCK = '--stock'


def add_ticker(args=None):
	if args is None:
		args = []

	do_verbose = is_verbose(args)
	do_forced = if_present_pop(args, FLAG_FORCE)
	if len(args) < 2:
		print("ERROR: Please provide a ticker and a ticker class to add")
		return 1

	new_ticker = args[0]
	print('Received ticker: ' + new_ticker)
	ticker = Ticker.get_ticker(new_ticker)

	# check if the ticker exists at all, and if it does, if the name field has been set
	if not do_forced:
		if ticker is not None and ticker[1] is not None:
			print('The ticker "%s - %s" is already present in the database. No need to add again. Exiting.' % (ticker[0], ticker[1]))
			return 0

	if do_forced:
		print('Doing forced update for this ticker\'s metadata...')

	is_fund = if_present_pop(args, FLAG_FUND)
	is_stock = if_present_pop(args, FLAG_STOCK)
	if not is_fund and not is_stock:
		print('ERROR: Could not determine if the ticker is an ETF or a stock. Please use the --fund or --stock flags to')
		print('    indicate which it is and retry.')
		return 1

	# then nicely ask AlphaVantage about the ticker (don't do this too often)
	retrieved_json = retrieve_ticker_meta(new_ticker)
	if retrieved_json is None:
		# retrieve_ticker_meta does the common logging for us
		return 1

	# insert the ticker and asset class into the database if it wasn't there already
	if ticker is None:
		Ticker.insert_new_ticker(new_ticker, Ticker.STOCK if is_stock else Ticker.FUND)

	do_ticker_update(new_ticker, retrieved_json)

	print('Successfully added %s to the database!' % (new_ticker,))
	if do_verbose:
		TickerWrapper.get(new_ticker).pretty_print()

	return 0
