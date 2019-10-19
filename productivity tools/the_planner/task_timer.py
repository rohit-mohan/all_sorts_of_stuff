"""
Description : A timer that times in pomodoro style. Also each pomodoro can be
			  associated with a task. 
Author : Rohit Mohan
Date : 27-1-18
Version : 1.0
"""
import threading


class TaskTimer :
	"""
		What : Class for pomodoro timer logic.
		Why : To time work done towards each task
	"""
	def __init__(self, duration, task, logger):
		"""
			Parameters : 
				+ duration - duration of a pomodoro (work slice) in minutes.
				+ task - the task associated with this work slice. 
				+ logger - a function which takes the current TaskTimer class object
							as a parameter and logs details.
		"""
		self.__duration = duration
		self.__task = task
		self.logger = logger
		
		# Flag to show timer is busy
		self.__isBusy = False 
		# Placeholder for threading.Timer object
		self.__t = None
		# Time elapsed in minutes
		self.__elapsed = 0
	
	### Start bunch of get and set methods for the member variables ###
	@property
	def duration(self):
		return self.__duration
	
	@duration.setter
	def duration(self, d):
		self.__duration = d

	@property
	def task(self):
		return self.__task
	
	@task.setter
	def task(self, t):
		self.__task = t

	@property
	def isBusy(self):
		return self.__isBusy
	
	@isBusy.setter
	def isBusy(self, i):
		pass
	
	@property
	def elapsed(self):
		return self.__elapsed
	
	@elapsed.setter
	def elapsed(self, e):
		pass
	
	### Stop bunch of get and set methods for the member variables ###
	
	def timer_cleanup(self) :
		"""
			Method to clean up the Timer instance, and to show timer is not busy and
			reset elapsed time.
		"""
		self.__t = None
		self.__isBusy = False
		self.elapsed = 0
	
	
	def timer_callback(self):
		"""
			Callback for Timer instance. This method allows us to have a minute by 
			minute update of the time elapsed since timer started. It repeatedly calls 
			the Timer instance's start() function until the duration is elapsed.
			
			Cancelation of the timer before the alloted duration is handled by the 
			cancel_timer() method of this TaskTimer class.
		"""
		self.__elapsed += 1
		
		print("Time elapsed : ", self.elapsed)
		
		if self.__elapsed >= self.__duration :
			self.logger(self)
			self.timer_cleanup()
		
		else :
			self.start_timer()	
		
		
	def start_timer(self):
		"""
			Method to start the timer. It allocates a new Timer instance and calls it's 
			start method. It also sets the isBusy flag to let users know the timer is 
			busy.
		"""
		self.__t = threading.Timer(60, self.timer_callback)
		self.__isBusy = True
		self.__t.start()
		
		
	def cancel_timer(self):
		"""
			Method to cancel the timer and cleanup outdated timer info.
		"""
		print("Cancelling timer.")
		
		self.__t.cancel()
		self.timer_cleanup()
	
	### String representation of class instance ###
	def __repr__(self):
		string = "<\n"
		print("Duration : ", self.duration)
		print("Task : ", self.task)
		string += ">"
		
		return string	

	def __str__(self):
		string = "<\n"
		print("Duration : ", self.duration)
		print("Task : ", self.task)
		string += ">"
		
		return string			
	
	###############################################
