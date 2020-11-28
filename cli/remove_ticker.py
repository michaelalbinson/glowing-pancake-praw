from api.local_stocks.Ticker import Ticker

REMOVE_TICKER = 'remove-ticker'


def remove_ticker(args):
	"""
	Update the provided ticker if it already exists
	"""
	if args is None:
		args = []

	if len(args) < 1:
		print("ERROR: Please provide a ticker to remove")
		return 1

	test_ticker = args[0]
	print('Removing ticker: %s' % test_ticker)
	found_t = Ticker.get_ticker(test_ticker)
	if found_t is None:
		print("Ticker %s is not in the database. Nothing to do. Exiting." % test_ticker)
		return 0

	Ticker.delete_ticker(test_ticker)
	print("Ticker %s successfully deleted!" % test_ticker)
	return 0
