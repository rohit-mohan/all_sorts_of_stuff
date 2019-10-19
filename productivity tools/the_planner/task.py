"""
Title : Task class
Author : Rohit Mohan
Date : 18-01-2017
Version : 1.0
"""
import datetime

class Task :
	"""
		What : Generic class representing
		Why  : Tasks are the fundamental building blocks of this whole thing
	"""
	def __init__(self, step, tag, isPoW, deadline, goal = None, resources=[]):
		"""
			Parameters : 
				+ step - String mentioning the step to be taken.
				+ tag - {oneshot, routine}
				+ isPoW - Boolean flag specifying whether this task has any proof of work.
				+ deadline - the final date, after which the task is stale.
				+ goal - [Optional] the Goal object to which this task belongs.
				+ resources - [Optional] the materials required for this task.
			
			This function initialized the variables of the class.
		"""
		self.__step = step
		self.__tag = tag
		self.__deadline = deadline
		self.__resources = resources
		self.__ispow = isPoW
		
		# A location to save the proof of work (eg. link to a blog, github, where to look for weight chart etc)
		self.__pow = ""
	
	@property
	def step(self):
		return self.__step
	
	@step.setter
	def step(self, s) :
		self.__step = s
	
	@property
	def deadline(self):
		return self.__deadline
	
	@deadline.setter
	def deadline(self, d) :
		self.__deadline = d
	
	@property
	def resources(self):
		return self.__resources
	
	@resources.setter
	def step(self, r) :
		self.__resources = r
	
	@property
	def ispow(self):
		return self.__ispow
	
	@ispow.setter
	def ispow(self, i) :
		self.__ispow = i

	@property
	def pow(self):
		return self.__pow
	
	@pow.setter
	def pow(self, p) :
		self.__pow = p
	
	def __eq__(self, other) :
		if not isinstance(other, Task) : return False
		
		flag = (other.step == self.step) and\
			   (other.tag == self.tag) and\
			   (other.ispow == self.ispow) and\
			   (other.deadline == self.deadline)
		
		if flag : return True
		else : return False
	
	def __repr__(self):
		return "<\n Step : %s \n Tag : %s \n Deadline : %s \n PoW : %s\n>" % \
				(self.__step, self.__tag, self.__deadline, self.__pow)
	
	def __str__(self):
		return "<\n Step : %s \n Tag : %s \n Deadline : %s \n PoW : %s\n>"% \
				(self.__step, self.__tag, self.__deadline, self.__pow)



	
class OneShot(Task):
	"""
		What : Type of task.
		Why  : Class representing tasks to be done just once.
	"""
	def __init__(self, step, isPoW, deadline, when=None, goal = None, resources=[]):
		"""
			Parameters :
				(Most parameters are passed to the base class Task.)
				+ when - specifies when this task is scheduled in Unix time. This should always be before
						 the deadline. If not, it is automatically reset to the deadline.
		"""
		super().__init__(step, "oneshot", isPoW, deadline, goal, resources)
		self.when = when
	
	@property
	def when(self):
		return self.__when
	
	@when.setter
	def when(self, when):
		self.__when = when if when <= self.__deadline else self.__deadline
	
	def __eq__(self, other) :
		if isinstance(other, OneShot): return False
		
		flag =  (other.when == self.when) and super().__eq__(self, other)
		
		if flag : return True
		else : return False
		
	def __repr__(self):
		return super.__repr__()[:-1] + " When : %s\n>" % (str(self.__when),)
	
	def __str__(self):
		return super.__str__()[:-1] + " When : %s\n>" % (str(self.__when),)
	
	
		


	
class Routine(Task):
	"""
		What : Class representing repeated tasks.
		Why  : Simplifies manipulation of similar tasks spread out over many dates.
	"""
	
	def __init__(self, step, isPoW, deadline, whens=[], goal = None, resources=[]):
		"""
			Parameters :
				(Most parameters are passed to the base class Task.)
				+ whens - specifies when this task is repeatedly scheduled as datetime obects. This should 
						  always be before the deadline. If not, it is automatically reset to the deadline.			
		"""
		super().__init__(step, "routine", isPoW, deadline, goal, resources)
		self.__routine = whens
		
	@property
	def routine(self):
		self.__routine = sorted(self.__routine)
		return self.__routine

		
	def __add__(self, other):
		"""
			Method to add another datetime object to the routine. It will return a new Routine object if 
			the date is successfully added. Else returns the same old one.
		"""
		if isinstance(other, datetime.datetime) :
			if other not in self.__routine and other <= self.deadline: 
				return Routine(self.step, self.ispow, self.deadline, self.__routine + [other], self.resources)
			elif other > self.deadline : 
				raise ValueError("The date you are trying to add crosses the task deadline.")
			else : 
				return self
		else :
			raise TypeError("Second operand should be an instance of class datetime.datetime.")
	
	def __sub__(self, other):
		"""
			Method to remove a particular date from the routine. It will return a new Routine object if
			the date is successfully removed. Else returns the same old one.
		"""		
		if isinstance(other, datetime.datetime) :
			if other in self.__routine :
				i = self.__routine.index(other)
				temp  = self.__routine[:i] + self.__routine[i+1:]
				return Routine(self.step, self.ispow, self.deadline, temp, self.resources)
			else : return self
		else :
			raise TypeError("Second operand should be an instance of class datetime.datetime.")
	
	def __eq__(self, other):
		if not isinstance(other, Routine) : return False
		
		flag = (other.routine == self.routine) and super().__eq__(self, other)
		
		if flag : return True
		else : return False
	
	def daysFrom(self, startdate, pattern_function):
		"""
			Method to add dates to the routine based on some startdate, and a pattern of progression.
			The pattern is conveyed through the function pattern_function, which takes the startdate
			and deadline as parameters.
		"""
		whens = [startdate + datetime.timedelta(days=i) for i in pattern_function(startdate, self.deadline)]
		for w in whens : 
			try :
				self = self + w
			except ValueError as e: 
				print repr(e) + " Make sure pattern_function enforces the deadline."
		
	
	def __repr__(self):
		string = "<\n."
		string += super().__str__() + '\n.'
		
		for w in sorted(self.__routine):
			string += str(w) + '\n.'
		
		string += ">"
		
		return string

	def __str__(self):
		string = "<\n."
		string += super().__str__() + '\n.'
		
		for w in sorted(self.__routine):
			string += str(w) + '\n.'
		
		string += ">"
		
		return string




















		
	
