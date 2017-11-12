from allGameObjectTests import *
import pytest

@pytest.mark.skip(reason="no way of currently testing this")
def test_1_getSuccessorsLeft():
	boardTest = Board(config=config12)
	successorStates, successorProbs = boardTest.getAllSuccessors("LEFT")
	successorGrids = [x.grid for x in successorStates]
	testGrids, testProbs = config12SuccessorsLeft
	testProbs = [pytest.approx(x, .01) for x in testProbs]
	assert successorGrids == testGrids
	assert successorProbs == testProbs