import os
import os.path
import sys




def  listZones():

	import os
	tz = os.popen("cd /usr/share/zoneinfo/posix && find * -type f -or -type l | sort").read()
	timeZones = tz.split('\n')
	print(timeZones)


def main(argv):

	listZones()

	tzname = os.environ.get('TZ')
	if tzname:
		print("tzname:", tzname)
	elif os.path.exists('/etc/timezone'):
		print("file:", open('/etc/timezone').read())
	else:
		sys.exit(1)

if __name__ == '__main__':
	main(sys.argv)

