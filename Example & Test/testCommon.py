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

#Test and Example Code. Not automated. Monitor relays and check output.

import time
import dae_RelayBoard 

def testStateFunctions(dr, relay, state):
    dr.setState(relay, state)
    time.sleep(0.5)
    testGetFunctions(dr)
    
def testGetFunctions(dr, printNums=True):
    states = dr.getStates()
    allStates = {}
    singleStates = {}
    for relay in states:
        if dr.getState(relay):
            allStates[relay] = "T"
        else:
            allStates[relay] = "F"
        if states[relay]:
            singleStates[relay] = "T"
        else:
            singleStates[relay] = "F"
    if printNums:
        print ("All States:\t" + str(allStates.keys()).replace("'",""))
        print ("\t\t" + str(allStates.values()).replace("'",""))
        print ("Single States:\t" + str(singleStates.keys()).replace("'",""))
        print ("\t\t" + str(singleStates.values()).replace("'",""))
    else:
        print ("All States:\t" + str(allStates.values()).replace("'",""))
        print ("Single States:\t"+ str(singleStates.values()).replace("'",""))      

class TestCommon:
    def __init__(self, boardType, *args):
        
        dr = dae_RelayBoard.DAE_RelayBoard(boardType)
        dr.initialise(*args)
        
        dr.setAllStatesOff()
        
        print ("Turn on one-by-one")
        for relay in range(1,dr.getNumRelays()+1):
            testStateFunctions(dr, relay, True)
        
        print ("\n\nTurn off one-by-one")
        for relay in range(1,dr.getNumRelays()+1):
            testStateFunctions(dr, relay, False)
        
        print ("\n\nTurn all on")
        dr.setAllStatesOn()
        testGetFunctions(dr)
        time.sleep(0.5)
        
        print ("\n\nTurn all off")
        dr.setAllStatesOff()
        time.sleep(0.5)
        testGetFunctions(dr)
        
        print ("\n\nTurn even on")
        evenStates = {}
        for relay in range(1,dr.getNumRelays()+1): 
            evenStates[relay] = relay%2==0
        dr.setStates(evenStates) 
        time.sleep(0.5)   
        testGetFunctions(dr)
        
        print ("\n\nTurn first on")
        dr.setState(1,True)  
        time.sleep(0.5)  
        testGetFunctions(dr)
        
        print ("\n\nTurn first off")
        dr.setState(1,False) 
        time.sleep(0.5)   
        testGetFunctions(dr)
        
        dr.disconnect()
            
            