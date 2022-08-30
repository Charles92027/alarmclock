from datetime import date
from datetime import timedelta

today = date.today()
firstDayOfTheYear = date(today.year, 1, 1)
lastDayOfNextYear = date(today.year + 1, 12, 31)

print(firstDayOfTheYear, " - ", lastDayOfNextYear)

theDate = firstDayOfTheYear
aDay = timedelta(days = 1)

while (theDate <= lastDayOfNextYear):
	
	theDateS = theDate.strftime("%Y-%m-%d")
	sql = "select '" + theDateS + "' theDate, STRFTIME('%w', '" + theDateS + "') theDay;"
	
	print(sql)
	
	
	theDate = theDate + aDay
	
	
	
	
