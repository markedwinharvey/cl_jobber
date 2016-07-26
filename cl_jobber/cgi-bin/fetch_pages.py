#!/usr/bin/env python
import requests
import cgi
import json
from bs4 import BeautifulSoup as bs
import sys
import os
print
#-------- class declarations --------#
class nation():
	def __init__(self,name):
		self.name=name
		self.states = {}	

class state():
	def __init__(self,name,nation):
		self.name=name
		self.substates = {}
		self.nation = nation

class substate():
	def __init__(self,name,url):
		self.name=name
		self.url=url
		

def get_cl_main():
	if not os.path.exists('misc/cl_main.html'):
		r = requests.get('https://www.craigslist.org/about/sites')
		page=r.text
		if not os.path.exists('misc'):
			os.makedir('misc')
		with open('misc/cl_main.html','w') as f:
			f.write(page)
	else:		
		with open('misc/cl_main.html','r') as f:
			page = f.read()
	return page

def make_usa(soup):
	usa = nation('United States')
	state_dat = soup.find('h1').find_next('div').contents

	for section in state_dat:
		this_section = bs(str(section))
		state_list = [bs(str(x)).get_text() for x in this_section.find_all('h4')]
		substate_list = [bs(str(x)).find_all('li') for x in this_section.select('h4 ~ ul')]
		for iter in range(len(state_list)):
			st = state(name=state_list[iter],nation=usa)
			usa.states[state_list[iter]] = st
			for each_subst in substate_list[iter]:
				subst = each_subst.find('a')
				url = 'https:'+str(subst.get('href'))
				if not url.endswith('org/'):
					continue
				sub_name = subst.get_text()
				subst = substate(url=url,name=sub_name)
				st.substates[sub_name] = subst
	return usa

def main():
	cl_main = get_cl_main()
	
	cl_soup = bs(cl_main)
	
	usa = make_usa(cl_soup)
	
	if len(sys.argv) > 2:
		prefs = []
		for selection in json.loads(sys.argv[1]):
			sel = selection.split(':')
			state = sel[0][:-1]
			substate = sel[1][1:]
			prefs.append(state+','+substate)
		prefs = '\n'.join(prefs)
		with open('misc/prefs','w') as f:
			f.write(prefs)
		
	
	
	#substate_list = []
	#for substate in sys.argv[1]:
	#	substate_list.append(substate.replace('0','/').replace('_',' '))
	
	#things = '\n'.join(sys.argv)
	#with open('fetch_shit','w') as f:
	#	f.write(things)
	
	'''
	data = cgi.FieldStorage()['package'].value
	data = json.loads(data)
	
	new_data = []
	for entry in data:
		entry = entry.replace('0','/').replace('_',' ')
		new_data.append(entry)
	new_data = '\n'.join(new_data)
	
	
	
	'''
	
	
	
	
	
	#with open('fetch_data','w') as f:
	#	f.write(new_data)


	try:
		sys.stdout.close()
	except:
		pass
	try:
		sys.stderr.close()
	except:
		pass
	pass
if __name__ == '__main__':
	main()