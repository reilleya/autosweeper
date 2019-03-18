def clamp(val, min, max):
	if val > max:
		return max
	elif val < min:
		return min
	else:
		return val
		
def exclude(set, index):
	return set[:index]+set[index+1:]

def combinations(values):
	combos = []
	indices = []
	n = 1
	for l in values:
		n*=len(l)
		indices.append(0)
	for i in range(0, n):
		combos.append(indices[:])
		indices[0]+=1
		for ci in range(0, len(values)):
			if indices[ci] == len(values[ci]):
				indices[ci] = 0
				if ci+1 == len(values):
					#combos.append(indices)
					break
				else:
					indices[ci+1] += 1
	
	return combos #NO FINISH IT
	
def combinationsN(n,v):
	vals = []
	for i in range(0, n):
		vals.append(range(0, v+1))
	return combinations(vals)
	
def everyOrder(set):
	if len(set) == 1:
		return [set]
	else:
		out = []
		for i in range(0, len(set)):
			ends = everyOrder(exclude(set,i))
			for end in ends:
				out.append([set[i]]+end)
		return out
		
def countClumps(set):
	out = [1]
	for i in range(1, len(set)):
		if set[i] == set[i-1]:
			out[-1]+=1
		else:
			out.append(1)
	return out
	
def counts(set):
	out = {}
	for item in set:
		if item in out:
			out[item]+=1
		else:
			out[item]=1
	return out
	
def progressBar(current, total, width):
	out = "["
	blocks = int((float(current)/total)*width)
	out += "="*blocks
	out += " "*(width-blocks)
	out += "]"
	return out
	
def winPrint(text, name):
	import win32print #is this how I multiplatform?
	pname = win32print.GetDefaultPrinter()
	printer = win32print.OpenPrinter(pname)
	job = win32print.StartDocPrinter(printer, 1, (name, None, "RAW"))
	win32print.StartPagePrinter(printer)
	win32print.WritePrinter(printer, text)
	win32print.EndPagePrinter(printer)
	win32print.EndDocPrinter(printer)
	win32print.ClosePrinter(printer)
	
def fileExists(fileName):
	try:
		open(fileName, "r").close()
		return True
	except:	
		return False
		