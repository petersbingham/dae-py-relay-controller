#-----------------------------------------------------------------------------
#Copyright (c) Peter Bingham  (petersbingham@hotmail.co.uk)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#-----------------------------------------------------------------------------

#Some quick tests. You need to be connected to the board for testing. Unhandled exceptions are a fail. Comment depending on attached board.

#Example Code. Set Com port below:
COMPORT = "COM8"

import time
import dae_RelayBoard   
from dae_RelayBoard.dae_RelayBoard_Common import Denkovi_Exception

def testException(function, *args):
    try:
        function(*args)
    except Denkovi_Exception as inst:
        print ("Expected Exception: " + str(inst))

def testBoard(boardType, numRelays, devID=None):
    dr = dae_RelayBoard.DAE_RelayBoard(boardType)
    testException(dr.setAllStatesOn)
    if devID is not None:
        dr.initialise(devID)
    else:
        dr.initialise()
    testException(dr.setState, numRelays+1, True)
    testException(dr.getState, numRelays+1)
    testException(dr.setState, 0, True)
    testException(dr.getState, 0)
    dr.disconnect()

testException(dae_RelayBoard.DAE_RelayBoard, 99999)

#testBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_4, 4)
#testBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_8, 8)
testBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_16, 16, COMPORT)
