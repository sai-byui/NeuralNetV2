import threading
import queue
import time



class layerThread(threading.Thread):
	def __init__(self, threadID, q, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.q = q
		self.name = name

	def run(self):
		if self.name != "":
			print(self.name + " standing by")
		else:
			print("Thread "+ self.threadID + " Starting")

		time.sleep(10)

		print(self.name + " starting attack run")

		time.sleep(5)

		if self.name == "jar jar binks":
			print("Meesa coming home")
		else:
			print(self.name + "coming home safely")



def calculateLayer():

	Q = queue.Queue()
	threadCount = 4
	threads = []
	names = ["red leader", "blue leader", "gold leader", "jar jar binks"]

	# thread setup
	for t in range(threadCount):
		this_thread = layerThread(t, Q, names[t] )
		this_thread.start()
		time.sleep(2)



if __name__ == "__main__":
	calculateLayer()