#!/usr/bin/env python
import subprocess as sp
import time
import webbrowser as wb

def main():
	
	try:
		cmd = 'python server.py &'.split()
		sp.Popen(cmd)
		time.sleep(.5)	
		
		#cmd = 'open -a firefox http://localhost:8000/cl_jobber'.split()
		#change to open in alternate browser
		#sp.Popen(cmd)
		
		
		wb.open('http://localhost:8000/cl_jobber')
		
		
		
		
		
		
		#pid = sp.Popen(cmd,stdout=sp.PIPE).communicate()[0]	
		#with open('pid','w') as f:
	#		f.write(pid)
		#print 'start finished'
	except:
		time.sleep(.5)
		print 'Cannot start server.'
		
		
if __name__ == '__main__':
	main()

