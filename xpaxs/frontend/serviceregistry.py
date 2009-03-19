"""
"""

import logging
import sys
import os

from PyQt4 import QtCore, QtGui


logger = logging.getLogger(__name__)

# TODO: this is an attempt to provide a services registry similar to that in
# Enthought's envisage framework. This is a simple implementation designed to
# allow xpaxs to be structured such that porting to envisage will be possible
# at some point in the future.

class ServiceRegistry:

    def __init__(self):

        self._services = {}

        self._serviceId = 0

    def registerService(self, protocol, obj, properties=None):
        if properties is None:
            properties = {}

        serviceId = self._nextServiceId()
        self._services[serviceId] = (protocol, obj, properties)

        logger.debug('service <%d> registered %s', serviceId, protocol)

        return serviceId

    def getService(self, protocol):
        services = self.getServices(protocol)
        if len(services) > 0:
            service = services[0]

        else:
            service = None

        return service

    def getServices(self, protocol):
        services = []
        for service_id, (name, obj, properties) in self._services.items():
            if name == protocol:
                services.append(obj)

        return services

    def unregisterService(self, serviceId):
        try:
            del self._services[serviceId]

            logger.debug('service <%d> unregistered', serviceId)

        except KeyError:
            raise ValueError('no service with id <%d>' % serviceId)

    def _nextServiceId(self):
        """ Returns the next service ID. """

        self._serviceId += 1

        return self._serviceId
