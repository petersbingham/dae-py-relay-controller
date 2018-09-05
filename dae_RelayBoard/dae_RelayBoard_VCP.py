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

import serial
import time
from . import dae_RelayBoard_Common

class DAE_RelayBoard_VCP:
    TIMEOUT = 1.0
    DELIM = "//"
    DEFAULT_CMDDELAY = 0.05 #Can override this default with zero and control delay in client code. Says 5ms but was getting corruption even around 20ms, so increased to 50ms. See test16Intervals.
        
    def __init__(self, *args): 
        if len(args)>0:
            self.cmdDelay = args[0]
        else:
            self.cmdDelay = self.DEFAULT_CMDDELAY
        self.ser = None
        
    def initialise(self, *args):
        self.disconnect()
        self.portstring = args[0]
        self.ser = self._connectToSerial()   
    
    def disconnect(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
        
    def _connectToSerial(self):    
        try:
            return serial.Serial(
                port=self.portstring,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                xonxoff=0,             # no software flow control
                rtscts=0,              # no RTS/CTS flow control        
                timeout=self.TIMEOUT,
                writeTimeout=self.TIMEOUT
            )
        except serial.SerialException:
            raise dae_RelayBoard_Common.Denkovi_Exception("Could not connect to relay board")

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
        if relay>self.NUMRELAYS or relay<1:
            raise dae_RelayBoard_Common.Denkovi_Exception("Relay Index out of bound")
        else:
            self._prepForCmd()
            if on:
                stateString = "+"
            else:
                stateString = "-"
            numString = "%02d" % relay
            self._write(numString+stateString)

    def _setAllStates(self, on):
        self._prepForCmd()
        if on:
            stateString = "on"
        else:
            stateString = "off"
        self._write(stateString)

###############
### Getters ###
############### 
                               
    def getStates(self):
        self._prepForCmd()   
        stateString = self._getStateString()
        states = {}
        for relay in range(1, self.NUMRELAYS+1):
            states[relay] = self._getState(relay, stateString)
        return states
                               
    def getState(self, relay):
        if relay>self.NUMRELAYS or relay<1:
            raise dae_RelayBoard_Common.Denkovi_Exception("Relay Index out of bound")
        else:
            self._prepForCmd()   
            stateString = self._getStateString()
            return self._getState(relay, stateString)

    def _getStateString(self):
        self._write("ask")
        time.sleep(self.cmdDelay)
        return self._read(2)
    
    def _getState(self, relay, stateString):
        if relay>self.NUMRELAYS/2:
            stateStringIndex = 1
            shifts = relay - self.NUMRELAYS/2 - 1
        else:
            stateStringIndex = 0
            shifts = relay - 1
            
        field = 128 >> int(shifts)
        try:
            return field & ord(stateString[stateStringIndex]) > 0 #Python 2
        except TypeError:
            return field & stateString[stateStringIndex] > 0      #Python 3

###############
### Helpers ###
############### 
        
    def _prepForCmd(self):
        if self.ser == None:
            raise dae_RelayBoard_Common.Denkovi_Exception("Board Not Initialised")
        else:
            time.sleep(self.cmdDelay)
            self.ser.flushInput()
            self.ser.flushOutput()
        
    def _write(self, cmdString):
        try:
            writeString = cmdString+self.DELIM
            bytesWritten = self.ser.write(writeString.encode())
            if len(writeString) != bytesWritten:
                raise dae_RelayBoard_Common.Denkovi_Exception("Error during write")
        except (serial.SerialException, serial.SerialTimeoutException):
            raise dae_RelayBoard_Common.Denkovi_Exception("Error while writing")
                    
    def _read(self, numBytes):
        try:
            retString = self.ser.read(size=numBytes)
            if len(retString) < numBytes:
                raise dae_RelayBoard_Common.Denkovi_Exception("Timeout waiting for response")
            return retString
        except (serial.SerialException, serial.SerialTimeoutException):
            raise dae_RelayBoard_Common.Denkovi_Exception("Error while writing")

class DAE_RelayBoard_16(DAE_RelayBoard_VCP):
    NUMRELAYS = 16
                