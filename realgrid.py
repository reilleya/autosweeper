import useful, random, os, ImageGrab, mousemacro, time, SendKeys

class clickedMine(Exception):
	pass

def average(image):
	d = image.getdata()
	tot = [0,0,0]
	n = image.size[0]*image.size[1]
	for x in range(0, image.size[0]):
		for y in range(0, image.size[1]):
			for c in range(0, 3):
				tot[c]+=d[(image.size[0]*y)+x][c]
	#print tot
	return [tot[0]/n, tot[1]/n, tot[2]/n]

def variance(image):
	d = image.getdata()
	tot = [0,0,0]
	aver = average(image)
	n = image.size[0]*image.size[1]
	for x in range(0, image.size[0]):
		for y in range(0, image.size[1]):
			for c in range(0, 3):
				tot[c]+=(d[(image.size[0]*y)+x][c]-aver[c])**2
	return [(tot[0]/n)**0.5,(tot[1]/n)**0.5,(tot[2]/n)**0.5]
	
def testZero(image):
	return sum(variance(image.crop([8,8,43,43])))<27
	
def testOne(image):
	c = image.getpixel((28,28))
	return c[2] > c[1]+c[0]

def testTwo(image):
	c = [image.getpixel((36,20)),image.getpixel((26,20))]
	return c[0][1]>c[0][0]+c[0][2] and c[1][0]+c[1][1]+c[1][2]>520
	
def testThree(image):
	c = [image.getpixel((23,11)),image.getpixel((23,27)),image.getpixel((23,42)),image.getpixel((34,20))]
	out = 1
	for p in range(0, len(c)):
		out*=(c[p][0]>3*(c[p][1]+c[p][2]))
	return out
	
def testFour(image):
	c = [image.getpixel((34,10)),image.getpixel((18,34)),image.getpixel((34,42))]
	out = 1
	for p in range(0, len(c)):
		out*=(c[p][2]>3*(c[p][0]+c[p][1]))
	return out
	
def testFive(image):
	c = [image.getpixel((34,12)),image.getpixel((22,12)),image.getpixel((21,20)),image.getpixel((21,42))]
	out = 1
	for p in range(0, len(c)):
		out*=(c[p][0]>3*(c[p][1]+c[p][2]))
	return out
	
def testSix(image):
	c = [image.getpixel((23,17)),image.getpixel((37,33)),image.getpixel((29,43))]
	out = 1
	for p in range(0, len(c)):
		out*=(abs(c[p][0]+c[p][1]-c[p][2])<10)
	return out
	
def testFlag(image):
	c = [image.getpixel((16,15)),image.getpixel((26,10)),image.getpixel((26,20))]
	out = 1
	for p in range(0, len(c)):
		out*=(c[p][0]>210)
	return out

class grid():
	def __init__(self, size, mines, firstguess=None, verbose = False):
		self.nmines = mines
		self.markedMines = 0
		self.dim = size
		self.sleeptime = 0
		os.startfile("D:/Programming Projects/Python/minesweeper/Minesweeper/MineSweeper.exe")
		self.grid = []
		time.sleep(3)
		self.readGrid()
		
		if firstguess != None:		
			self.click(firstguess[0], firstguess[1], False)
	
	def readGrid(self):
		tests = {1:testOne, 2:testTwo, 3:testThree, 4:testFour, 5:testFive, 6:testSix, "B":testFlag, 0:testZero} #move dis
		mousemacro.move(0,0)
		#print "\n\n\n\n\n"
		screen = ImageGrab.grab()
		imdata = screen.getdata()
		#self.markedMines = 0
		won = True
		for point in ([820,430],[1080,430],[1080,600],[820,600]):
			for c in range(0,3):
				won *= (imdata[(point[1]*screen.size[1])+point[0]][c]==240)
		if won:
			print "YOU WON!"
		else:
			self.grid = []
			sm = screen.crop([547,128,1374,955])
			xstarts = [0,51,103,155,206,258,310,361,413,466,517,569,621,672,724,776]
			xsizes = [51,52,52,51,52,52,51,52,53,51,52,52,51,52,52,51]
			ystarts = [0,51,103,155,206,258,310,362,413,466,518,569,621,673,724,776]
			ysizes = [51,52,52,51,52,52,52,51,53,52,51,52,52,51,52,52]
			
			for y in range(0,16):
				self.grid.append([])
				for x in range(0, 16):
					#print "X: "+str(x)+", Y: "+str(y)
					name = "#"
					b = sm.crop([xstarts[x], ystarts[y], xstarts[x]+xsizes[x], ystarts[y]+ysizes[y]])
					b = b.resize([51,51])
					#v = variance(b.crop([8,8,43,43]))
					#print "\t"+str(v)+"--->"+str(sum(v))
					for lab in tests:
						if name == "#" and tests[lab](b):
							name = lab
							if lab == "B":
								pass
								#self.markedMines+=1
					#b = b.filter(ImageFilter.FIND_EDGES)
					self.grid[-1].append(name)
					#b.save("boxes/"+str(y)+"-"+str(x)+"-"+str(name)+".png")
			print "\n\n\n"
			self.draw()
	
	def outputGrid(self, sec = None):
		out = []
		if sec == None:
			sec = [0,self.dim,0,self.dim]
		else:
			sec[1]+=1
			sec[3]+=1 #Ugly range() hack
		for i in range(0, 4):
			sec[i] = useful.clamp(sec[i],0,self.dim)
		for y in range(sec[2],sec[3]):
			out.append("")
			for x in range(sec[0],sec[1]):
				out[-1]+=str(self.grid[y][x])
		return out
		
	def getUnmarked(self):
		return self.nmines-self.markedMines
		
	def draw(self, rev=False):
		d = self.outputGrid()
		mod = ""
		for line in d:
			for letter in line:
				mod += letter + " "
			mod+="\n"
		print mod
		print "Unmarked mines:"+str(self.nmines-self.markedMines)
	
	def click(self, x, y, won): #Returns True if you are still alive. False if not...
		mousemacro.move(546+(52*x)+26, 127+(52*y)+26)
		mousemacro.click()
		if not won:
			self.sleep(0.1)
			mousemacro.move(50,50)
			mousemacro.click()
			screen = ImageGrab.grab()
			imdata = screen.getdata()
			if imdata[925+(480*1920)][0] == 240 and imdata[925+(480*1920)][1] == 240 and imdata[925+(480*1920)][2] == 240:
				raise clickedMine("Tried to click a mine!") #Make a specific error maybe?
				return False
			
	def doubleClick(self, x, y):
		mousemacro.move(546+(52*x)+26, 127+(52*y)+26)
		mousemacro.click()
		self.sleep(0.1)
		mousemacro.click()
	
	def mark(self, x, y, m): #Mark as either a bomb (m=True), a possible bomb (m=False), or clear the current mark (m=None)
		mousemacro.move(546+(52*x)+26, 127+(52*y)+26)
		mousemacro.rightclick()
		self.markedMines += 1
			
	def getAt(self, x, y):
		return grid[y][x]
		
	def getRange(self, xstart, xend, ystart, yend, data): #Return an array of getAt results
		pass
		
	def getAdjacent(self, x, y):
		pass
		
	def sleep(self, stime):
		self.sleeptime += stime
		time.sleep(stime)
		
	def exit(self):
		mousemacro.move(1892,6)
		mousemacro.click()
		
	def endGame(self):
		mousemacro.move(875,630)
		mousemacro.click()