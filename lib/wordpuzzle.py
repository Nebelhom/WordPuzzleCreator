#!/usr/bin/env python

# Word search puzzle maker

import copy
import random
from string import ascii_uppercase, upper

def find_longest_word(word_list):
		"""Determines the longest word in word_list and returns the length"""
		result = 0
		for word in word_list:
			length = len(word)
			if length > result:
				result = length
		return result


def list_upper(word_list):
	"""Returns a list of strings to all upper case"""
	result = []
	for word in word_list:
		result.append(word.upper())
	return result

def list_rm_space(word_list):
	"""Removes whitespace from strings in list"""
	result = []
	for word in word_list:
		w = word.replace(' ', '')
		result.append(w)
	return result


class PuzzleGrid(object):
	def __init__(self, word_list, repeats=10000):
		self.rows = find_longest_word(word_list) # Y range
		self.cols = find_longest_word(word_list) + 2 # X range
		self.word_list = list_rm_space(word_list)
		self.word_list = list_upper(word_list)
		self.repeats = repeats

		# Created later
		self.grid = []
		self.answer = []

		# # Directions: R2L, L2R, T2B, B2T, R2LDiagDown, R2LDiagUp, L2RDiagDown, R2LDiagUp
		self.directions = {
			'L2R': lambda x, y: [x + 1, y],
			'R2L': lambda x, y: [x - 1, y],
			'T2B': lambda x, y: [x, y + 1],
			'B2T': lambda x, y: [x, y - 1],
			'L2RDiagDown': lambda x, y: [x + 1, y + 1],
			'L2RDiagUp': lambda  x, y: [x + 1, y - 1],
			'R2LDiagDown': lambda x, y: [x - 1, y + 1],
			'R2LDiagUp': lambda x, y: [x - 1, y -1]
		}

		self.limits = {
			'L2R': lambda word: (0, self.cols - len(word), 0, self.rows - 1),
			'R2L': lambda word: (len(word) - 1, self.cols - 1, 0, self.rows - 1),
			'T2B': lambda word: (0, self.cols - 1, 0, self.rows - len(word)),
			'B2T': lambda word: (0, self.cols - 1, len(word) - 1, self.rows - 1),
			'L2RDiagDown': lambda word: (0, self.cols - len(word), 0, self.rows - len(word)),
			'L2RDiagUp': lambda word: (0, self.cols - len(word), len(word) -1, self.rows - 1),
			'R2LDiagDown': lambda word: (len(word) - 1, self.cols - 1, 0, self.rows - len(word)),
			'R2LDiagUp': lambda word: (len(word) - 1, self.cols - 1, len(word) - 1, self.rows - 1)
		}

	def __str__(self):
		s = ''
		for row in self.grid:
			for letter in row:
				s = s + ' ' + letter
			s = s + '\n'
		return s

	def check_path(self, word, coord_list):
		"""
		Checks if word space is unoccupied or the same letter.
		Returns True or False
		"""

		# Checks format: [((y, x), letter),...] I wish I knew why
		checks = zip(word, coord_list)
		for (y, x), letter in checks:
			if self.grid[x][y] != '0' and self.grid[x][y] != letter:
				return False
		return True

	def create_grid(self):
		"""Creates the grid"""
		_grid = [['0' for x in xrange(self.cols)] for x in xrange(self.rows)]
		return _grid

	def fillup_grid(self):
		"""Fills up the grid gaps with random letters"""
		i = 0
		while i < len(self.grid):
			j = 0
			while j < len(self.grid[i]):
				if self.grid[i][j] == '0':
					self.grid[i][j] = random.choice(ascii_uppercase)
				j += 1
			i += 1

	def map_coords(self, word, start_xy, direction):
		"""Maps the coordinates for the word, returns list of lists"""
		
		coords = []
		x, y = start_xy
		for letter in word:
			coords.append((x, y))
			x, y = self.directions[direction](x, y)
		return coords

	def output2excel(self, fname, answer=False, title='Word Search'):
		"""Prints the puzzle to an excel file"""
		# Dependent on xlwt, therefore need to scope it
		try:
			import xlwt

			if answer:
				grid = self.answer
			else:
				grid = self.grid

			book = xlwt.Workbook()
			sheet = book.add_sheet('Word Search')

			for k in range(0, len(self.grid[0])):
				sheet.col(k).width = 700

			# Writing to the worksheet
			sheet.write(0, 0, title, xlwt.easyxf(
				'font: bold True;'))

			# Insert the puzzle
			i = 0
			# i + space to move puzzle down from title
			space = 2
			# This is ugly but xlwt does not allow post style mod
			# of the cells
			while i < len(grid):
				j = 0
				while j < len(grid[i]):
					if grid[i][j] != '0':
						# top left corner
						if (i, j) == (0, 0):
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: left thick, top thick;'))
						# top right
						elif (i, j) == (0, len(grid[0]) - 1):
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: right thick, top thick;'))
						# bottom left
						elif (i, j) == (len(grid) - 1, 0):
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: left thick, bottom thick;'))
						# bottom right
						elif (i, j) == (len(grid) - 1, len(grid[0]) - 1):
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: right thick, bottom thick;'))
						# left
						elif j == 0:
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: left thick'))
						# right
						elif j == len(grid[0]) - 1:
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: right thick'))
						# top
						elif i == 0:
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: top thick'))
						# bottom
						elif i == len(grid) - 1:
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'
								'borders: bottom thick'))
						else:
							sheet.row(i + space).write(j, grid[i][j], xlwt.easyxf(
								'alignment: horizontal center;'
								'alignment: vertical center;'))
					j += 1
				i += 1

			# The list of words
			table_row = 2 + len(grid) + 2
			sheet.row(table_row).write(0, 'WORDLIST', xlwt.easyxf(
				'font: underline single;'))
			table_row += 1
			for word in self.word_list:
				sheet.row(table_row).write(0, word)
				table_row += 1

			book.save(fname)

		except ImportError, e:
			print "xlwt is not installed and therefore cannot be used "
			print "to write the Puzzle to an Excel File"
			pass

	def output2txt(self, fname, answer=False):
		"""Prints the Puzzle to a txt file"""

		if answer:
			grid = self.answer
		else:
			grid = self.grid

		with open(fname, 'w') as f:
			# Write the puzzle
			for row in grid:
				s = ''
				for letter in row:
					s = s + ' ' + letter
				f.write(s + '\n')
			# Write the list underneath
			f.write('\n')
			f.write('WORDLIST\n')
			f.write('--------')
			f.write('\n')
			for word in self.word_list:
				f.write(word + '\n')

	def place_words(self):
		"""
		Places the words at random into the grid.
		Returns True if all words could be placed,
		otherwise False.
		"""
		
		for word in self.word_list:
			# Choose a direction at random and call it
			direction = random.choice(self.directions.keys())
			placed = False

			# Actual placing	
			for j in xrange(self.repeats):
				# Finds a start point
				limits = self.limits[direction](word)
				x, y = [random.randint(limits[0], limits[1]),
						random.randint(limits[2], limits[3])]
				coords = self.map_coords(word, (x, y), direction)
				if self.check_path(coords, word):
					# Place the word
					for letter in word:
						self.grid[y][x] = letter
						x, y = self.directions[direction](x, y)
						placed = True
					break
			# What if the word could not be placed?
			if not placed:
				return False
		return True

	def main(self):
		"""Creates the word search puzzle"""

		for i in xrange(self.repeats):
			self.grid = self.create_grid()
			worked = self.place_words()

			if worked:
				self.answer = copy.deepcopy(self.grid)
				self.fillup_grid()
				return True
		print "Unfortunately, it was not possible to place all words."
		print "Try again or consider take out words from your list."
		print "The combination may not be possible."
		return False
