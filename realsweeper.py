import realgrid, time, ImageGrab, useful, mousemacro, random

def isNumber(c):
	return c not in ("0", "#", "B", "?", "X")

for i in range(0, 100):
	clicked = []
	marked = []	
	time.sleep(2)
	g = realgrid.grid(16, 40, [7,7])

	time.sleep(1)
	g.readGrid()

	while 1:
		oldstate = g.outputGrid()
		for y in range(0, 16):
			for x in range(0, 16):
				#if isNumber(g.getAt(x,y,False)):
				
				d = g.outputGrid([x-1,x+1,y-1,y+1])
				if isNumber(d[(y!=0)][(x!=0)]): #If our location is a number, count surrounding unknowns and bombs
					nunknown = 0
					adjmines = 0
					for l in d:
						for c in l:
							if c=="#":
								nunknown+=1
							if c=="B":
								adjmines+=1
					if adjmines == int(d[(y!=0)][(x!=0)]) and nunknown!=0: #All of the mines for this square found, double click it
						if [x,y] not in clicked:
							g.doubleClick(x,y)
							clicked.append([x,y])
							g.sleep(0.05)
							mousemacro.move(0,0)
						#g.readGrid()
						
					elif nunknown+adjmines == int(d[(y!=0)][(x!=0)]): #We can mark all of the adjacent unknowns as mines
						for iy in range(0,len(d)):
							for ix in range(0, len(d[iy])):
								if d[iy][ix] == "#":
									if [ix+x-(x!=0), iy+y-(y!=0)] not in marked:
										g.mark(ix+x-(x!=0), iy+y-(y!=0), True)
										g.sleep(0.05)
										mousemacro.move(0,0)
										marked.append([ix+x-(x!=0), iy+y-(y!=0)])
										#g.readGrid()
		g.readGrid()
		if g.getUnmarked() <= 0:
				#won+=1
			print "Game won! Cleaning up..."
			w = g.outputGrid()
			clpos = [] #Places we need to click before the game knows that we won
			for y in range(0, len(w)):
				for x in range(0, len(w[y])):
					if w[y][x] == "#":
						clpos.append([x,y])
			for p in clpos:
				g.click(p[0], p[1], True)
				g.sleep(0.05)
			g.sleep(1)
			g.click(0,0, True)
			g.sleep(1)
			g.endGame()
			break
			
		for p in marked:
			if g.outputGrid()[p[1]][p[0]] != "B":
				g.mark(p[0], p[1], True)
				g.markedMines -= 1
		
		g.readGrid()
		if oldstate == g.outputGrid():
			print "STALE!"
			print g.sleeptime
			#print "No progress made, trying some elimination"
			#incomplete += 1
			w = g.outputGrid()
			poss = []
			for y in range(0, len(w)):
				for x in range(0, len(w[y])):
					if isNumber(w[y][x]):
						for ix in range(useful.clamp(x-1,0,g.dim),useful.clamp(x+2,0,g.dim)):
							for iy in range(useful.clamp(y-1,0,g.dim),useful.clamp(y+2,0,g.dim)):
								if w[iy][ix] == "#" and [ix,iy] not in poss:
									poss.append([ix,iy])			
			
			if len(poss) == 0:
				#print "No unknowns bordering numbers, reasoning impossible"
				poss = []
				for y in range(0, len(w)):
					for x in range(0, len(w[y])):
						if w[y][x] == "#":
							poss.append([x,y])
				if len(poss)==g.getUnmarked():
					#print "All unmarked are bombs"
					for p in poss:
						g.mark(p[0],p[1], True)
						g.sleep(0.05)
						mousemacro.move(0,0)
						marked.append([p[0],p[1]])
				else:
					print "Trying a random guess"
					guess = random.choice(poss)
					try:
						g.click(guess[0], guess[1], False)
					except realgrid.clickedMine:
						print "Guessed a mine, game lost with "+str(g.getUnmarked()) + " mines left"
						mousemacro.move(830, 610)
						mousemacro.click()
						break
			else:
				#print "Checking all "+str(len(poss))+" guesses"
				foundClick = False
				for p in poss:
					tg = w[:]
					tg[p[1]]=tg[p[1]][:p[0]]+"B"+tg[p[1]][p[0]+1:]
					#print "Trying at: "+str(p)
					old = ""
					while old != tg and not foundClick:
						old=tg[:]
						#for i in tg:
						#	print i
						#print
						for y in range(0, len(tg)):
							for x in range(0, len(tg[y])):
								if isNumber(tg[y][x]):
									bpos = []
									upos = []
									for ix in range(useful.clamp(x-1,0,g.dim),useful.clamp(x+2,0,g.dim)):
										for iy in range(useful.clamp(y-1,0,g.dim),useful.clamp(y+2,0,g.dim)):
											if tg[iy][ix] == "B":
												bpos.append([ix,iy])
											elif tg[iy][ix] == "#":
												upos.append([ix,iy])
									#print str(bpos)+"="+str(len(bpos))
									#print str(upos)+"="+str(len(upos))
									if len(bpos) > int(tg[y][x]): 
										print "Overbombed number found, clicking initial guess"
										g.click(p[0],p[1], False)
										foundClick = True
										break
									if len(bpos) == int(tg[y][x]): #Found all of the bombs, delete the rest
										for up in upos:
											tg[up[1]]=tg[up[1]][:up[0]]+"X"+tg[up[1]][up[0]+1:]
									if len(bpos)+len(upos) == int(tg[y][x]): #The number of unknowns matches the middle number, we can mark them all
										for up in upos:
											tg[up[1]]=tg[up[1]][:up[0]]+"B"+tg[up[1]][up[0]+1:]
									if int(tg[y][x]) > len(upos)+len(bpos): #Not enough spots to get all the bombs in
										print "Unsatisfiable number found, clicking initial guess"
										g.click(p[0],p[1], False)
										foundClick = True
										break
					print "No change"
					if foundClick:
						break
				if not foundClick:
					print "Elimination logic found nothing new, randomly guessing"
					poss = []
					for y in range(0, len(w)):
						for x in range(0, len(w[y])):
							if w[y][x] == "#":
								poss.append([x,y])
					if len(poss)==g.getUnmarked():
						print "All unmarked are bombs"
						for p in poss:
							g.mark(p[0],p[1], True)
							g.sleep(0.05)
							mousemacro.move(0,0)
							marked.append([p[0],p[1]])
					else:
						print "Trying a random guess"
						guess = random.choice(poss)
						try:
							g.click(guess[0], guess[1], False)
						except realgrid.clickedMine:
							print "Guessed a mine, game lost with "+str(g.getUnmarked()) + " mines left"
							mousemacro.move(830, 610)
							mousemacro.click()
							break