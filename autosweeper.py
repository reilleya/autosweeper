import grid, useful, random, sys, datetime

size = 16
nmines = 40
games = 1000

lost = 0
incomplete = 0
won = 0

def isNumber(c):
	return c not in ("0", "#", "B", "?", "X")
	
def satisfiable(subset, pos):
	nposs = 0
	nbombs = 0
	for y in range(0, len(subset)):
		for x in range(0, len(subset[y])):
			if subset[y][x] == "#":
				nposs+=1
			if subset[y][x] == "B":
				nbombs+=1
	return nposs+nbombs >= int(subset[pos[1]][pos[0]])
	
def overmarked(subset, pos):
	nbomb = 0
	for y in range(0, len(subset)):
		for x in range(0, len(subset[y])):
			if subset[y][x] == "B":
				nbomb+=1
	return nbomb <= int(subset[pos[1]][pos[0]])

start = datetime.datetime.now()
	
for game in range(0, games):
	print
	print "@"*65 
	print "Game: "+str(game+1)
	
	g = grid.grid(size, nmines, [int(size/2),int(size/2)], False)

	passes = 0
	
	while 1:
		#print "*"*65
		#print "Pass: "+str(passes+1)
		oldstate = g.outputGrid(False)
		for y in range(0, size):
			for x in range(0, size):
				if isNumber(g.getAt(x,y,False)):
					d = g.outputGrid(False, [x-1,x+1,y-1,y+1])
				#if isNumber(d[(y!=0)][(x!=0)]): #If our location is a number, count surrounding unknowns and bombs
					nunknown = 0
					adjmines = 0
					for l in d:
						for c in l:
							if c=="#":
								nunknown+=1
							if c=="B":
								adjmines+=1
					if adjmines == int(d[(y!=0)][(x!=0)]): #All of the mines for this square found, double click it
						g.doubleClick(x,y)
					elif nunknown+adjmines == int(d[(y!=0)][(x!=0)]): #We can mark all of the adjacent unknowns as mines
						for iy in range(0,len(d)):
							for ix in range(0, len(d[iy])):
								if d[iy][ix] == "#":
									g.mark(ix+x-(x!=0), iy+y-(y!=0), True)
				
		#g.draw()
		passes += 1
		if g.getUnmarked() == 0:
			won+=1
			print "Game won!"
			break
		if oldstate == g.outputGrid(False):
			#print "No progress made, trying some elimination"
			#incomplete += 1
			w = g.outputGrid(False)
			poss = []
			for y in range(0, len(w)):
				for x in range(0, len(w[y])):
					if isNumber(w[y][x]):
						for ix in range(useful.clamp(x-1,0,size),useful.clamp(x+2,0,size)):
							for iy in range(useful.clamp(y-1,0,size),useful.clamp(y+2,0,size)):
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
				else:
					print "Trying a random guess"
					guess = random.choice(poss)
					try:
						g.click(guess[0], guess[1])
					except grid.clickedMine:
						print "Guessed a mine, game lost with "+str(g.getUnmarked()) + " mines left"
						lost+=1
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
									for ix in range(useful.clamp(x-1,0,size),useful.clamp(x+2,0,size)):
										for iy in range(useful.clamp(y-1,0,size),useful.clamp(y+2,0,size)):
											if tg[iy][ix] == "B":
												bpos.append([ix,iy])
											elif tg[iy][ix] == "#":
												upos.append([ix,iy])
									#print str(bpos)+"="+str(len(bpos))
									#print str(upos)+"="+str(len(upos))
									if len(bpos) > int(tg[y][x]): 
										#print "Overbombed number found, clicking initial guess"
										g.click(p[0],p[1])
										foundClick = True
										break
									if len(bpos) == int(tg[y][x]): #Found all of the bombs, delete the rest
										for up in upos:
											tg[up[1]]=tg[up[1]][:up[0]]+"X"+tg[up[1]][up[0]+1:]
									if len(bpos)+len(upos) == int(tg[y][x]): #The number of unknowns matches the middle number, we can mark them all
										for up in upos:
											tg[up[1]]=tg[up[1]][:up[0]]+"B"+tg[up[1]][up[0]+1:]
									if int(tg[y][x]) > len(upos)+len(bpos): #Not enough spots to get all the bombs in
										#print "Unsatisfiable number found, clicking initial guess"
										g.click(p[0],p[1])
										foundClick = True
										break
					#print "No change"
					if foundClick:
						break
				if not foundClick:
					#print "Elimination logic found nothing new, randomly guessing"
					poss = []
					for y in range(0, len(w)):
						for x in range(0, len(w[y])):
							if w[y][x] == "#":
								poss.append([x,y])
					if len(poss)==g.getUnmarked():
						#print "All unmarked are bombs"
						for p in poss:
							g.mark(p[0],p[1], True)
					else:
						#print "Trying a random guess"
						guess = random.choice(poss)
						try:
							g.click(guess[0], guess[1])
						except grid.clickedMine:
							print "Guessed a mine, game lost with "+str(g.getUnmarked()) + " mines left"
							lost+=1
							break

elapsed = datetime.datetime.now() - start
			
print
print "@"*65 		
print "Games: "+str(games)
print "\tWon: "+str(won)
print "\tLost: "+str(lost)
print "\tIncomplete: "+str(incomplete)
print "Win percentage: "+str(100*float(won)/games)+"%"
print "Total time: " +str(elapsed.seconds)+" seconds"
print "Time per game: "+str(float(elapsed.seconds)/games)+" seconds"