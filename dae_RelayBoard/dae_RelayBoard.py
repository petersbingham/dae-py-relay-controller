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

from . import dae_RelayBoard_Common

DAE_RELAYBOARD_TYPE_4 = "type4"
DAE_RELAYBOARD_TYPE_8 = "type8"
DAE_RELAYBOARD_TYPE_16 = "type16"

class DAE_RelayBoard:
    def __init__(self, boardType, *args):
        self.relayHandler = None
        self.CommString = False
        if boardType == DAE_RELAYBOARD_TYPE_16:
            from . import dae_RelayBoard_VCP
            self.CommString = True
            self.relayHandler = dae_RelayBoard_VCP.DAE_RelayBoard_16(*args)
        elif boardType == DAE_RELAYBOARD_TYPE_8:
            from . import dae_RelayBoard_D2XX
            self.relayHandler = dae_RelayBoard_D2XX.DAE_RelayBoard_8(*args)
        elif boardType == DAE_RELAYBOARD_TYPE_4:
            from . import dae_RelayBoard_D2XX
            self.relayHandler = dae_RelayBoard_D2XX.DAE_RelayBoard_4(*args)
        self._checkInit()

    def needsCommString(self):
        return self.CommString

    def initialise(self, *args):
        self._checkInit()
        self.relayHandler.initialise(*args)

    def disconnect(self):
        self._checkInit()
        self.relayHandler.disconnect()

    def getNumRelays(self):
        self._checkInit()
        return self.relayHandler.NUMRELAYS

###############
### Setters ###
###############

    def setAllStatesOn(self):
        self._checkInit()
        self.relayHandler.setAllStatesOn()

    def setAllStatesOff(self):
        self._checkInit()
        self.relayHandler.setAllStatesOff()

    def setStates(self, states):
        self.relayHandler.setStates(states)

    def setState(self, relay, on):
        self._checkInit()
        self.relayHandler.setState(relay, on)

###############
### Getters ###
###############

    def getStates(self):
        self._checkInit()
        return self.relayHandler.getStates()

    def getState(self, relay):
        self._checkInit()
        return self.relayHandler.getState(relay)

###############
### Helpers ###
###############

    def _checkInit(self):
        if self.relayHandler is None:
            raise dae_RelayBoard_Common.Denkovi_Exception("No supported board has been successfully initialised")

