#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Openid
# Copyright (C) 2010-2012 Hive Solutions Lda.
#
# This file is part of Hive Solutions Openid.
#
# Hive Solutions Openid is confidential and property of Hive Solutions Lda.,
# its usage is constrained by the terms of the Hive Solutions
# Confidential Usage License.
#
# Hive Solutions Openid should not be distributed under any circumstances,
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

__copyright__ = "Copyright (c) 2010-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

class ExceptionController:
    """
    The hive open id main exception controller.
    """

    hive_openid_plugin = None
    """ The hive openid plugin """

    hive_openid = None
    """ The hive openid """

    def __init__(self, hive_openid_plugin, hive_openid):
        """
        Constructor of the class.

        @type hive_openid_plugin: HiveOpenidPlugin
        @param hive_openid_plugin: The hive open id main plugin.
        @type hive_openid: HiveOpenid
        @param hive_openid: The hive open id main.
        """

        self.hive_openid_plugin = hive_openid_plugin
        self.hive_openid = hive_openid

    def handle_exception(self, rest_request, parameters = {}):
        """
        Handles an exception.

        @type rest_request: RestRequest
        @param rest_request: The rest request for which the exception occurred.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the exception parameters
        exception = parameters.get(EXCEPTION_VALUE)
        exception_message = exception.get(MESSAGE_VALUE)

        # processes the contents of the template file assigning the appropriate values to it
        template_file = self.retrieve_template_file("general.html.tpl", partial_page = "exception.html.tpl")
        template_file.assign("exception_message", exception_message)
        self.process_set_contents(rest_request, template_file, assign_session = True)
