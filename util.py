from datetime import date
from datetime import timedelta


def addYears(theDate, years):

	newDate = theDate

	try:
		newDate = theDate.replace(year = theDate.year + years)

	except ValueError:
		newDate = theDate + (date(theDate.year + years, 1, 1) - date(theDate.year, 1, 1))
		
	return newDate
