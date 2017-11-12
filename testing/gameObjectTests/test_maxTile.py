from allGameObjectTests import *

def test_1_maxTile():
	boardTest = Board(config=config1)
	assert boardTest.maxTile == config1MaxTile

def test_10_maxTile():
	boardTest = Board(config=config10)
	assert boardTest.maxTile == config10MaxTile

def test_11_maxTile():
	boardTest = Board(config=config11)
	assert boardTest.maxTile == config11MaxTile
