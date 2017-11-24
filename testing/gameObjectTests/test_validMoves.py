from allGameObjectTests import *
import pytest

def test_1_ValidMoves():
	board = Board(config=config1)
	assert set(board.validMoves()) == set(config1ValidMoves)

def test_2_ValidMoves():
	board = Board(config=config2)
	assert set(board.validMoves()) == set(config2ValidMoves)

def test_3_ValidMoves():
	board = Board(config=config3)
	assert set(board.validMoves()) == set(config3ValidMoves)

def test_4_ValidMoves():
	board = Board(config=config4)
	assert set(board.validMoves()) == set(config4ValidMoves)

def test_5_ValidMoves():
	board = Board(config=config5)
	assert set(board.validMoves()) == set(config5ValidMoves)

def test_6_ValidMoves():
	board = Board(config=config6)
	assert set(board.validMoves()) == set(config6ValidMoves)

def test_7_ValidMoves():
	board = Board(config=config7)
	assert set(board.validMoves()) == set(config7ValidMoves)

def test_8_ValidMoves():
	board = Board(config=config8)
	assert set(board.validMoves()) == set(config8ValidMoves)

def test_9_ValidMoves():
	board = Board(config=config9)
	assert set(board.validMoves()) == set(config9ValidMoves)
