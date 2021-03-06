#Small parser for the COVID-19 data provided by the JHU: https://github.com/CSSEGISandData/COVID-19

#Please make sure your local COVID-19 data repository is cloned to the same parent directory in which this repo is located. 

import datetime
from numpy import array

def parse(which=None):
	path='./../COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
	fname='time_series_covid19_*_global.csv'
	if which==None:
		which='confirmed'
	f=path+fname.replace('*',which)
	data={}
	try:
		fl=open(f,'r')
		header=True
		for line in fl:
			if '\"' in line:
				#fix South Korea...
				line=fix_comma_in_name(line)
			d=line.split(',')
			d[-1]=d[-1].strip('\n')
			if header:
				dates=[]
				for date in d[4:]:
					m,d,y=date.split('/')
					dates.append(datetime.date(int(y),int(m),int(d)))
				data['dates']=array(dates)
				header=False
			else:
				province=d[0]
				region=d[1]
				lat=d[2]
				lon=d[3]
				#print d
				N_t=[float(val) for val in d[4:]]
				if region in data.keys():
					data[region]+=array(N_t)
				else:
					data[region]=array(N_t)
		fl.close()
		return data
	except Exception as e:
		print('Failed to load data!')
		import traceback
		traceback.print_exc()


def fix_comma_in_name(line):
	line=list(line)
	i=0
	while line[i]!='\"':
		i+=1
	j=len(line)-1
	while line[j]!='\"':
		j-=1
	for k in range(i,j):
		if line[k]==',':
			line[k]='_'
	return ''.join(line)


def parse_pop():
	def fix_comma(l):
		remove=[]
		for i in range(len(l)):
			try:
				l[i]=int(l[i])
			except:
				if l[i]!='':
					remove.append(i)
				else:
					l[i]=None
		for i in remove:
			l.pop(i)
		return l
	fname='./Population_per_Country_2020.csv'
	data={}
	try:
		fl=open(fname,'r')
		header=4
		i=0
		for line in fl:
			if i<header:
				pass
			elif i==header:
				key='years'
				line=line.replace('\"','')
				d=line.split(',')
				data[key]=d[4:-2]
			else:
				line=line.replace('\"','')
				d=line.split(',')
				key=d[0]
				l=d[5:-2]
				l=fix_comma(l)
				data[key]=l
			i+=1
		fl.close()
		return data
	except Exception as e:
		print('Failed to load data!')
		import traceback
		traceback.print_exc()


