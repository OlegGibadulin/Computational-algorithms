from math import *

funcFromX = -3
funcToX = 3
funcStepX = 1

funcFromY = -3
funcToY = 3
funcStepY = 1

# Исследуемая функция
def searchedFunc(x, y):
	return x * x + y * y

# Создание начальной таблицы х у z
def createTableXY(funcFromX, funcToX, funcStepX, funcFromY, funcToY, \
	funcStepY):
	table = [[], [], []]
	tmp = funcFromX
	while (tmp <= funcToX):
		table[0].append(tmp)
		tmp += funcStepX

	tmp = funcFromY
	while (tmp <= funcToY):
		table[1].append(tmp)
		tmp += funcStepY

	while (funcFromX <= funcToX):
		tmpList = []
		tmp = funcFromY
		while (tmp <= funcToY):
			tmpList.append(searchedFunc(funcFromX, tmp))
			tmp += funcStepY
		table[2].append(tmpList)
		funcFromX += funcStepX

	return table

# Поиск в таблице
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
def createTable(tableXY, n, index, typeTable):
	# расстояние до х от 0 и до длины в таблице
	iterXL = index
	iterXR = len(tableXY[typeTable]) - iterXL - 1

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

	return iterXL - left, iterXL + right + 1

# Вычисление следующего столбца таблицы
def countNextColumn(table, ind):
	column = []
	for i in range(len(table[0]) - ind):
		column.append((table[ind][i] - table[ind][i + 1]) / \
			(table[0][i] - table[0][i + ind]))

	return column

if (__name__ == "__main__"):
	tableXY = createTableXY(funcFromX, funcToX, funcStepX, funcFromY, funcToY,\
	 funcStepY)
	# nX = 2
	# x = 1.25
	# nY = 2
	# y = 1.5

	nX = int(input("Введите степень полинома для x: "))
	while (nX <= 0):
		print("Степень полинома должна быть положительной\n")
		nX = int(input("Введите степень полинома для x: "))

	x = float(input("Введите x: "));

	if (len(tableXY[0]) < nX + 1 ):
		print("Размер таблицы должен быть больше степени полинома")
		exit()

	if (x < funcFromX or x > funcToX):
		print("x выходит за пределы, возможно \
получение неточного значения (экстрополяция)")

	nY = int(input("Введите степень полинома для y: "))
	while (nY <= 0):
		print("Степень полинома должна быть положительной\n")
		nY = int(input("Введите степень полинома для x: "))

	y = float(input("Введите y: "));

	if (len(tableXY[1]) < nY + 1):
		print("Размер таблицы должен быть больше степени полинома")
		exit()

	if (y < funcFromY or y > funcToY):
		print("y выходит за пределы, возможно \
получение неточного значения (экстрополяция)")

	index = binarySearch(tableXY[0], x)
	index -= 1
	typeTable = 0 # 0 - x; 1 - y
	leftX, rightX = createTable(tableXY, nX, index, typeTable)

	s = (5 - len("x/y")) * " " + "x/y"

	for i in range(len(tableXY[1])):
		s += (5 - len(str(tableXY[1][i]))) * " " + str(tableXY[1][i])

	print(s)

	for i in range(len(tableXY[0])):
		s = ""
		s += (5 - len(str(tableXY[0][i]))) * " " + str(tableXY[0][i])
		for j in range(len(tableXY[2][i])):
			s += (5 - len(str(tableXY[2][i][j]))) * " " + str(tableXY[2][i][j])
		print(s)

	table = [[], []]

	# таблица для интерполяции по х
	for i in range(leftX, rightX):
		table[0].append(tableXY[0][i])

	index = binarySearch(tableXY[1], y)
	index -= 1
	typeTable = 1 # 0 - x; 1 - y
	leftY, rightY = createTable(tableXY, nY, index, typeTable)

	# таблица для интерполяции по у для х
	for i in range(leftX, rightX):
		tmpTable = [[], []]
		for j in range(leftY, rightY):
			tmpTable[0].append(tableXY[1][j])
			tmpTable[1].append(tableXY[2][i][j])

		# print(tmpTable)

		fx = tmpTable[1][0]

		for k in range(1, nY + 1):
			tmpTable.append(countNextColumn(tmpTable, k))
			tmp = 1
			for m in range(0, k):
				tmp *= y - tmpTable[0][m]
			fx += tmp * tmpTable[k + 1][0]
		table[1].append(fx)

	print(table)

	fx = table[1][0]

	for i in range(1, nX + 1):
		table.append(countNextColumn(table, i))
		tmp = 1
		for j in range(0, i):
			tmp *= x - table[0][j]
		fx += tmp * table[i + 1][0]

	print("Полученный результат: ", "%.2f" % fx)
	print("Проверочный результат: ", "%.2f" % searchedFunc(x, y))
	print("Погрешность: ", abs(fx - searchedFunc(x, y)))
