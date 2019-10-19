#!/usr/bin/python
from gi.repository import Gtk, GObject
from datetime import datetime as dt
from time import strftime
from os import path
import cPickle as pkl
from database import TimerDB

class MainAppWindow(Gtk.Window):
	
	
	def __init__(self, stat_file = 'stats.db', setting_file = 'settings.pkl'):
		self.dataBase = TimerDB(stat_file)
		self.settingFile = setting_file
		
		# Timer variables
		self.numSessionsDone = 0
		self.timerID = 0
		
		# Session variables
		self.startTime = dt.now()
		self.sessionInfo ={'Start Day Name' : None,
							'Start Day' : None,
							'Start Month' : None,
							'Start Year' : None,
							'Start Hour' : None,
							'Start Minute' :None,
							'Start Second' : None,
							'End Day Name' : None,
							'End Day' : None,
							'End Month' : None,
							'End Year' :  None,
							'End Hour' : None,
							'End Minute' : None,
							'End Second' :  None,
							'Duration' : None,
							'Project' : None}
		
		self.settingHolder = {'Study Interval' : {'Hours' : 0, 'Minutes' :  0,'Seconds' : 5},
							'Short Break' : {'Hours' : 0, 'Minutes' :  0,'Seconds' : 0},
							'Long Break' : {'Hours' : 0, 'Minutes' :  0,'Seconds' : 0},
							'Sessions / Unit' : {'Number' : 0}}
		self.importSettings()
		
		
		# Project variables
		self.projectList = {'Project' : {'Hours' : 0, 'Minutes' :  0,'Seconds' : 0}, 
							'Physics' :{'Hours' : 0, 'Minutes' :  0,'Seconds' : 0}, 
							'Maths' : {'Hours' : 0, 'Minutes' :  0,'Seconds' : 0}}
		self.projectNames = self.projectList.keys()
		self.curProject = self.projectNames[0]
		
		
		
		Gtk.Window.__init__(self, title="TimerApp")
		self.set_border_width(10)
		
		# Main box
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
		self.add(box)

		# Stack
		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack.set_transition_duration(500)
		
		# Stack Page 1 : Project info
		projectBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		
		taskHeading = Gtk.Label('Choose a task to do  : ')
		projectBox.pack_start(taskHeading, False, True, 0)
		
		projectStore = Gtk.ListStore(str)
		for project in self.projectNames :
			projectStore.append([project])
		
		self.comboBox = Gtk.ComboBox.new_with_model(projectStore)
		self.comboBox.connect("changed", self.projectComboCallBack)
		self.comboBox.set_active(0)
		rendererText = Gtk.CellRendererText()
		self.comboBox.pack_start(rendererText, True)
		self.comboBox.add_attribute(rendererText, "text", 0)
		projectBox.pack_start(self.comboBox, False, True, 0)
		
		self.projectLabel = Gtk.Label("Total time spent on task : %10d : %02d : %02d" % (0, 0, 0))
		projectBox.pack_start(self.projectLabel, False, True, 0)
		
		self.sessionsLabel = Gtk.Label("Number of sessions completed : %s" %( str(self.numSessionsDone) ) )
		projectBox.pack_start(self.sessionsLabel, False, True, 0)
		
		stack.add_titled(projectBox, "task", "Task")
		
				
		# Stack Page 2 : Timer
		timerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.timerButton = Gtk.ToggleButton.new_with_label("Timer On/Off")
		self.timerButton.connect("toggled", self.timerButtonCallBack)
		self.timeLabel = Gtk.Label("START TIMER")
		timerBox.pack_start(self.timerButton, False, True, 0)
		timerBox.pack_start(self.timeLabel, True, True, 0)
		stack.add_titled(timerBox, "timer", "Timer")
		

		# Stack Page 3 : Settings
		settingGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
		settingGrid.set_row_spacing(20)
		settingGrid.set_column_spacing(1)
		
		rowHeadings = ['Study Interval']#, 'Short Break', 'Long Break', 'Sessions / Unit']
		colHeadings = ['Hours', 'Minutes', 'Seconds']
		
		count = 1
		for string in rowHeadings:
			label = Gtk.Label(string)
			settingGrid.attach(label, 0, count, 2, 1)
			count = count + 1
		
		count = 0
		for string in colHeadings:
			label = Gtk.Label(string)
			settingGrid.attach(label, count+2, 0, 1, 1)
			count = count + 1
		
		self.settingSpinButtons = {}
		for j,prop in zip(range(3), rowHeadings) :
			tempList = {}
			for i,sec in zip(range(3), colHeadings) :
				adjustment = Gtk.Adjustment(0, 0, 59, 1, 10, 0)
				spinButton = Gtk.SpinButton()
				spinButton.set_adjustment(adjustment)
				spinButton.set_value(0)
				tempList[sec] = spinButton
				settingGrid.attach(spinButton, i+2, j+1, 1, 1)
			
			self.settingSpinButtons[prop] = tempList

		"""
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		spinButton = Gtk.SpinButton()
		spinButton.set_adjustment(adjustment)
		spinButton.set_value(0)
		self.settingSpinButtons['Sessions / Unit'] = {'Number' : spinButton}
		settingGrid.attach(spinButton, 2, 4, 3, 1)
		"""
		
		self.updateButton = Gtk.Button('Update')
		self.updateButton.connect("clicked", self.updateSettingCallBack)
		settingGrid.attach(self.updateButton, 3, 5, 2, 1)
		
		stack.add_titled(settingGrid, "settings", "Settings")
		
		# Fill main box
		stack_switcher = Gtk.StackSwitcher()
		stack_switcher.set_stack(stack)
		box.pack_end(stack_switcher, True, True, 0)
		box.pack_end(stack, True, True, 0)
	
	def importSettings(self):
		if path.isfile(self.settingFile):
			with open(self.settingFile, 'rb') as f:
				self.settingHolder = pkl.load(f)
			print "Loaded settings"

	def exportSettings(self):
		with open(self.settingFile, 'wb') as f:
			pkl.dump(self.settingHolder, f)
		print "Saved settings"	
	
		
	def updateInfo(self):
		project = self.curProject
		
		# Update Sessions
		self.numSessionsDone = self.numSessionsDone + 1
		self.sessionsLabel.set_label( "Number of sessions completed : %02d" %(self.numSessionsDone) )
		
		# Update Projects 
		oldTime = self.projectList[project]['Hours'] * 3600 + self.projectList[project]['Minutes'] * 60 + self.projectList[project]['Seconds']
		hours, minutes, seconds = sec2HrMinSec(self.sessionInfo['Duration'] + oldTime)
		self.projectLabel.set_label("Total time spent on task : %10d : %02d : %02d" % (hours, minutes, seconds))
		
		# Update database
		self.dataBase.storeSessionEntry(self.sessionInfo)
	
	def startTimer(self):
		self.comboBox.set_sensitive(False)
		self.updateButton.set_sensitive(False)
		
		self.timeLabel.set_label("%02d : %02d : %02d" % (0, 0, 0))
		
		self.startTime = dt.now()
		self.timerID  = GObject.timeout_add(1000, self.updateTimer)
		
		self.sessionInfo['Start Day Name'] = strftime("%A")
		self.sessionInfo['Start Day'] = self.startTime.day
		self.sessionInfo['Start Month'] = self.startTime.month
		self.sessionInfo['Start Year'] = self.startTime.year
		self.sessionInfo['Start Hour'] = self.startTime.hour
		self.sessionInfo['Start Minute'] = self.startTime.minute
		self.sessionInfo['Start Second'] = self.startTime.second
		
		
		
		
	def stopTimer(self):
		GObject.source_remove(self.timerID)
		
		n = dt.now()
		self.sessionInfo['End Day Name'] = strftime("%A")
		self.sessionInfo['End Day'] = n.day
		self.sessionInfo['End Month'] = n.month
		self.sessionInfo['End Year'] = n.year
		self.sessionInfo['End Hour'] = n.hour
		self.sessionInfo['End Minute'] = n.minute
		self.sessionInfo['End Second'] = n.second
		self.sessionInfo['Duration'] = (n - self.startTime).seconds
		self.sessionInfo['Project'] = self.curProject
		
		self.timeLabel.set_label("TIMER STOPPED")
		
		self.updateButton.set_sensitive(True)
		self.comboBox.set_sensitive(True)
	
	def updateTimer(self):
		seconds = (dt.now() - self.startTime).seconds
		hours, minutes, seconds = sec2HrMinSec(seconds)
		
		condition = (seconds == self.settingHolder['Study Interval']['Seconds']) and \
					(minutes ==  self.settingHolder['Study Interval']['Minutes']) and \
					(hours == self.settingHolder['Study Interval']['Hours'])
		
		if condition:
			self.timerButton.set_active(False)
			self.updateInfo()
		
		else :
			self.timeLabel.set_label("%02d : %02d : %02d" % (hours, minutes, seconds))
			
			return True
	
	def timerButtonCallBack(self, timerButton):
		#  this takes 2 args: (how often to update in millisec, the method to run)
		if timerButton.get_active() == True:
			self.startTimer()
		else :
			self.stopTimer()
	
	
	def updateSettingCallBack(self, updateButton):
		for outKey in self.settingSpinButtons.keys():
			for inKey in self.settingSpinButtons[outKey].keys():
				self.settingHolder[outKey][inKey] = self.settingSpinButtons[outKey][inKey].get_value_as_int()
	
	def projectComboCallBack(self, combo):
		treeIter = combo.get_active_iter()
		if treeIter != None:
			model = combo.get_model()
			self.curProject = model[treeIter][0]
		print "current project : ", self.curProject
	
	def quitApp(self, widget, event):
		#self.exportSettings()
		print "Quiting"
		Gtk.main_quit()

	
def sec2HrMinSec(seconds):
	hours = seconds / 3600
	seconds = seconds % 3600
	minutes = seconds / 60
	seconds = seconds % 60

	return hours, minutes, seconds
		
	
win = MainAppWindow()
win.connect("delete-event", win.quitApp)
Gtk.Window.set_default_size(win, 300, 100)
win.show_all()

Gtk.main()
