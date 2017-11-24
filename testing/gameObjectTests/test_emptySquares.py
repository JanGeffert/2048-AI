from allGameObjectTests import *

def test_1_emptySquares():
	boardTest = Board(config=config1)
	assert boardTest.emptySquares() == config1Free

def test_2_emptySquares():
	boardTest = Board(config=config2)
	assert boardTest.emptySquares() == config2Free

def test_3_emptySquares():
	boardTest = Board(config=config3)
	assert boardTest.emptySquares() == config3Free

def test_4_emptySquares():
	boardTest = Board(config=config4)
	assert boardTest.emptySquares() == config4Free

def test_5_emptySquares():
	boardTest = Board(config=config5)
	assert boardTest.emptySquares() == config5Free

def test_6_emptySquares():
	boardTest = Board(config=config6)
	assert boardTest.emptySquares() == config6Free

def test_7_emptySquares():
	boardTest = Board(config=config7)
	assert boardTest.emptySquares() == config7Free

def test_8_emptySquares():
	boardTest = Board(config=config8)
	assert boardTest.emptySquares() == config8Free

def test_9_emptySquares():
	boardTest = Board(config=config9)
	assert boardTest.emptySquares() == config9Free

	