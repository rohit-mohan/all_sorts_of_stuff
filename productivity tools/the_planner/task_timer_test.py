from task_timer import TaskTimer
import time

def test_logger(tt) :
	print("Duration : ", tt.duration)
	print("Task : ", tt.task)
	print("Completed 1 Work Slice")


tt = TaskTimer(5, "Physics", test_logger)
tt.start_timer()
time.sleep(60*3)
tt.cancel_timer()
