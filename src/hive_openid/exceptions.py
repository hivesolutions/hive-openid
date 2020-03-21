#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions OpenID
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Solutions OpenID.
#
# Hive Solutions OpenID is confidential and property of Hive Solutions Lda.,
# its usage is constrained by the terms of the Hive Solutions
# Confidential Usage License.
#
# Hive Solutions OpenID should not be distributed under any circumstances,
# violation of this may imply legal action.
#
# If you have any questions regarding the terms of this license please
# refer to <http://www.hive.pt/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

class HiveOpenIDException(colony.ColonyException):
    """
    The Hive OpenID exception class.
    """

    message = None
    """ The exception's message """

class InvalidMode(HiveOpenIDException):
    """
    The invalid mode class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HiveOpenIDException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Invalid mode - %s" % self.message

class MissingProperty(HiveOpenIDException):
    """
    The missing property class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HiveOpenIDException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Missing property - %s" % self.message

class AuthenticationFailed(HiveOpenIDException):
    """
    The authentication failed class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HiveOpenIDException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "Authentication failed - %s" % self.message

class UserInformationError(HiveOpenIDException):
    """
    The user information error class.
    """

    def __init__(self, message):
        """
        Constructor of the class.

        :type message: String
        :param message: The message to be printed.
        """

        HiveOpenIDException.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.

        :rtype: String
        :return: The string representation of the class.
        """

        return "User information error - %s" % self.message
