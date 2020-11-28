from api.local_stocks.TickerWrapper import TickerWrapper
from cli.utils import is_verbose

TICKER_EXISTS = 'ticker-exists'


def ticker_exists(args=None):
	"""
	Check if the specified ticker exists in the current local db, if yes, say so and optionally print more information
	"""
	if args is None:
		args = []

	do_verbose = is_verbose(args)
	if len(args) < 1:
		print("ERROR: Please provide a ticker to search for")
		return 1

	test_ticker = args[0]
	print('Received ticker: ' + test_ticker)
	if len(test_ticker) > 6:
		print('ERROR: The input ' + test_ticker + ' could not be interpreted as a ticker. '
												  'Please try again and pass a ticker name.')
		return 1

	found_ticker = TickerWrapper.get(test_ticker)
	if found_ticker is None:
		print('Ticker %s could not be found in the database. Exiting.' % test_ticker)
		return 0

	print('Found "%s - %s" in the database' % (found_ticker.ticker, found_ticker.name))
	if do_verbose:
		found_ticker.pretty_print()

	return 0
