#!/usr/bin/env python

# Example Word Search Puzzles

from wordsearchgame import PuzzleGrid

# The word list to be used
word_list = ['Python', 'Word', 'Search', 'Anastomoses', 'Embolus']
# Instantiate the PuzzleGrid class
p = PuzzleGrid(word_list)
# Create the Puzzle
p.main()
# Output to txt
p.output2txt('test.txt')
# Output to Excel
p.output2excel('test.xls')

# If you need the answers
p.output2txt('answer.txt', answer=True)
p.output2excel('answer.xls', answer=True)
