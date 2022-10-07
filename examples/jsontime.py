from datetime import datetime

now = datetime.now()

theTime = now.strftime("%H:%M:%S")
t = {"time": theTime}
d = {"now": now.strftime("%Y-%m-%d %H:%M:%S")}
print (t)
print (d)


