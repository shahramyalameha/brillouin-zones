import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import tkinter as Tk
import sys

matplotlib.use('TkAgg')


class BrillouinZone(object):
	d = 1;
	brillouin = 1;
	brillouinMax = 1;
	
	colors = ['red', 'green', 'blue', 'black', 'magenta', 'yellow', 'cyan'];
	
	def __init__(self, a1, a2, size):
		self.a1 = a1;
		self.a2 = a2;
		self.size = size;
		self.x = np.arange(-1 * self.size, self.size, 0.01);
		self.y = np.arange(-1 * self.size, self.size, 0.01);
		
		self.pointsX = [];
		self.pointsY = [];
		self.non = 0;
		self.distances = [];
		
		root = Tk.Tk()
		root.wm_title("Embedding in TK")
		self.f = Figure()
		self.plt = self.f.add_subplot(1, 1, 1)
		
		self.main();
		self.update();
		# a tk.DrawingArea
		self.canvas = FigureCanvasTkAgg(self.f, master=root)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		
		nextBtn = Tk.Button(master=root, text='Next', command=self.next)
		backBtn = Tk.Button(master=root, text='Back', command=self.back)
		quitBtn = Tk.Button(master=root, text='Quit', command=sys.exit)
		nextBtn.pack(side=Tk.RIGHT)
		backBtn.pack(side=Tk.RIGHT)
		quitBtn.pack(side=Tk.LEFT)
		
		Tk.mainloop()
	
	def main(self):
		for i in range(-1 * self.size, self.size + 1):
			for j in range(-1 * self.size, self.size + 1):
				self.pointsX.append(i * self.a1[0] + j * self.a2[0]);
				self.pointsY.append(i * self.a1[1] + j * self.a2[1]);
				self.non += 1;
		self.distances = self.findDistances(self.pointsX, self.pointsY);
		print("ended distances")
		self.brillouinMax = len(self.distances);
	
	def update(self):
		funcs = [];
		for i in range(0, self.brillouin):
			for j in range(0, self.non):
				if np.abs((float((self.pointsY[j] ** 2 + self.pointsX[j] ** 2)) - self.distances[i])) < 0.001:
					funcs.append(self.plot(self.pointsX[j], self.pointsY[j], i));
		self.plt.plot(self.pointsX, self.pointsY, 'ro');
		self.plt.axis([-1 * self.size + 0.2, self.size + 0.2, -1 * self.size + 0.2, self.size + 0.2]);
		print("ended plot points")
	
	def next(self):
		self.plt.clear()
		newBrillouin = self.brillouin + 1;
		if newBrillouin <= self.brillouinMax:
			self.brillouin = newBrillouin
			self.update();
			self.canvas.draw()
	
	def back(self):
		self.plt.clear()
		newBrillouin = self.brillouin - 1;
		if newBrillouin >= 0:
			self.brillouin = newBrillouin
			self.update();
			self.canvas.draw()
	
	# def increaseBrillouin(self):
	# 	newBrillouin = self.brillouin + 1;
	# 	if newBrillouin <= self.brillouinMax:
	# 		self.brillouin = newBrillouin
	#
	# def decreaseBrillouin(self):
	# 	newBrillouin = self.brillouin - 1;
	# 	if newBrillouin >= 0:
	# 		self.brillouin = newBrillouin
	
	def findDistances(self, x, y):
		distances = [0];
		for i in range(-1 * self.size, len(x)):
			for j in range(-1 * self.size, len(y)):
				dis = x[i] ** 2 + y[j] ** 2
				if self.findInArray(distances, dis) is False:
					distances.append(dis);
		distances.sort();
		distances.remove(0);
		print(distances);
		return distances;
	
	def findInArray(self, distances, dis):
		for i in range(0, len(distances)):
			if np.abs(dis - distances[i]) < 0.01:
				return True;
		return False;
	
	def plot(self, p2x, p2y, colorIndex, p1x=0, p1y=0):
		if (p2x - p1x) == 0:
			y0 = (p2y + p1y) / 2;
			y1 = self.x * 0 + y0;
			self.plt.plot(self.x, y1, lw=1, color=self.getColor(colorIndex));
			return y1;
		elif (p2y - p1y) == 0:
			x0 = (p2x + p1x) / 2;
			x1 = self.y * 0 + x0;
			self.plt.plot(x1, self.y, lw=1, color=self.getColor(colorIndex));
			return x1;
		else:
			m = (p2y - p1y) / (p2x - p1x);
			m = -1 / m;
			x0 = (p2x + p1x) / 2;
			y0 = (p2y + p1y) / 2;
			y1 = self.x * m + (-m * x0 + y0);  # y = mx + (-mx0 +y0)
			self.plt.plot(self.x, y1, lw=1, color=self.getColor(colorIndex));
			return y1;
	
	def getColor(self, colorIndex):
		index = colorIndex;
		while index >= len(self.colors):
			index = index - len(self.colors)
		return self.colors[index];


BrillouinZone([1, 0], [0, 1], 5);
# BrillouinZone([1, 0], [np.cos(np.deg2rad(60)), np.sin(np.deg2rad(60))], 6);


# minn = np.minimum(funcs[0], funcs[1]);
# minn = np.minimum(funcs[2], minn);
# minn = np.minimum(funcs[3], minn);
# minn = np.minimum(funcs[4], minn);
# minn = np.minimum(funcs[5], minn);
#
# max = np.maximum(funcs[0], funcs[1]);
# max = np.maximum(funcs[2], max);
# max = np.maximum(funcs[3], max);
# max = np.maximum(funcs[4], max);
# max = np.maximum(funcs[5], max);
#
# self.plt.fill_between(self.x, minn, max, color='grey', alpha='0.5')

# self.plt.fill_between(x, y1, y2, where=((x2 < x) & (x1 > x)), facecolor='green', alpha=0.5)

# self.plt.fill_between(x, y1, y2, where=((y1 > y4) & (y1 < y3)), facecolor='green', alpha=0.5)
# self.plt.fill_between(x, y1, y2, where=((y2 < y1) & (y1 > x)), facecolor='green', alpha=0.5)
