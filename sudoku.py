#!/usr/bin/python

import copy
import math

class sudokumatrix:
	sudokuLength = 0
	areaMap = []

	def __init__(self, maxnum = 9):
		self.sudokuLength = maxnum
		self.availNumberSet = set(range(1, maxnum+1))

		self.cells = []
		self.cellMask = []

		for i in range(maxnum*maxnum):
			self.cells.append(0)
			self.cellMask.append([0]*(maxnum+1))
			self.areaMap.append(set())

		# Temporary build areaMapMask
		areaMapMask = []
		zoneLength = maxnum // int(math.sqrt(maxnum))
		zoneNumber = 0

		for i in range(zoneLength):
			for j in range(zoneLength):
				for k in range(zoneLength):
					areaMapMask.extend([zoneNumber+k]*zoneLength)
			zoneNumber += zoneLength

		# Build areaMap
		for position in range(maxnum*maxnum):
			# RowMap
			row = (position // self.sudokuLength) * self.sudokuLength
			self.areaMap[position].update(range(row,row + self.sudokuLength))

			# ColMap
			col = position % self.sudokuLength
			self.areaMap[position].update(range(col, self.sudokuLength ** 2, self.sudokuLength))

			# BoxMap
			count = 0
			for b in range(self.sudokuLength ** 2):
				if areaMapMask[b] == areaMapMask[position]:
					self.areaMap[position].add(b)
					count += 1
	
					if count >= self.sudokuLength:
						break


	def ChangeCell(self, position, number):
		oldnumber = self.cells[position]
		self.cells[position] = number

		for c in self.areaMap[position]:
			if oldnumber != 0:
				self.cellMask[c][oldnumber] -= 1
			if number != 0:
				self.cellMask[c][number] += 1


	def IsFinished(self):
		# Not yet complete check
		for i in range(self.sudokuLength ** 2):
			if self.cells[i] == 0:
				return 0
		# Completed
		return 1

	def ViewMatrix(self):
		count = 0
		for i in range(self.sudokuLength):
			for j in range(self.sudokuLength):
				print self.cells[count],
				count += 1
			print ""

	def ViewCellMask(self):
		count = 0
		for i in range(self.sudokuLength):
			for j in range(self.sudokuLength):
				print self.cellMask[count],
				count += 1
			print ""
	


class guess:
	def BuildCellMaskSet(self, position):
		maskedNumbers = set()

		for i in range(1, self.matrix.sudokuLength + 1):
			if self.matrix.cellMask[position][i] > 0:
				maskedNumbers.add(i)

		return maskedNumbers


	def CalcMatrix(self):
		canFill = self.matrix.sudokuLength - 1

		while 1:
			continueflag = 0
			for i in range(self.matrix.sudokuLength ** 2):
				maskedNumbers = self.BuildCellMaskSet(i)

				if self.matrix.cells[i] == 0 and len(maskedNumbers) == canFill:
					continueflag = 1
					number = (self.matrix.availNumberSet - maskedNumbers).pop()
					print "Fillable cell found : position %d is %d" % (i,number)
					self.matrix.ChangeCell(i,number)
				elif self.matrix.cells[i] == 0 and len(maskedNumbers) == canFill + 1: # Incorrect sudoku condition
					return 1

			if continueflag == 0:
				break

		return 0


	def FindMostGuessableCell(self):
		MostMaskedCell = -1
		MostMaskedLength = 0

		for i in range(self.matrix.sudokuLength ** 2):
			if self.matrix.cells[i] == 0:
				maskedNumbers = self.BuildCellMaskSet(i)
				if MostMaskedLength < len(maskedNumbers):
					MostMaskedCell = i
					MostMaskedLength = len(maskedNumbers)
					if MostMaskedLength >= self.matrix.sudokuLength - 1:
						break

		return MostMaskedCell


	def Guess(self,matrix):
		self.matrix = copy.deepcopy(matrix)
		result = self.CalcMatrix()

		if result == 1: # Wrong answer
			return 0

	# Terminate condition
		if self.matrix.IsFinished() == 1: # Found correct answer
			self.matrix.ViewMatrix()
			return 1

	# Or Else
		guessposition = self.FindMostGuessableCell()
		guessnumbers = self.matrix.availNumberSet - self.BuildCellMaskSet(guessposition)

		for guessnumber in guessnumbers:
			print "Guess : position %d maybe %d" % (guessposition,guessnumber)
			self.matrix.ChangeCell(guessposition,guessnumber)
			nextguess = guess()
			result = nextguess.Guess(self.matrix)

			if result == 1:
				return self.FindAnotherSolution()
			
			if result == 2: # No more proceed, please.
				return 2

			print "Guess : position %d is not %d. guess next" % (guessposition,guessnumber)

		return 0


	def FindAnotherSolution(self):
		yesno = raw_input("Find Another Solution?(y/N) : ")
	
		if yesno == 'y':
			return 0

		return 2

		

def Input():
	while 1:
		inputdata = raw_input('Input sudoku matrix : ')

		length = math.sqrt(len(inputdata.split(',')))

		# Validator
		if int(length) != length :
			print max(inputdata.split(',')), length
			print "Wrong Data! Please Input Again"
			print "Example : 9,0,0,8,2,0,1,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,6,4,0,9,0,0,0,0,7,0,0,2,1,0,0,0,7,0,0,0,3,0,0,0,8,3,0,0,5,0,0,0,0,9,0,1,7,0,0,0,0,3,0,0,0,0,0,0,0,0,5,1,8,0,4,3,0,0,2"
			print "(9x9 sudoku)"
			continue
		else:
			break

	length = int(length)

	print "(",length,"x",length,") sudoku :"

	data = sudokumatrix(length)
	count = 0
	for k in inputdata.split(','):
		data.ChangeCell(count,int(k))
		count += 1

	return data

# main function

gt = guess()

while 1:
	data = Input()

	data.ViewMatrix()

	yesno = raw_input("Is this Correct?(y/N) : ")

	if yesno == 'y':
		break


gt.Guess(data)
