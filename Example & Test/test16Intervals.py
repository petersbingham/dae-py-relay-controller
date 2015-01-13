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

#Tests for the interval timings. Change below to test for different times:
INTERVAL = 0.050
#Set Com port below:
COMPORT = "COM8"

import time
import testCommon
import dae_RelayBoard 

        
dr = dae_RelayBoard.DAE_RelayBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_16, INTERVAL)
dr.initialise(COMPORT)

dr.setAllStatesOff()
testCommon.testGetFunctions(dr, False)

for relay in range(1,dr.getNumRelays()+1):
    dr.setState(relay, True)
    testCommon.testGetFunctions(dr, False)  
    
dr.disconnect()