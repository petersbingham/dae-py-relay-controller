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

#Example Code

import time
import dae_RelayBoard   

dr = dae_RelayBoard.DAE_RelayBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_4)

dr.initialise()

dr.setAllStatesOff()

#Turn on one-by-one
for r in range(1,dr.getNumRelays()+1):
    dr.setState(r, True)
    time.sleep(0.5)
    print (dr.getStates())

#Turn off one-by-one
for r in range(1,dr.getNumRelays()+1):
    dr.setState(r, False)
    time.sleep(0.5)
    print (dr.getStates())

#Turn all on
dr.setAllStatesOn()
print (dr.getStates())
time.sleep(0.5)

#Turn all off
dr.setAllStatesOff()
time.sleep(0.5)
print (dr.getStates())

#Turn even on
evenStates = {}
for relay in range(1,dr.getNumRelays()+1): 
    if relay%2==0:
        evenStates[relay] = True
dr.setStates(evenStates)   
time.sleep(0.5)
print (dr.getStates())

#Turn first on
dr.setState(1,True)  
time.sleep(0.5)
print (dr.getStates())

#Turn first off
dr.setState(1,False) 
time.sleep(0.5) 
print (dr.getStates())

dr.disconnect()
