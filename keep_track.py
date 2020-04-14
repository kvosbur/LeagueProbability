import time, subprocess, datetime
str(datetime.timedelta(seconds=666))
'0:11:06'		
run = subprocess.Popen(['C:\\Python34\\python.exe', 'C:\\Users\\kevin\\Google Drive\\Programming\\Python\\round_robin.py'])
n=0
accumulator = 0
while n == 0:
	statis = run.poll()
	if statis == 0:
		n = 1
	accumulator += 1
	time.sleep(1)
	
	print('Since Start: ' + str(datetime.timedelta(seconds=accumulator)))

