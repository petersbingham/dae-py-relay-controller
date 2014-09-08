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

from FTD2XXWrap import *
import dae_RelayBoard_Common

class DAE_RelayBoard_D2XX:
    BAUDRATE = 921600
    MASK = 255
    BITMODE = 4 
    
    def __init__(self):  
        self.handle = None      
        try:
            self.FTD2XX = FTD2XXWrap()
        except WindowsError:
            self.FTD2XX = None
        
    #currently only gets first board
    def initialise(self, *args):
        self.disconnect()
        self._checkInit(False)
        ret, self.handle = self._handleRet(self.FTD2XX.initFirstSpecifiedSerialNum(dae_RelayBoard_Common.DENKOVI_ID))
        self._handleRet(self.FTD2XX.FT_SetBaudRate(self.handle, self.BAUDRATE))
        self._handleRet(self.FTD2XX.FT_SetBitMode(self.handle, self.MASK, self.BITMODE))
    
    def disconnect(self):
        if self.handle is not None:
            self._checkInit()
            self._handleRet(self.FTD2XX.FT_Close(self.handle))
            self.handle = None
            
###############
### Setters ###
###############   
 
    def setAllStatesOn(self):
        self._setAllStates(True)
    
    def setAllStatesOff(self):
        self._setAllStates(False)
     
    def setStates(self, states):
        for relay in states:
            self.setState(relay, states[relay])
    
    def setState(self, relay, on):
        self._checkInit()
        if relay>self.NUMRELAYS or relay<1:
            raise dae_RelayBoard_Common.Denkovi_Exception("Relay Index out of bound")
        stateByte = self._getStateByte()            
        toggle = 1 << self._getBitIndex(relay)
        if on:
            relState = stateByte | toggle
        else:
            relState = stateByte & ~toggle                       
        self._handleRet(self.FTD2XX.FT_Write(self.handle, chr(relState), 1))
    
    def _setAllStates(self, on):
        self._checkInit()
        if on:
            writeChar = chr(0xFF)
        else:
            writeChar = chr(0)
        self._handleRet(self.FTD2XX.FT_Write(self.handle, writeChar, 1))

###############
### Getters ###
###############  
                               
    def getStates(self):
        self._checkInit()
        stateByte = self._getStateByte()
        states = {}
        for relay in range(1, self.NUMRELAYS+1):
            states[relay] = self._getState(stateByte, relay)
        return states   
                               
    def getState(self, relay):
        self._checkInit()
        if relay>self.NUMRELAYS or relay<1:
            raise dae_RelayBoard_Common.Denkovi_Exception("Relay Index out of bound")
        stateByte = self._getStateByte()
        return self._getState(stateByte, relay)
    
    def _getState(self, stateByte, relay):
        if 1<<self._getBitIndex(relay) & stateByte:
            return True
        else:
            return False  
           
    def _getStateByte(self):
        ret, stateByte = self._handleRet(self.FTD2XX.FT_GetBitMode(self.handle))
        return stateByte   

###############
### Helpers ###
############### 
       
    def _handleRet(self, ret):
        if ret[0] != FT_OK:
            raise dae_RelayBoard_Common.Denkovi_Exception("FT return error: " + FTErrMap(ret[0]))
        return ret
    
    def _checkInit(self, checkHandle=True):
        if self.FTD2XX is None:
            raise dae_RelayBoard_Common.Denkovi_Exception("FTD2XX module not initialised")
        if checkHandle and self.handle is None:
            raise dae_RelayBoard_Common.Denkovi_Exception("No FT connection")
            
            
class DAE_RelayBoard_8(DAE_RelayBoard_D2XX):
    NUMRELAYS = 8

    def _getBitIndex(self, relay):
        return relay-1 
    
    
class DAE_RelayBoard_4(DAE_RelayBoard_D2XX):
    NUMRELAYS = 4

    def _getBitIndex(self, relay):
        return 2*relay-1 
           