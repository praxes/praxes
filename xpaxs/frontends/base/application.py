"""
"""

#---------------------------------------------------------------------------
# Stdlib imports
#---------------------------------------------------------------------------

import logging
import sys
import os

#---------------------------------------------------------------------------
# Extlib imports
#---------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui

#---------------------------------------------------------------------------
# xpaxs imports
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------
# Normal code begins
#---------------------------------------------------------------------------


# TODO: this is an attempt to provide a services registry similar to that in
# Enthought's envisage framework. This is a simple implementation designed to
# allow xpaxs to be structured such that porting to envisage will be possible
# at some point in the future.

class XpaxsApplication:

    class __impl(QtGui.QApplication):
        """ Implementation of the singleton interface """

        def __init__(self, args=None):
            if args is None:
                args = sys.argv

            QtGui.QApplication.__init__(self, args)

            from xpaxs.frontends.base.serviceregistry import ServiceRegistry
            self._serviceRegistry = ServiceRegistry()

        @property
        def serviceRegistry(self):
            return self._serviceRegistry

        def registerService(self, protocol, obj):
            return self._serviceRegistry.registerService(protocol, obj)

        def getService(self, protocol):
            return self._serviceRegistry.getService(protocol)

        def unregisterService(self, serviceId):
            self._serviceRegistry.unregisterService(serviceId)

    # storage for the instance reference
    __instance = None

    def __init__(self, args=None):
        """ Create singleton instance """
        # Check whether we already have an instance
        if XpaxsApplication.__instance is None:
            # Create and remember instance
            XpaxsApplication.__instance = XpaxsApplication.__impl(args)

            import xpaxs
            xpaxs.application = XpaxsApplication.__instance

        # Store instance reference as the only member in the handle
        self.__dict__['_XpaxsApplication__instance'] = XpaxsApplication.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


def main():
    import sys
    app = XpaxsApplication(sys.argv)

    import xpaxs

    print dir(QtGui.qApp)
    print dir(xpaxs.application)

    form = QtGui.QWidget()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
