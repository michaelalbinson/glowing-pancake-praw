from api.local_stocks.TickerWrapper import TickerWrapper

SHOW_FINANCIALS = 'show-financials'


def show_financials(args=None):
	"""

	"""
	if args is None:
		args = []

	if len(args) < 1:
		print("ERROR: Please provide a ticker to search for")
		return 1

	test_ticker = args[0]
	print('Showing ticker: ' + test_ticker)
	found_ticker = TickerWrapper.get(test_ticker)
	if found_ticker is None:
		print('Ticker %s could not be found in the database. Exiting.' % test_ticker)
		return 0

	found_ticker.pretty_print_financials()

	return 0
