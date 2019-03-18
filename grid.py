import useful, random

class clickedMine(Exception):
	pass

class grid():
	def __init__(self, size, mines, firstguess=None, verbose = False):
		self.verbose = verbose
		self.nmines = mines
		self.dim = size
		self.field = []
		self.revealed = []
		self.marks = []
		self.adjacent = []
		self.markedMines = 0
		self.fillOut()
		if firstguess != None:
			while self.field[firstguess[1]][firstguess[0]] or self.calcAdjacent(firstguess[0],firstguess[1])!=0:
				self.fillOut()
			
		for y in range(0, self.dim): #For speeeed
			self.adjacent.append([])
			for x in range(0, self.dim):
				self.adjacent[-1].append(self.calcAdjacent(x,y))
	
		if firstguess != None:		
			self.click(firstguess[0], firstguess[1])
	
	def fillOut(self):
		#print "Generating!"
		self.field = []
		self.revealed = []
		self.marks = []
		for row in range(0, self.dim):
			self.field.append([])
			self.revealed.append([])
			self.marks.append([])
			for col in range(0, self.dim):
				self.field[-1].append(False)
				self.revealed[-1].append(False)
				self.marks[-1].append(None)
		#Populate it with mines
		for b in range(0, self.nmines):
			px = random.randint(0,self.dim-1)
			py = random.randint(0,self.dim-1)
			while self.field[py][px]:
				px = random.randint(0,self.dim-1)
				py = random.randint(0,self.dim-1)
			self.field[py][px] = True
		
	def outputGrid(self, rev, sec = None):
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
				if rev:
					if self.field[y][x]:
						out[-1]+="X"
					else:
						out[-1]+="0"
				else:
					if self.revealed[y][x]:
						out[-1]+=str(self.getAdjacent(x,y))
					else:
						if self.marks[y][x]!=None:
							out[-1]+=("B"*self.marks[y][x])+("?"*(not self.marks[y][x]))
						else:
							out[-1]+="#"
				#out[-1]+=" "
		return out
		
	def getUnmarked(self):
		return self.nmines-self.markedMines
		
	def draw(self, rev=False):
		d = self.outputGrid(rev)
		mod = ""
		for line in d:
			for letter in line:
				mod += letter + " "
			mod+="\n"
		print mod
		print "Unmarked mines:"+str(self.nmines-self.markedMines)
	
	def click(self, x, y): #Returns True if you are still alive. False if not...
		if self.verbose:
			print "Clicking on ("+str(x)+","+str(y)+"), which is"+((not self.field[y][x])*" not")+" a mine."
		if not self.field[y][x]:
			self.revealed[y][x]=True
			if self.getAdjacent(x,y) == 0:
				for ix in range(useful.clamp(x-1,0,self.dim),useful.clamp(x+2,0,self.dim)):
					for iy in range(useful.clamp(y-1,0,self.dim),useful.clamp(y+2,0,self.dim)):
						if not (ix==x and iy==y):
							if not self.revealed[iy][ix]:
								if self.getAdjacent(ix, iy) == 0:
									self.click(ix,iy)
								else:
									if not self.field[iy][ix]:
										self.revealed[iy][ix] = True
			else:
				self.revealed[y][x] = True
			return True
		else:
			raise clickedMine("Tried to click a mine!") #Make a specific error maybe?
			return False
			
	def doubleClick(self, x, y):
		if self.verbose:
			print "Doubleclicking on ("+str(x)+","+str(y)+"), which is surrounded by "+str(self.getAdjacent(x,y))+" mines"
		nmarked = 0
		part = self.outputGrid(False, [x-1,x+1,y-1,y+1])
		for p in part: #Loop through to find all mines
			for l in p:
				if l == "B":
					nmarked += 1
		if nmarked == self.getAdjacent(x,y):
			for ix in range(useful.clamp(x-1,0,self.dim),useful.clamp(x+2,0,self.dim)):
				for iy in range(useful.clamp(y-1,0,self.dim),useful.clamp(y+2,0,self.dim)):
					if not (ix==x and iy==y):
						if not self.revealed[iy][ix] and self.marks[iy][ix] == None:
							out = self.click(ix, iy)
							if not out:
								return False
		return True
	
	def mark(self, x, y, m): #Mark as either a bomb (m=True), a possible bomb (m=False), or clear the current mark (m=None)
		if not self.revealed[y][x]:
			if self.marks[y][x] and not m: #If they mark something that they had marked a mine as not a mine
				self.markedMines -= 1 #Remove one from the tally
			if not self.marks[y][x] and m: #If marking a non-marked as bomb square as a bomb, add one to the tally
				self.markedMines += 1
			self.marks[y][x] = m
			if self.verbose:
				print "Marking ("+str(x)+","+str(y)+") as "+str(m)
		else:
			raise Exception #THIS IS GROSS. NO NO NO. CUSTOM EXCEPTIONS PLEASE!
			
	def getAt(self, x, y, rev): #Return just a single tile of the grid. Less expensive?
		if rev:
			if self.field[y][x]:
				return "X"
			else:
				return "0"
		else:
			if self.revealed[y][x]:
				return str(self.getAdjacent(x,y))
			else:
				if self.marks[y][x]!=None:
					return ("B"*self.marks[y][x])+("?"*(not self.marks[y][x]))
				else:
					return "#"
		
	def getRange(self, xstart, xend, ystart, yend, data): #Return an array of getAt results
		pass
	
	
	def getAdjacent(self, x, y):
		return self.adjacent[y][x]
	
	def calcAdjacent(self, x, y):
		num = 0
		for ix in range(useful.clamp(x-1,0,self.dim),useful.clamp(x+2,0,self.dim)):
			#print ix
			for iy in range(useful.clamp(y-1,0,self.dim),useful.clamp(y+2,0,self.dim)):
				#print "\t"+str(iy)
				if not (ix==x and iy==y):
					if self.field[iy][ix]:
						num += 1
		return num