from math import *

funcFrom = 0
funcTo = 1
funcStep = 1

# Исследуемая функция
def searchedFunc(x):
	# return sin(radians(30 * x))
	return x * x

# Создание начальной таблицы х у
def createTableXY(x0, xN, h):
	table = [[],[]]
	for x in range(x0, xN + h, h):
		table[0].append(x)
		table[1].append(searchedFunc(x))

	return table

def createDiffTable(tableXY):
	diffTable = [[0],[0]]

	for i in range(1, len(tableXY[0])):
		h = tableXY[0][i] - tableXY[0][i - 1]
		y = (tableXY[1][i] - tableXY[1][i - 1]) / h

		diffTable[0].append(h);
		diffTable[1].append(y);

	return diffTable

def createSlauTable(diffTable):
	slauTable = [[0, 0], [0, 0], [0, 0], [0, 0]]

	for i in range(2, len(diffTable[0])):
		A = diffTable[0][i - 1]
		B = -2 * (diffTable[0][i - 1] + diffTable[0][i])
		D = diffTable[0][i]
		F = -3 * (diffTable[1][i] - diffTable[1][i - 1])

		slauTable[0].append(A)
		slauTable[1].append(B)
		slauTable[2].append(D)
		slauTable[3].append(F)

	return slauTable

def createCoeffTable(slauTable):
	coeffTable = [[0, 0, 0], [0, 0, 0]]

	ksi = 0 # eds
	eta = 0 # n

	for i in range(2, len(slauTable[0]) - 1):
		tmp = slauTable[1][i] - slauTable[0][i] * ksi

		ksi = slauTable[2][i] / tmp
		eta = (slauTable[3][i] + slauTable[0][i] * eta) / tmp

		coeffTable[0].append(ksi)
		coeffTable[1].append(eta)

	return coeffTable

def findC(slauTable, coeffTable):
	n = len(slauTable[0]) - 1
	if (n == 1):
		eta = 0
	else:
		tmp = slauTable[1][n] - slauTable[0][n] * coeffTable[0][n]
		eta = (slauTable[3][n] + slauTable[0][n] * coeffTable[1][n]) / tmp
	c = [0, eta]

	for i in range(len(coeffTable[0]) - 1, 0, -1):
		c.append(coeffTable[0][i] * c[-1] + coeffTable[1][i])

	return c[::-1]

def findABD(c, diffTable, tableXY):
	table = [[0], [0], [0], [0]]

	for i in range(1, len(tableXY[0])):
		a = tableXY[1][i - 1]
		b = diffTable[1][i] - (c[i + 1] + 2 * c[i]) * \
		diffTable[0][i] / 3
		d = (c[i + 1] - c[i]) / (3 * diffTable[0][i])

		table[0].append(a)
		table[1].append(b)
		table[2].append(c[i])
		table[3].append(d)

	return table

def binarySearch(tableX, item):
	low = 0
	high = len(tableX) - 1

	while (low <= high):
		mid = int((low + high) / 2)
		guess = tableX[mid]
		if (item == guess):
			return mid
		elif (item < guess):
			high = mid - 1
		else:
			low = mid + 1
	
	return low

if (__name__ == "__main__"):
	tableXY = createTableXY(funcFrom, funcTo, funcStep)

	print("X         Y")
	for i in range(len(tableXY[0])):
		print("%7.2f" % tableXY[0][i], "%7.2f" % tableXY[1][i])

	x = float(input("Введите x: "));

	if (x < funcFrom or x > funcTo):
		print("Экстарполяция")

	# forward step
	diffTable = createDiffTable(tableXY)
	slauTable = createSlauTable(diffTable)
	coeffTable = createCoeffTable(slauTable)

	# back step
	c = findC(slauTable, coeffTable)
	table = findABD(c, diffTable, tableXY)

	index = binarySearch(tableXY[0], x);
	if (index >= len(tableXY[0])):
		index -= 1
	dx = x - tableXY[0][index - 1]
	fx = table[0][index] + dx * (table[1][index] + dx * (table[2][index] + \
		dx * table[3][index]))
	
	print("Полученный результат: ", "%.2f" % fx)
	print("Проверочный результат: ", "%.2f" % searchedFunc(x))
	print("Погрешность: ", "%.5f" % abs(fx - searchedFunc(x)))
