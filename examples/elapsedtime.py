import time
from datetime import timedelta

start = time.time()

end = time.time()
elapsed = (end - start)

hours, rem = divmod(elapsed, 3600)
minutes, seconds = divmod(rem, 60)
mask = "{:0>2}:{:0>2}"
printableTime = "  " + mask.format(int(hours), int(minutes))

print(printableTime)
