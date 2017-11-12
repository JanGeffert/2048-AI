from allGameObjectTests import *

def test_1_shiftLeft():
	boardTest = Board(XDIM, YDIM, config=config1)
	boardTest.shift("LEFT")
	assert boardTest.grid == config1ShiftLeft

def test_1_shiftRight():
	boardTest = Board(XDIM, YDIM, config=config1)
	boardTest.shift("RIGHT")
	assert boardTest.grid == config1ShiftRight

def test_1_shiftUp():
	boardTest = Board(XDIM, YDIM, config=config1)
	boardTest.shift("UP")
	assert boardTest.grid == config1ShiftUp

def test_1_shiftDown():
	boardTest = Board(XDIM, YDIM, config=config1)
	boardTest.shift("DOWN")
	assert boardTest.grid == config1ShiftDown

def test_4_shiftDown():
	boardTest = Board(XDIM, YDIM, config=config4)
	boardTest.shift("DOWN")
	assert boardTest.grid == config4ShiftDown

def test_5_shiftLeft():
	boardTest = Board(XDIM, YDIM, config=config5)
	boardTest.shift("LEFT")
	assert boardTest.grid == config5ShiftLeft

def test_10_shiftUp():
	boardTest = Board(XDIM, YDIM, config=config10)
	boardTest.shift("UP")
	assert boardTest.grid == config10ShiftUp

def test_10_shiftDown():
	boardTest = Board(XDIM, YDIM, config=config10)
	boardTest.shift("DOWN")
	assert boardTest.grid == config10ShiftDown