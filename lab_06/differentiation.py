from math import *
import numpy as np
import pandas as pd

xB = -3
xE = 3
h = 1

a0, a1, a2 =  1, 2, 3

def f(x):
	# return cos(x) - 1
	return (a0 * x / (a1 + a2 * x))

def f_der(x):
	# return -sin(x)
	return (a0 * (a1 + a2 * x) - a0 * a2 * x) / ((a1 + a2 * x) ** 2)

def etaksi(): # производная эта по кси
	return a1 / a0

def etay(y): # производная эта по у
	return y * y

def ksix(x): # производная кси по х
	return 1 / (x * x)

def createTable():
	table = [[], []]
	xCur = xB
	while (xCur <= xE):
		table[0].append(xCur)
		table[1].append(f(xCur))
		xCur += h

	return table

# односторонняя (правостороняя) разность
def oneSideDiff(table):
	der = []

	for i in range(0, len(table[0]) - 1):
		dx = table[0][i + 1] - table[0][i]
		if (dx == 0):
			der.append(None)
		else:
			df = table[1][i + 1] - table[1][i]
			der.append(df / dx)
	der.append(None)

	return der

# формулы повышенной точности на краях
def boundaryDiff(table):
	der = []
	sz = len(table[0])

	for i in range(sz):
		der.append(None)

	h = table[0][1] - table[0][0]

	der[0] = (-3 * table[1][0] + 4 * table[1][1] - table[1][2]) / (2 * h)
	der[sz - 1] = (3 * table[1][sz - 1] - 4 * table[1][sz - 2] + table[1][sz - 3]) / (2 * h)

	return der

# центральная (двусторонняя) разность
def centralDiff(table):
	der = [None]

	for i in range(1, len(table[0]) - 1):
		dx = table[0][i + 1] - table[0][i - 1]
		if (dx == 0):
			der.append(None)
		else:
			df = table[1][i + 1] - table[1][i - 1]
			der.append(df / dx)
	der.append(None)

	return der

# формула Рунге (одностороннии производные)
def RungeDiff(table):
	der = []

	sz = len(table[0])
	h = table[0][1] - table[0][0]
	rh = 2 * h
	p = 1

	"""der.append(None)
	der.append(None)"""

	for i in range(0, sz - 2):
		ksih = (table[1][i + 1] - table[1][i]) / h
		ksirh = (table[1][i + 2] - table[1][i]) / rh

		der.append(ksih + (ksih - ksirh) / (pow(2, p) - 1))

	"""for i in range(2, sz):
		ksih = (table[1][i] - table[1][i - 1]) / h
		ksirh = (table[1][i] - table[1][i - 2]) / rh

		der.append(ksih + (ksih - ksirh) / (pow(2, p) - 1))"""

	der.append(None)
	der.append(None)

	return der

# выравнивающие переменные
def alignmentVarDiff(table):
	der = []

	for i in range(len(table[0])):
		if (table[0][i] == 0):
			der.append(None)
		else:
			der.append(etaksi()*etay(table[1][i])*ksix(table[0][i]))

	return der

if (__name__ == "__main__"):
	table = createTable()

	if (len(table[0]) < 3):
		print("Size of table must be more then 2")
		exit()

	oneSideTable = oneSideDiff(table)
	boundaryTable = boundaryDiff(table)
	centralTable = centralDiff(table)
	RungeTable = RungeDiff(table)
	alignmentVarTable = alignmentVarDiff(table)

	resTable = np.column_stack((table[0], oneSideTable, boundaryTable, centralTable, \
		RungeTable, alignmentVarTable, [f_der(i) for i in table[0]]))

	resTableStr = pd.DataFrame(resTable, columns=["x", "одност.разн.", "на краях", \
		"центр.разн.", "форм.Рунге", "вырав.перем.", "f'(x)"])
	
	print("\n")
	print(resTableStr)
	print("\n")
