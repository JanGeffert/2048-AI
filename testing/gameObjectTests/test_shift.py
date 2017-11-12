from allGameObjectTests import *
import pytest

def test_1_shiftLeft():
	boardTest = Board(config=config1)
	boardTest.shift("LEFT")
	assert boardTest.grid == config1ShiftLeft

def test_1_shiftRight():
	boardTest = Board(config=config1)
	boardTest.shift("RIGHT")
	assert boardTest.grid == config1ShiftRight

@pytest.mark.skip(reason="no way of currently testing this")
def test_1_shiftUp():
	boardTest = Board(config=config1)
	boardTest.shift("UP")
	assert boardTest.grid == config1ShiftUp

@pytest.mark.skip(reason="no way of currently testing this")
def test_1_shiftDown():
	boardTest = Board(config=config1)
	boardTest.shift("DOWN")
	assert boardTest.grid == config1ShiftDown

def test_4_shiftDown():
	boardTest = Board(config=config4)
	boardTest.shift("DOWN")
	assert boardTest.grid == config4ShiftDown

def test_5_shiftLeft():
	boardTest = Board(config=config5)
	boardTest.shift("LEFT")
	assert boardTest.grid == config5ShiftLeft

def test_10_shiftUp():
	boardTest = Board(config=config10)
	boardTest.shift("UP")
	assert boardTest.grid == config10ShiftUp

def test_10_shiftDown():
	boardTest = Board(config=config10)
	boardTest.shift("DOWN")
	assert boardTest.grid == config10ShiftDown