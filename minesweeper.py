import grid

g = grid.grid(16, 40, [7, 7])

g.draw(True)
print()
print()
g.draw()
inp = input(">")
while inp != "done":
	print("*" * 27)
	redraw = False
	if inp[0] == "c":
		p = inp[1:].split(",")
		r = g.click(int(p[0]), int(p[1]))
		if not r:
			print("UR DED")
			break
		redraw = True
	if inp[0] == "d":
		p = inp[1:].split(",")
		r = g.doubleClick(int(p[0]), int(p[1]))
		if not r:
			print("UR DED")
			break
		redraw = True
	if inp[0] == "m":
		p = inp[1:].split(",")
		if p[2] == "B":
			toMark = True
		elif p[2] == "?":
			toMark = False
		else:
			toMark = None
		g.mark(int(p[0]), int(p[1]), toMark)
		redraw = True
	if inp[0]=="g":
		p = inp[1:].split(",")
		r = g.getAt(int(p[0]), int(p[1]),p[2])
		print(p[2] + "->" + str(r))
	if redraw:
		g.draw()
	inp = input(">")