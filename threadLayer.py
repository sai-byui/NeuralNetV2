import threading
import queue
import time



class layerThread(threading.Thread):
	def __init__(self, threadID, q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.q = q

	def run(self):
		print( "thread "+ str(self.threadID) + " starting" )

		total = 0

		while self.q.qsize() > 0 :
			total += self.q.get()
			time.sleep(.1)

		print("thread "+ str(self.threadID) +" got"+ str(total))



def calculateLayer(listOfNodes):

	Q = queue.Queue(101)
	threadCount = 4
	threads = []

	for x in listOfNodes:
		Q.put(x)

	# thread setup
	for t in range(threadCount):
		this_thread = layerThread(t, Q)
		threads.append(this_thread)



	# start the threads
	for x in threads:
		x.start()


	# start back up once all of these threads have finished
	for i in threads:
		i.join()

	print("*** all threads done ***")

if __name__ == "__main__":
	calculateLayer([x for x in range(100)])