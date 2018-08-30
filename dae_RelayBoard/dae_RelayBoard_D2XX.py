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

import sys
from . import dae_RelayBoard_Common

class DAE_RelayBoard_D2XX:
    BAUDRATE = 921600
    MASK = 255
    BITMODE = 4 
    
    def __init__(self):       
        if sys.platform == 'win32':
            from . import FTD2XXWindows
            self.FTD2XX = FTD2XXWindows.FTD2XXWindows()
        elif 'linux' in sys.platform:
            from . import FTD2XXLinux
            self.FTD2XX = FTD2XXLinux.FTD2XXLinux()
        
        
    #currently only gets first board
    def initialise(self, *args):
        self.disconnect()
        self._checkInit()
        deviceId = dae_RelayBoard_Common.DENKOVI_ID
        if len(args):
            deviceId = args[0]
        self.FTD2XX.initialise(deviceId, self.BAUDRATE, self.MASK, self.BITMODE)
    
    def disconnect(self):
        self._checkInit()
        self.FTD2XX.close()
            
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
            raise dae_RelayBoard_Common.Denkovi_Exception("Relay Index out of bounds")
        stateByte = self._readByte()            
        toggle = 1 << self._getBitIndex(relay)
        if on:
            relState = stateByte | toggle
        else:
            relState = stateByte & ~toggle                       
        self._writeByte(relState)
    
    def _setAllStates(self, on):
        self._checkInit()
        if on:
            writeChar = 0xFF
        else:
            writeChar = 0
        self._writeByte(writeChar)
           
    def _writeByte(self, byte):
        return self.FTD2XX.writeByte(byte)

###############
### Getters ###
###############  
                               
    def getStates(self):
        self._checkInit()
        stateByte = self._readByte()
        states = {}
        for relay in range(1, self.NUMRELAYS+1):
            states[relay] = self._getState(stateByte, relay)
        return states   
                               
    def getState(self, relay):
        self._checkInit()
        if relay>self.NUMRELAYS or relay<1:
            raise dae_RelayBoard_Common.Denkovi_Exception("Relay Index out of bounds")
        stateByte = self._readByte()
        return self._getState(stateByte, relay)
    
    def _getState(self, stateByte, relay):
        if 1<<self._getBitIndex(relay) & stateByte:
            return True
        else:
            return False  
           
    def _readByte(self):
        return self.FTD2XX.readByte()

###############
### Helpers ###
############### 
    
    def _checkInit(self):
        if self.FTD2XX is None:
            raise dae_RelayBoard_Common.Denkovi_Exception("FTD2XX module not initialised")
            
            
class DAE_RelayBoard_8(DAE_RelayBoard_D2XX):
    NUMRELAYS = 8

    def _getBitIndex(self, relay):
        return relay-1 
    
    
class DAE_RelayBoard_4(DAE_RelayBoard_D2XX):
    NUMRELAYS = 4

    def _getBitIndex(self, relay):
        return 2*relay-1 
           
