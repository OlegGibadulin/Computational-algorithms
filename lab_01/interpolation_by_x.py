from math import *

funcFrom = -3
funcTo = 3
funcStep = 1

# Исследуемая функция
def searchedFunc(x):
	# return sin(radians(30 * x))
	return x - cos(x)

# Создание начальной таблицы х у
def createTableXY(x0, xN, h):
	table = [[],[]]
	while (x0 <= xN):
		table[1].append(x0)
		table[0].append(searchedFunc(x0))
		x0 += h

	return table

"""def loadTableXY():
	table = []
	with open("table.txt", 'r') as f:
		table.readlines()
		print(table)

	return table"""

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

if (__name__ == "__main__"):
	#table = loadTableXY()
	tableXY = createTableXY(funcFrom, funcTo, funcStep)
	# n = 2
	# x = 1.5

	print("X         Y")
	for i in range(len(tableXY[0])):
		print("%7.2f" % tableXY[0][i], "%7.2f" % tableXY[1][i])


	n = int(input("Введите степень полинома: "))
	while (n <= 0):
		print("Степень полинома должна быть положительной\n")
		n = int(input("Введите степень полинома: "))

	x = 0;

	if (x < funcFrom or x > funcTo):
		print("x выходит за пределы, возможно \
			получение неточного значения (экстрополяция)")

	if (len(tableXY[0]) < n + 1):
		print("Размер таблицы должен быть больше степени полинома")
		exit()

	index = binarySearch(tableXY[0], x)
	index -= 1
	table = createTable(tableXY, n, index)

	fx = table[1][0]

	for i in range(1, n + 1):
		table.append(countNextColumn(table, i))
		tmp = 1
		for j in range(0, i):
			tmp *= x - table[0][j]
		fx += tmp * table[i + 1][0]

	print("Полученный результат: ", "%.2f" % fx)
