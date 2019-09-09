from math import *
import numpy as np

E = [12.13, 20.98, 31.00, 45.00]

T0 = 20000
Tw = 3000
m = 40

VBegin = -1
XBegin = [3, -1, -10, -20, -35]

eps = 1e-4
dihEps = 1e-5

def readFile(str):
	f = open(str, 'r')
	nums = []
	for i in range(5):
		nums.append([])

	for line in f:
		r = 0
		T = ""

		while (line[r] != ' '):
			T += line[r]
			r += 1

		for i in range(5):
			while (line[r] == ' '):
				r += 1
			Q = ""
			while (line[r] != ' ' and line[r] != '\n'):
				Q += line[r]
				r += 1
			num = [float(T), float(Q)]
			nums[i].append(num)
	f.close()

	return nums

def calculateQ(Q_from_T, T):
	res = Q_from_T[0][1]
	n = len(Q_from_T)

	for i in range(n - 1):
		get_mult = 1
		for l in range(i + 1):
			get_mult *= T - Q_from_T[l][0]
		get_mult *= Q_from_T[l + 1][l + 2]
		res += get_mult

	return res

def interp(str):
	Q_from_T = readFile(str)
	for i in range(5):
		n = len(Q_from_T[i])
		for k in range(n):
			for l in range(n - 1):
				Q_from_T[i][k].append(0)

	for k in range(5):
		n = len(Q_from_T[k])
		for i in range(n - 1):
			for l in range(i + 1, n, 1):
			 Q_from_T[k][l][i + 2] = (Q_from_T[k][l - 1][i + 2 - 1] - \
			 	Q_from_T[k][l][i + 2 - 1]) / (Q_from_T[k][l - i - 1][0] - Q_from_T[k][l][0])

	return Q_from_T

def getQ(T):
	Q = []
	coeff = interp("static_sum.txt")
	for i in range(5):
		Q.append(calculateQ(coeff[i], T))

	return Q

def f(T, V, X, z, G):
	numSum = 0

	for i in range(1, 5):
		numSum += exp(X[i] * pow(z[i], 2) / (1 + pow(z[i], 2) * (G / 2)))

	y = pow(G, 2) - 5.87 * pow(10, 10) * (1 / pow(T, 3)) * (exp(V) / (1 + G / 2) + numSum)

	return y

def getC(a, b):
	return (a + b) / 2

def dihMethod(T, V, X, z):
	iterMax = 100
	count = 0
	a = 0
	b = 3
	c = 1.5

	while (fabs((b - a) / c) > eps):
		count += 1
		c = getC(a, b)
		if (f(T, V, X, z, a) * f(T, V, X, z, c) <= 0):
			b = c
		elif (f(T, V, X, z, b) * f(T, V, X, z, c) < 0):
			a = c

	return getC(a, b)

def getdE(T, z, G):
	dE = []
	for i in range(0, 4):
		num = 8.61 * pow(10, -5) * T * log((1 + pow(z[i + 1], 2) * \
			(G / 2)) * (1 + G / 2) / (1 + pow(z[i + 1], 2) * (G / 2)))
		dE.append(num)

	return dE

def getK(T, z, G, E, dE, Q):
	K = []
	for i in range(0, 4):
		num = 2 * 2.415 * pow(10,-3) * Q[i + 1] / Q[i] * pow(T, 1.5) * \
		exp(-(E[i] - dE[i]) * (11603 / T))
		K.append(num)

	return K

def getMatrix(T, p, G, X, K, V, z):
	matrix = [[], [], [], [], [], []]
	vector = []

	matrix[0].append(1)
	matrix[0].append(-1)
	matrix[0].append(1)
	matrix[0].append(0)
	matrix[0].append(0)
	matrix[0].append(0)

	matrix[1].append(1)
	matrix[1].append(0)
	matrix[1].append(-1)
	matrix[1].append(1)
	matrix[1].append(0)
	matrix[1].append(0)

	matrix[2].append(1)
	matrix[2].append(0)
	matrix[2].append(0)
	matrix[2].append(-1)
	matrix[2].append(1)
	matrix[2].append(0)

	matrix[3].append(1)
	matrix[3].append(0)
	matrix[3].append(0)
	matrix[3].append(0)
	matrix[3].append(-1)
	matrix[3].append(1)

	matrix[4].append(exp(V))
	matrix[5].append(-exp(V))

	for i in range(0, 5):
		matrix[4].append(-z[i] * exp(X[i]))
		matrix[5].append(-exp(X[i]))

	for i in range(0, 4):
		num = -(V + X[i + 1] - X[i] - log(K[i]))
		vector.append(num)

	num = exp(V)
	for i in range(1, 5):
		num -= z[i] * exp(X[i])
	vector.append(-num)

	num = 0.285 * pow(10, -11) * pow(G * T, 3) + p * 7242 / T - exp(V)
	for i in range(0, 5):
		num -= exp(X[i])
	vector.append(-num)

	return matrix, vector

def convertPascalToAtm(pascal):
    return pascal / 101325

def convertAtmToPascal(atm):
    return atm * 101325

def getT(zi):
    return T0 + (Tw - T0) * pow(zi, m)

def GaussMethod(matrix, vector):
    M = np.array(matrix)
    v = np.array(vector)
    vectorTmp = np.linalg.solve(M, v)
    return M, vectorTmp

def calcN(p, zi):
	p = convertPascalToAtm(p)
	X = XBegin.copy()
	V = VBegin
	T = getT(zi)
	Q = getQ(T)

	err = [0, 0, 0, 0, 0, 0]
	dv = -1
	dx = [3, -1, -10, -20, -35]
	z = [0, 1, 2, 3, 4]
	# G = 0

	while (True):
		G = dihMethod(T, V, X, z)
		dE = getdE(T, z, G)
		K = getK(T, z, G, E, dE, Q)
		matrix, vector = getMatrix(T, p, G, X, K, V, z)
		matrix, vector = GaussMethod(matrix, vector)

		dv = vector[0]
		err[0] = vector[0] / V
		V += dv

		for i in range(0, 5):
			dx[i] = vector[i + 1]
			err[i + 1] = fabs(vector[i + 1] / X[i])
			X[i] += dx[i]

		if (max(err) < eps):
			break

	numSum = 0

	if (zi == 0):
		for x in X:
			print(exp(x));

		print(exp(V))
		print(G)
		print()

	for x in X:
		numSum += exp(x)

	return convertAtmToPascal(numSum)

def integ(p):
	h = 1 / 40
	summ = (calcN(p, 0) * 0 + calcN(p, 1) * 1) / 2
	z = h

	while (z < 1):
		summ += calcN(p, z) * z
		z += h
	summ *= h

	return summ

def Fp(p):
	PBegin = convertAtmToPascal(0.5)
	TBegin = 300

	return 7242 * PBegin / TBegin - 2 * integ(p)

def calcP(p1, p2):
	return (p1 + p2) / 2

def calcDiff(p1, p2):
	return fabs(p2 - p1)

def dih():
	p1 = convertAtmToPascal(3)
	p2 = convertAtmToPascal(25)
	del_p = calcDiff(p1, p2)

	if (Fp(p1) > Fp(p2)):
		t = p1
		p1 = p2
		p2 = t

	p = calcP(p1, p2)
	count = 0
	while (del_p / p >= eps):
		p3 = p
		if (Fp(p3) < 0):
			p1 = p3
		else:
			p2 = p3
		p = calcP(p1, p2)
		del_p = calcDiff(p1, p2)
		count += 1
		if (count == 100):
			break

	return p

if (__name__ == "__main__"):
	print("Answer: ", convertPascalToAtm(dih()))

	
