#!/usr/local/bin/python3

"""
Entry point for the `cli` package, contains methods for performing administrative tasks on the database, and maybe more
in the future!
"""

from cli.ticker_exists import TICKER_EXISTS, ticker_exists
from cli.add_ticker import ADD_TICKER, add_ticker
from cli.remove_ticker import REMOVE_TICKER, remove_ticker
from cli.update_ticker import UPDATE_TICKER, update_ticker
from cli.show_financials import SHOW_FINANCIALS, show_financials
from sys import argv


if len(argv) <= 1:
	print("Error: too few arguments provided.")
	exit(1)

# execute the command and then exit with the returned status code
status_code = 0
command = argv[1]
remaining_args = argv[2:]
if command == TICKER_EXISTS:
	status_code = ticker_exists(remaining_args)
elif command == ADD_TICKER:
	status_code = add_ticker(remaining_args)
elif command == REMOVE_TICKER:
	status_code = remove_ticker(remaining_args)
elif command == UPDATE_TICKER:
	status_code = update_ticker(remaining_args)
elif command == SHOW_FINANCIALS:
	status_code = show_financials(remaining_args)
else:
	print('ERROR: command "' + command + '" not found')
	status_code = 1

exit(status_code)