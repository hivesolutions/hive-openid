#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Openid
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

class HiveOpenid(colony.System):
    """
    The hive openid class.
    """

    authentication_properties_map = {}
    """ The authentication properties map, this is the map
    that contains the configuration that is going to be used
    at runtime to "guide" the authentication process """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.authentication_properties_map = {}

    def load_components(self):
        """
        Loads the main components models, controllers, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # creates the controllers and assigns them to the current instance
        # allowing them to start being used in the current workflow
        mvc_utils_plugin.assign_controllers(self, self.plugin)

    def unload_components(self):
        """
        Unloads the main components models, controllers, etc.
        This load should occur the earliest possible in the unloading process.
        """

        # retrieves the mvc utils plugin
        mvc_utils_plugin = self.plugin.mvc_utils_plugin

        # destroys the controllers, unregistering them from the internal
        # structures, this should prevent any more usage of the controllers
        mvc_utils_plugin.unassign_controllers(self)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the mvc service.
        """

        return (
            (r"hive_openid/?", self.main_controller.index, "get"),
            (r"hive_openid/index", self.main_controller.index, "get"),
            (r"hive_openid/users/<str:username>", self.main_controller.user_vcard, "get", "vcf"),
            (r"hive_openid/users/<str:username>", self.main_controller.user, "get"),
            (r"hive_openid/signin", self.main_controller.signin, "get"),
            (r"hive_openid/allow", self.main_controller.allow, "get"),
            (r"hive_openid/approve", self.main_controller.approve, "get"),
            (r"hive_openid/server", self.main_controller.server, ("get", "post")),
            (r"hive_openid/xrds", self.main_controller.xrds, "get"),
            (r"hive_openid/login", self.main_controller.login, "post"),
            (r"hive_openid/logout", self.main_controller.logout, "get"),
            (r"hive_openid/redirect", self.main_controller.redirect_do, "get"),
            (r"hive_openid/<str:username>", self.main_controller.user_vcard, "get", "vcf"),
            (r"hive_openid/<str:username>", self.main_controller.user, "get")
        )

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        # retrieves the plugin manager and uses it to retrieve
        # the colony site plugin path
        plugin_manager = self.plugin.manager
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)

        return (
            (r"hive_openid/resources/.+", (plugin_path + "/hive_openid/resources/extras", "hive_openid/resources")),
        )

    def set_service_configuration_property(self, service_configuration_propery):
        # retrieves the service configuration and extracts the proper
        # authentication information from it setting it under the system
        service_configuration = service_configuration_propery.get_data()
        authentication_properties_map = service_configuration["authentication_properties"]
        self.authentication_properties_map = authentication_properties_map

    def unset_service_configuration_property(self):
        # unsets the authentication properties map, restoring it to the
        # original invalid/empty value that does not provide authentication
        self.authentication_properties_map = {}
