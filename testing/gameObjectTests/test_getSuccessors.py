from allGameObjectTests import *

def test_1_getSuccessorsLeft():
	boardTest = Board(config=config12)
	successorStates, successorProbs = boardTest.getSuccessors("LEFT")
	successorGrids = [x.grid for x in successorStates]
	testGrids, testProbs = config12SuccessorsLeft
	assert set(successorGrids) == set(testGrids)
	assert set(successorProbs) == set(testProbs)