import matplotlib.pyplot as plt

def plotGraph(mineDensity, avgScore):
	'''
	mineDensity: x-axis, avgScore: y-axis
	'''
	fig = plt.figure()
	plt.plot(mineDensity, avgScore)
	plt.xlabel('Mine Density')
	plt.ylabel('Average Score')
	plt.title('avgScore vs mineDensity')
	plt.show()


#mineDensity = [10,20,30,40,50]
#avgScore = [1,0.7,0.5,0.3,0.2]
#plotGraph(mineDensity, avgScore)