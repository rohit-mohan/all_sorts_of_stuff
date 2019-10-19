from tinydb import TinyDB, Query
from os.path import isfile
from warnings import warn

class TimerDB:
	def __init__(self, db_file = None):
		self.sessionEntryFields = ['Start Day Name',
							'Start Day',
							'Start Month',
							'Start Year',
							'Start Hour',
							'Start Minute',
							'Start Second',
							'End Day Name',
							'End Day',
							'End Month',
							'End Year',
							'End Hour',
							'End Minute',
							'End Second',
							'Duration',
							'Project']
		
		self.projectOutputFields = ['Name',
									'Total Time',
									'Avg Time Per Month',
									'Avg Time Per Day',
									'Avg Timer Hour']
		
		self.totalWorkOutputFields = ['Total Time',
									'Avg Time Per Month',
									'Avg Time Per Day',
									'Avg Timer Hour']
		
		self.dbFile = db_file
		if db_file :
			self.db = TinyDB(db_file)


	def setDBFile(self, b_file):
		self.dbFile = db_file
		if db_file :
			self.db = TinyDB(db_file)
	
	def storeSessionEntry(self, entry):
	
		for field in self.sessionEntryFields :
			if field not in entry:
				warn('Bad entry. Could not find the field : %s' % (field))
				return
				
		self.db.insert(entry)
	
	def getProjectSummary(self, projectName) :
		projectOutput = {'Name' : projectName}
		#projectOutput['Start Date'] = self.getStartDate(projectData)
		#projectOutput['End Date'] = self.getEndDate(projectData)
		projectOutput['Total Time'] = self.getTotalTime(projectName)
		projectOutput['Avg Time Per Month'] = self.getAvgTimePerMonth(projectName)
		projectOutput['Avg Time Per Day'] = self.getAvgTimePerDay(projectName)
		projectOutput['Avg Time Per Hour'] = self.getAvgTimerPerHour(projectName)
	
		return projectOutput
	
	def getTotalSummary(self):
		totalOutput = {}
		totalOutput['Total Time'] = self.getTotalTime()
		totalOutput['Avg Time Per Month'] = self.getAvgTimePerMonth()
		totalOutput['Avg Time Per Day'] = self.getAvgTimePerDay()
		totalOutput['Avg Time Per Hour'] = self.getAvgTimerPerHour()
	
		return totalOutput	
	
	def getTotalTime(self, name=None):
		
		if name:
			sessions = Query()
			data = self.db.search(sessions['Project'] == name)
		else:
			data = self.db.all()
		
		sec = 0 
		for d in data :
			sec = sec + int(d['Duration'])
			
		return sec
	
	def getAvgTimerPerMonth(self, name=None):
		months = {'January' : 0,
					'February' : 0,
					'March' : 0,
					'April' : 0,
					'May' : 0,
					'June' : 0,
					'July' : 0,
					'August' : 0,
					'September' : 0,
					'October' : 0,
					'November' : 0,
					'December' : 0}
		
		for month in months.keys():
		
			sessions = Query()
			if name :
				data = self.db.search((sessions['Project'] == name) & (sessions['Start Month'] == month))
			else :
				data = self.db.search((sessions['Start Month'] == month))
		
			sec = 0
			for d in data :
				sec = sec + int(d['Duration'])
			
			months[month] = sec
		
		return months
	
	def getAvgTimerPerDay(self, name=None):
		days = {'Saturday' : 0,
					'Sunday' : 0,
					'Monday' : 0,
					'Tuesday' : 0,
					'Wednesday' : 0,
					'Thursday' : 0,
					'Friday' : 0}
		
		for day in days.keys():
		
			sessions = Query()
			if name :
				data = self.db.search((sessions['Project'] == name) & (sessions['Start Day Name'] == day))
			else :
				data = self.db.search((sessions['Start Day Name'] == day))
		
			sec = 0
			for d in data :
				sec = sec + int(d['Duration'])
			
			days[day] = sec
		
		return days	
		
	def getAvgTimerPerHour(self, name=None):
		hours = {}
		for i in xrange(24) :
			hours[str(i)] = 0
		
		for hour in hours.keys():
		
			sessions = Query()
			if name :
				data = self.db.search((sessions['Project'] == name) & (sessions['Start Hour'] == hour))
			else :
				data = self.db.search((sessions['Start Hour'] == hour))
		
			sec = 0
			for d in data :
				sec = sec + int(d['Duration'])
			
			hours[hour] = sec
		
		return hours
	

	
	
	
	
