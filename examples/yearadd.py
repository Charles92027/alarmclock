import datetime
from datetime import date

def addYears(d, years):
	try:
		return d.replace(year = d.year + years)

	except ValueError:
		#If not same day, it will return other, i.e.  February 29 to March 1 etc
		return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def addYearx(d, years):
	return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))




print(addYears(datetime.date(2015,8,12), -1))
print(addYears(datetime.date(2015,1,1), 1))
print(addYears(datetime.date(2015,9,12), 2))
print(addYears(datetime.date(2000,2,29),1))


print(addYearx(datetime.date(2015,8,12), -1))
print(addYearx(datetime.date(2015,1,1), 1))
print(addYearx(datetime.date(2015,9,12), 2))
print(addYearx(datetime.date(2000,2,29),1))




