"""
"""
from __future__ import absolute_import

#import logging
import sys
import os

from PyQt4 import QtCore, QtGui


# TODO: this is an attempt to provide a services registry similar to that in
# Enthought's envisage framework. This is a simple implementation designed to
# allow praxes to be structured such that porting to envisage will be possible
# at some point in the future.

class PraxesApplication:

    class __impl(QtGui.QApplication):
        """ Implementation of the singleton interface """

        def __init__(self, args=None):
            if args is None:
                args = sys.argv

            QtGui.QApplication.__init__(self, args)

            from .serviceregistry import ServiceRegistry
            self._serviceRegistry = ServiceRegistry()

            self.openViews = []

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
        if PraxesApplication.__instance is None:
            # Create and remember instance
            PraxesApplication.__instance = PraxesApplication.__impl(args)

            import praxes
            praxes.application = PraxesApplication.__instance

        # Store instance reference as the only member in the handle
        self.__dict__['_PraxesApplication__instance'] = PraxesApplication.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


#def main():
#    import sys
#    app = PraxesApplication(sys.argv)
#
#    import praxes
#
#    print dir(QtGui.qApp)
#    print dir(praxes.application)
#
#    form = QtGui.QWidget()
#    form.show()
#    sys.exit(app.exec_())
#
#
#if __name__ == "__main__":
#    main()
