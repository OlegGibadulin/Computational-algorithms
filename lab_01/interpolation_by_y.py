from math import *

funcFrom = -4
funcTo = 3
funcStep = 2

# Исследуемая функция
def searchedFunc(x):
	# return sin(radians(30 * x))
	return x * x - 1

# Создание начальной таблицы х у
def createTableXY(x0, xN, h):
	table = [[],[]]
	while (x0 <= xN):
		table[0].append(x0)
		table[1].append(searchedFunc(x0))
		x0 += h

	return table

# Поиск x в таблице ху
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

# Создание таблицы для интерполяции
def createTable(tableXY, n, index):
	# расстояние до х от 0 и до длины в таблице
	iterXL = index
	iterXR = len(tableXY[0]) - iterXL - 1

	# количество элементов справа и слева
	gap = int(n / 2)
	left = gap
	right = n - gap

	if (iterXL < left):
		right += gap - iterXL
		left = iterXL

	if (iterXR < right):
		left += right - iterXR
		right = iterXR

	# таблица для интерполяции
	table = [[],[]]
	for i in range(iterXL - left, iterXL + right + 1, 1):
		table[0].append(tableXY[0][i])
		table[1].append(tableXY[1][i])

	return table

# Вычисление следующего столбца таблицы
def countNextColumn(table, ind):
	column = []
	for i in range(len(table[0]) - ind):
		column.append((table[ind][i] - table[ind][i + 1]) / \
			(table[0][i] - table[0][i + ind]))

	return column

def funcHalfDel(a, b):
	eps = 1e-5
	while (a - b > eps):
		c = (a + b) / 2.0
		fa = searchedFunc(a)
		fc = searchedFunc(c)
		d = fc * fa

		if (d > 0):
			a = c
		else:
			b = c

	return (a + b) / 2.0

if (__name__ == "__main__"):
	tableXY = createTableXY(funcFrom, funcTo, funcStep)
	n = 2

	print("X         Y")
	for i in range(len(tableXY[0])):
		print("%7.2f" % tableXY[0][i], "%7.2f" % tableXY[1][i])

	n = int(input("Введите степень полинома: "))
	while (n <= 0):
		print("Степень полинома должна быть положительной\n")
		n = int(input("Введите степень полинома: "))

	if (len(tableXY[0]) < n + 1):
		print("Размер таблицы должен быть больше степени полинома")
		exit()

	"""tmpArr = [[],[]]
	tmpStep = (abs(funcFrom) + abs(funcTo)) / (10 * funcStep)
	print(tmpStep)
	while (funcFrom <= funcTo):
		tmpArr[0].append(funcFrom)
		tmpArr[1].append(searchedFunc(funcFrom))
		funcFrom += tmpStep"""

	tmpX = []
	num = []
	i = 0
	while i < len(tableXY[0]) - 1:
		if (tableXY[1][i] * tableXY[1][i + 1] <= 0):
			if (tableXY[1][i] == 0 or tableXY[1][i + 1] == 0):
				if (tableXY[1][i] == 0):
					tmpX.append(tableXY[0][i])
					num.append(i)
				else:
					tmpX.append(tableXY[0][i + 1])
					num.append(i + 1)
				i += 1
			else:
				tmpX.append(funcHalfDel(tableXY[0][i], tableXY[0][i + 1]))
				num.append(i)
		i += 1

	# print(tableXY)
	# print(tmpX)

	# index = binarySearch(tableXY[0], x)
	table = createTable(tableXY, n, num[0])

	fx = table[1][0]

	for i in range(1, n + 1):
		table.append(countNextColumn(table, i))
		tmp = 1
		for j in range(0, i):
			tmp *= tmpX[0] - table[0][j]
		fx += tmp * table[i + 1][0]

	for i in range(len(table)):
		print(table[i])

	print("Полученный результат: ", "%.2f" % fx)
	print("Проверочный результат: ", "%.2f" % searchedFunc(tmpX[0]))
	print("Погрешность: ", abs(fx - searchedFunc(tmpX[0])))
