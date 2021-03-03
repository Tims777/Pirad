def parse_change(args):
    """
        Tries to parse a tuple of the form (operation, value).

        Valid operations are +, - and =
        :returns: a tuple of the form (relative, difference) so that the new value can be obtained by:
            relative * old_value + difference
        :raises: IndexError if args is not a 2-tuple
        :raises: ValueError if args[0] is not a valid operation or args[1] is not a valid int
    """
    diff = int(args[1])
    if args[0] == '+':
        return 1, diff
    elif args[0] == '-':
        return 1, -diff
    elif args[0] == '=':
        return 0, diff
    else:
        raise ValueError('Invalid operation: ' + args[0])


def clamp(x, min, max):
    """
        Implementation of a clamp-function.

        :returns: the value x if it is within the given min/max-range.
            If not min or max are returned respectively.
    """
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x
