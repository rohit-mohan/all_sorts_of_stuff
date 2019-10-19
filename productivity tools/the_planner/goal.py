"""
Description : The Goal class, which is a collection of tasks, with a deadline
Author : Rohit Mohan
Date : 29-1-18
Version : 1.0
"""
from task import *

class Goal :
	def __init__(what, why, deadline, tasks):
		self.what = what
		self.why = why
		self.deadline = deadline
		self.__tasks = tasks
	
	def __add__(self, other):
		if isinstance(other, Task) :
			if other.deadline <= self.deadline :
				return Goal(self.what, self.why, self.deadline, self.__tasks + [other])
			else : 
				raise ValueError("The deadline of the Task should not go beyond the deadline of the Goal")
		else :
			raise TypeError("Second operand should be an instance of Task")
	
	def __sub__(self, other):
		if isinstance(other, Task) : 
			if other in self.__tasks :
				i = self.__tasks.index(other)
				tasks = self.__tasks[:i] + self.__task[i+1 : ]
				return Goal(self.what, self.why, self.deadline, tasks)
			
			else : 
				return self 
			
		else :
			raise TypeError("Second operand should be an instance of Task")
