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

from ctypes import *

FT_OK = 0
FT_INVALID_HANDLE = 1
FT_DEVICE_NOT_FOUND = 2
FT_DEVICE_NOT_OPENED = 3
FT_IO_ERROR = 4
FT_INSUFFICIENT_RESOURCES = 5
FT_INVALID_PARAMETER = 6
FT_INVALID_BAUD_RATE = 7
FT_DEVICE_NOT_OPENED_FOR_ERASE = 8
FT_DEVICE_NOT_OPENED_FOR_WRITE = 9
FT_FAILED_TO_WRITE_DEVICE = 10
FT_EEPROM_READ_FAILED = 11
FT_EEPROM_WRITE_FAILED = 12
FT_EEPROM_ERASE_FAILED = 13
FT_EEPROM_NOT_PRESENT = 14
FT_EEPROM_NOT_PROGRAMMED = 15
FT_INVALID_ARGS = 16
FT_NOT_SUPPORTED = 17
FT_OTHER_ERROR = 18

def FTDllErrMap(errCode):
    return {
        FT_OK : "FT_OK",
        FT_INVALID_HANDLE : "FT_INVALID_HANDLE",
        FT_DEVICE_NOT_FOUND : "FT_DEVICE_NOT_FOUND",
        FT_DEVICE_NOT_OPENED : "FT_DEVICE_NOT_OPENED",
        FT_IO_ERROR : "FT_IO_ERROR",
        FT_INSUFFICIENT_RESOURCES : "FT_INSUFFICIENT_RESOURCES",
        FT_INVALID_PARAMETER : "FT_INVALID_PARAMETER",
        FT_INVALID_BAUD_RATE : "FT_INVALID_BAUD_RATE",
        FT_DEVICE_NOT_OPENED_FOR_ERASE : "FT_DEVICE_NOT_OPENED_FOR_ERASE",
        FT_DEVICE_NOT_OPENED_FOR_WRITE : "FT_DEVICE_NOT_OPENED_FOR_WRITE",
        FT_FAILED_TO_WRITE_DEVICE : "FT_FAILED_TO_WRITE_DEVICE",
        FT_EEPROM_READ_FAILED : "FT_EEPROM_READ_FAILED",
        FT_EEPROM_WRITE_FAILED : "FT_EEPROM_WRITE_FAILED",
        FT_EEPROM_ERASE_FAILED : "FT_EEPROM_ERASE_FAILED",
        FT_EEPROM_NOT_PRESENT : "FT_EEPROM_NOT_PRESENT",
        FT_EEPROM_NOT_PROGRAMMED : "FT_EEPROM_NOT_PROGRAMMED",
        FT_INVALID_ARGS : "FT_INVALID_ARGS",
        FT_NOT_SUPPORTED : "FT_NOT_SUPPORTED",
        FT_OTHER_ERROR : "FT_OTHER_ERROR"
    }.get(errCode , "Unknown Error Code: " + str(errCode))

FT_LIST_NUMBER_ONLY = 0x80000000
FT_LIST_BY_INDEX = 0x40000000
FT_LIST_ALL = 0x20000000

FT_OPEN_BY_SERIAL_NUMBER = 1
FT_OPEN_BY_DESCRIPTION = 2
FT_OPEN_BY_LOCATION = 4

MAX_BUFF_SZ = 64

class FTD2XXDllWrap(object):
    def __init__(self):
        self.FTD2XXDLL = WinDLL("FTD2XX.dll")
 
    def FT_Open(self, deviceNum):
        handle = c_void_p()
        ret = self.FTD2XXDLL.FT_Open(deviceNum, pointer(handle))
        return (ret, handle)
 
    def FT_Close(self, handle):
        ret = self.FTD2XXDLL.FT_Close(handle)
        return (ret,)

    def FT_Write(self, handle, buff, numBytes):
        buff = pointer(c_byte(buff))
        bytesWritten = c_int()
        ret = self.FTD2XXDLL.FT_Write(handle, cast(buff,c_void_p), numBytes, pointer(bytesWritten))
        return (ret, bytesWritten)
 
    def FT_Read(self, handle, numBytes):
        buff = (c_char * numBytes)()
        ret = self.FTD2XXDLL.FT_Read(handle, cast(buff,c_void_p), numBytes)
        string = ""
        for i in range(0,numBytes):
            string += buff[i]
        return (ret, string)        
        
    def FT_GetNumDevices(self):
        numDevs = c_int()
        ret = self.FTD2XXDLL.FT_CreateDeviceInfoList(byref(numDevs))
        return (ret, numDevs.value)  
        
    def FT_GetDeviceDescription(self, index):
        return self._getBuffer(index, FT_OPEN_BY_DESCRIPTION)
        
    def FT_GetDeviceSerialNumber(self, index):
        return self._getBuffer(index, FT_OPEN_BY_SERIAL_NUMBER)
    
    def _getBuffer(self, index, flag):
        index = c_void_p(index)
        buff = (c_char * MAX_BUFF_SZ)()
        ret = self.FTD2XXDLL.FT_ListDevices(index, cast(buff,c_void_p), FT_LIST_BY_INDEX|flag)
        string = ""
        for i in range(0,MAX_BUFF_SZ):
            if buff[i] != "\x00":
                string += buff[i].decode()
        return (ret, string)
    
    def FT_SetBitMode(self, handle, mask, enable):
        ret = self.FTD2XXDLL.FT_SetBitMode(handle, mask, enable)
        return (ret,)
    
    def FT_SetBaudRate(self, handle, baudRate):
        ret = self.FTD2XXDLL.FT_SetBaudRate(handle, baudRate)
        return (ret,)
   
    def FT_GetBitMode(self, handle):
        charBuff = c_ubyte()
        ret = self.FTD2XXDLL.FT_GetBitMode(handle, pointer(charBuff))
        return (ret, charBuff.value)
    
    def FT_ResetDevice (self, handle):
        ret = self.FTD2XXDLL.FT_ResetDevice(handle)
        return (ret,)
    
    
###############
### Helpers ###
############### 

    def initFirst(self, idString):
        ret, numDevs = self.FT_GetNumDevices()
        if ret==FT_OK:
            for i in range(0, numDevs):
                ret, SN = self.FT_GetDeviceSerialNumber(i)
                if ret==FT_OK:
                    if idString.upper() in SN.upper():
                        return self.FT_Open(i)
            return (ret, None)
        else:
            return (ret, None)

    def initSpecified(self, idString):
        indexed = idString.split("#", 2)
        if len(indexed) == 2:
            idString = indexed[0]
            which = int(indexed[1])
        else:
            which = 0

        index = 0
        ret, numDevs = self.FT_GetNumDevices()
        if ret==FT_OK:
            for i in range(0, numDevs):
                ret, SN = self.FT_GetDeviceSerialNumber(i)
                if ret==FT_OK:
                    if idString.upper() in SN.upper():
                        if which == index:
                            return self.FT_Open(i)
                        index += 1
            return (ret, None)
        else:
            return (ret, None)
