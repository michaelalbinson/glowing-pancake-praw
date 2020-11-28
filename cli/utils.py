from cli.FLAGS import FLAG_VERBOSE, FLAG_V, FLAG_FORCE


def is_verbose(args):
	"""

	:param args: The argument array passed to a command
	:return: True if the arguments contain FLAG_VERBOSE or FLAG_V, False otherwise
	"""
	return if_present_pop(args, FLAG_VERBOSE) or if_present_pop(args, FLAG_V)


def is_forced(args):
	"""

	:param args: The argument array passed to a command
	:return: True if the arguments contain FLAG_VERBOSE or FLAG_V, False otherwise
	"""
	return if_present_pop(args, FLAG_FORCE)


def if_present_pop(args, to_pop):
	"""
	Pop the given argument from the list if it's present, otherwise do nothing
	:param args: list
	:param to_pop: string
	:return: True if the argument was present, false otherwise
	"""
	if to_pop not in args:
		return False

	args.remove(to_pop)
	return True

