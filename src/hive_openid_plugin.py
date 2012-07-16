#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Openid
# Copyright (C) 2010 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2010 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class HiveOpenidPlugin(colony.base.system.Plugin):
    """
    The main class for the Hive Openid Main plugin.
    """

    id = "pt.hive.cronus.plugins.hive_openid"
    name = "Hive Openid"
    description = "The plugin that offers the hive openid provider"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "web.mvc_service"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.mvc.utils", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.api.openid", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.authentication", "1.x.x"),
        colony.base.system.PluginDependency("pt.hive.colony.plugins.information.user", "1.x.x")
    ]
    main_modules = [
        "hive_openid.exceptions",
        "hive_openid.system"
    ]

    hive_openid = None
    """ The hive openid """

    mvc_utils_plugin = None
    """ The web mvc utils plugin """

    api_openid_plugin = None
    """ The api openid plugin """

    authentication_plugin = None
    """ The main authentication plugin """

    information_user_plugin = None
    """ The information user plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import hive_openid.system
        self.hive_openid = hive_openid.system.HiveOpenid(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)
        self.hive_openid.load_components()

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)
        self.hive_openid.unload_components()

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.system.Plugin.unset_configuration_property(self, property_name)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return self.hive_openid.get_patterns()

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return self.hive_openid.get_communication_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return self.hive_openid.get_resource_patterns()

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.mvc.utils")
    def set_mvc_utils_plugin(self, mvc_utils_plugin):
        self.mvc_utils_plugin = mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.api.openid")
    def set_api_openid_plugin(self, api_openid_plugin):
        self.api_openid_plugin = api_openid_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.authentication")
    def set_authentication_plugin(self, authentication_plugin):
        self.authentication_plugin = authentication_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.information.user")
    def set_information_user_plugin(self, information_user_plugin):
        self.information_user_plugin = information_user_plugin

    @colony.base.decorators.set_configuration_property_method("service_configuration")
    def service_configuration_set_configuration_property(self, property_name, property):
        self.hive_openid.set_service_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("service_configuration")
    def service_configuration_unset_configuration_property(self, property_name):
        self.hive_openid.unset_service_configuration_property()
