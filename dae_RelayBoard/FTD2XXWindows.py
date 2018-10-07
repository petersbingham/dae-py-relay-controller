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

from . import FTD2XXDllWrap
from . import dae_RelayBoard_Common

class FTD2XXWindows(object):
    def __init__(self):
        self.handle = None
        self.FTD2XXDLL = FTD2XXDllWrap.FTD2XXDllWrap()
 
    def initialise(self, deviceID, baudRate, mask, bitMode):
        self.handle = self._handleRet(self.FTD2XXDLL.initSpecified(deviceID))[1]
        self._checkInit()
        self._handleRet(self.FTD2XXDLL.FT_SetBaudRate(self.handle, baudRate))
        self._handleRet(self.FTD2XXDLL.FT_SetBitMode(self.handle, mask, bitMode))
 
    def close(self):
        if self.handle is not None:
            self._handleRet(self.FTD2XXDLL.FT_Close(self.handle))
            self.handle = None
        
    def writeByte(self, byte):
        self._checkInit()
        self._handleRet(self.FTD2XXDLL.FT_Write(self.handle, byte, 1))
 
    def readByte(self):
        self._checkInit()
        return self._handleRet(self.FTD2XXDLL.FT_GetBitMode(self.handle))[1]
    
    def _checkInit(self):
        if self.handle is None:
            raise dae_RelayBoard_Common.Denkovi_Exception("FTD2XXWindows device not initialised")
       
    def _handleRet(self, ret):
        if ret[0] != FTD2XXDllWrap.FT_OK:
            raise dae_RelayBoard_Common.Denkovi_Exception(self._getErrString(ret))
        return ret
    
    def _getErrString(self, ret):
        return "FT return error: " + FTD2XXDllWrap.FTDllErrMap(ret[0])
        