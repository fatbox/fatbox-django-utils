#
# Retrieved from http://stackoverflow.com/a/6574789 March 31st, 2013
# Updated to use Django translation functions and return strings by Evan
#

from django.utils.translation import ugettext as _
from django.utils.translation import ungettext as __

INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
UNITS = ["seconds", "minutes", "hours", "days", "weeks", "months", "years"]
NAMES = [
    (_('%d second'), _('%d seconds')),
    (_('%d minute'), _('%d minutes')),
    (_('%d hour'), _('%d hours')),
    (_('%d day'), _('%d days')),
    (_('%d week'), _('%d weeks')),
    (_('%d month'), _('%d months')),
    (_('%d year'), _('%d years'))
]

def humanize_time(amount, units):
    '''
    Divide `amount` in time periods.
    Useful for making time intervals more human readable.

    >>> humanize_time(173, "hours")
    u'1 week, 5 hours'
    >>> humanize_time(17313, "seconds")
    u'4 hours, 48 minutes, 33 seconds'
    >>> humanize_time(5400, "seconds")
    u'1 hour, 30 minutes'
    >>> humanize_time(90, "weeks")
    u'1 year, 10 months, 2 weeks'
    >>> humanize_time(42, "months")
    u'3 years, 6 months'
    >>> humanize_time(500, "days")
    u'1 year, 5 months, 3 weeks, 3 days'
    '''
    result = []

    unit = map(lambda a: a, UNITS).index(units)

    # Convert to seconds
    amount = amount * INTERVALS[unit]

    for i in range(len(NAMES)-1, -1, -1):
        a = amount / INTERVALS[i]
        if a > 0:
            result.append(NAMES[i][1 % a] % a)
            amount -= a * INTERVALS[i]

    return ", ".join(result)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
