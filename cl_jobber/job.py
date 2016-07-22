#!/usr/bin/env python
'''
craigslist job searcher
'''
import os
import requests
from bs4 import BeautifulSoup as bs
import subprocess as sp
import sys

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

#-------- function declarations --------#

def exit():
	print; print 'Exiting...';print;sys.exit()

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

def generate_html(usa):
	html = []
	html.append(
		'''<h4 class="opt"><input type="checkbox" id="all"/>All</h4>'''
	)
	for state in sorted(usa.states):
		html.append(
			'''	<div>
					<h4 class="opt state">%s</h4>
					<div class="substates hidden">
			''' %state
		)
		for substate in sorted(usa.states[state].substates):
			html.append(
				'''		&nbsp; &nbsp;
					<div class='opt'> <input type="checkbox" class="opt sub_check" name="%s : %s" id="%s"/>
					<h5 class="opt">%s</h5> </div><br>											
				''' %(state,substate,substate.replace(' ','_').replace('/','0'),substate)
			)		
		html.append('</div></div>')

	return '\n'.join(html)

	
def get_prefs():
	if not os.path.exists('misc/prefs'):
		sp.Popen(['touch','misc/prefs'])
	return None
	
def main():
	
	cl_main = get_cl_main()
	
	cl_soup = bs(cl_main)
	
	usa = make_usa(cl_soup)
	
	prefs = get_prefs()
	
	if prefs:
		#ask user to proceed with preferences
		pass
	else:
		#if not os.path.exists('/misc/options'):			
		html = generate_html(usa)
		with open('misc/options','w') as f:
			f.write(html)
		sp.call(['python','start.py'])
		

	
if __name__ == '__main__':
	main()