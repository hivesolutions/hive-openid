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

import colony.libs.import_util

import hive_openid.exceptions

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

NAMESPACE_NAME = "pt.hive.cronus.plugins.hive_openid"
""" The namespace name """

OPENID_NAMESPACE_VALUE = "http://specs.openid.net/auth/2.0"
""" The openid namespace value """

ASSOCIATE_VALUE = "associate"
""" The associate value """

CHECKID_SETUP_VALUE = "checkid_setup"
""" The checkid setup value """

CHECK_AUTHENTICATION_VALUE = "check_authentication"
""" The check authentication value """

X_RDS_LOCATION_VALUE = "X-XRDS-Location"
""" The x rds location value """

AUTHENTICATION_HANDLER_VALUE = "authentication_handler"
""" The authentication handler value """

EXCEPTION_VALUE = "exception"
""" The exception value """

MESSAGE_VALUE = "message"
""" The message value """

ARGUMENTS_VALUE = "arguments"
""" The arguments value """

USERNAME_VALUE = "username"
""" The username value """

PASSWORD_VALUE = "password"
""" The password value """

MODE_VALUE = "mode"
""" The mode value """

VALID_VALUE = "valid"
""" The valid value """

INVALID_VALUE = "invalid"
""" The invalid value """

OPENID_VALUE = "openid"
""" The openid value """

OPENID_USER_VALUE = "openid_user"
""" The openid user value """

OPENID_USER_INFORMATION_VALUE = "openid_user_information"
""" The openid user information value """

OPENID_SERVER_VALUE = "openid_server"
""" The openid server value """

OPENID_USER_BASE_VALUE = "openid_user_base"
""" The openid base value """

mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class MainController(controllers.Controller):
    """
    The main controller.
    """

    association_handle_openid_server_map = {}
    """ The map associating the association handle
    with the openid server """

    def __init__(self, plugin, system):
        controllers.Controller.__init__(self, plugin, system)
        self.association_handle_openid_server_map = {}

    @mvc_utils.serialize
    def handle_index(self, rest_request, parameters = {}):
        """
        Handles the given index rest request.

        @type rest_request: RestRequest
        @param rest_request: The index rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "index_contents.html.tpl"
        )
        self._assign_base(rest_request, template_file)
        self.process_set_contents(rest_request, template_file, assign_session = True)

    @mvc_utils.serialize
    def handle_user(self, rest_request, parameters = {}):
        """
        Handles the given user rest request.

        @type rest_request: RestRequest
        @param rest_request: The user rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the info user plugin
        info_user_plugin = self.plugin.info_user_plugin

        # retrieves the openid user pattern
        openid_user = self.get_pattern(parameters, OPENID_USER_VALUE)

        # retrieves the host path for the xrds path as the openid xrds address
        openid_xrds = self._get_host_path(rest_request, "/xrds?openid_user=" + openid_user)

        # retrieves the user information from the info user plugin
        # using the openid user
        openid_user_information = info_user_plugin.get_user_info(openid_user)

        # in case the openid user information is not found
        if not openid_user_information:
            # raises a user information error
            raise hive_openid.exceptions.UserInformationError("user information not found")

        # sets the xrds header value
        rest_request.set_header(X_RDS_LOCATION_VALUE, openid_xrds)

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "user_contents.html.tpl"
        )
        template_file.assign(OPENID_USER_VALUE, openid_user)
        template_file.assign(OPENID_USER_INFORMATION_VALUE, openid_user_information)
        self._assign_base(rest_request, template_file)
        self.process_set_contents(rest_request, template_file, assign_session = True)

    @mvc_utils.serialize
    def handle_user_vcard(self, rest_request, parameters = {}):
        """
        Handles the given user vcard rest request.

        @type rest_request: RestRequest
        @param rest_request: The user vcard rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the info user plugin
        info_user_plugin = self.plugin.info_user_plugin

        # retrieves the openid user pattern
        openid_user = self.get_pattern(parameters, OPENID_USER_VALUE)

        # retrieves the user information from the info user plugin
        # using the openid user
        openid_user_information = info_user_plugin.get_user_info(openid_user)

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file("vcard.vcf.tpl")
        template_file.assign(OPENID_USER_VALUE, openid_user)
        template_file.assign(OPENID_USER_INFORMATION_VALUE, openid_user_information)
        self._assign_base(rest_request, template_file)
        self.process_set_contents(rest_request, template_file, assign_session = True, content_type = "text/x-vcard")

    @mvc_utils.serialize
    def handle_signin(self, rest_request, parameters = {}):
        """
        Handles the given signin request.

        @type rest_request: RestRequest
        @param rest_request: The signin rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
             partial_page = "signin_contents.html.tpl"
        )
        self._assign_base(rest_request, template_file)
        self.process_set_contents(rest_request, template_file, assign_session = True)

    @mvc_utils.serialize
    def handle_allow(self, rest_request, parameters = {}):
        """
        Handles the given allow request.

        @type rest_request: RestRequest
        @param rest_request: The allow rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "allow_contents.html.tpl"
        )
        self._assign_base(rest_request, template_file)
        self.process_set_contents(rest_request, template_file, assign_session = True)

    @mvc_utils.serialize
    def handle_approve(self, rest_request, parameters = {}):
        """
        Handles the given approve request.

        @type rest_request: RestRequest
        @param rest_request: The approve rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # processes the contents of the template file assigning the
        # appropriate values to it
        template_file = self.retrieve_template_file(
            "general.html.tpl",
            partial_page = "approve_contents.html.tpl"
        )
        self._assign_base(rest_request, template_file)
        self.process_set_contents(rest_request, template_file, assign_session = True)

    @mvc_utils.serialize
    def handle_server(self, rest_request, parameters = {}):
        """
        Handles the given server rest request.

        @type rest_request: RestRequest
        @param rest_request: The server rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data_flat(rest_request, DEFAULT_ENCODING)

        # retrieves the openid data
        openid_data = form_data_map.get(OPENID_VALUE, {})

        # retrieves the openid mode
        openid_mode = openid_data.get(MODE_VALUE, INVALID_VALUE)

        # prints a debug message
        self.plugin.debug("Receiving request '%s' from client" % openid_mode)

        # in case it's is a post request (associate)
        if openid_mode == ASSOCIATE_VALUE:
            # processes the associate
            return self.process_associate(rest_request, openid_data)
        elif openid_mode == CHECKID_SETUP_VALUE:
            # processes the checkid setup
            return self.process_check_id_setup(rest_request, openid_data)
        elif openid_mode == CHECK_AUTHENTICATION_VALUE:
            # processes the check authentication
            return self.process_check_authentication(rest_request, openid_data)
        else:
            # raises the invalid mode exception
            raise hive_openid.exceptions.InvalidMode(openid_mode)

    @mvc_utils.serialize
    def handle_xrds(self, rest_request, parameters = {}):
        """
        Handles the given xrds rest request.

        @type rest_request: RestRequest
        @param rest_request: The xrds rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request)

        # retrieves the openid data
        openid_user = form_data_map.get(OPENID_USER_VALUE, INVALID_VALUE)

        # retrieves the host path for the server path as the openid server address
        openid_server = self._get_host_path(rest_request, "/server")

        # retrieves the host path for the user base path as the openid user base address
        openid_user_base = self._get_host_path(rest_request, "/" + openid_user)

        # retrieves the template file
        template_file = self.retrieve_template_file("xrds.xml.tpl")

        # assigns the template variables
        template_file.assign(OPENID_SERVER_VALUE, openid_server)
        template_file.assign(OPENID_USER_BASE_VALUE, openid_user_base)

        # processes the template file
        processed_template_file = self.process_template_file(rest_request, template_file)

        # sets the request contents
        self.set_contents(rest_request, processed_template_file, "application/xrds+xml")

    @mvc_utils.serialize
    def handle_login(self, rest_request, parameters = {}):
        """
        Handles the given login request.

        @type rest_request: RestRequest
        @param rest_request: The login rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data_flat(rest_request, DEFAULT_ENCODING)

        # processes the login, retrieving the authentication user information
        authentication_user_information = self.process_login(rest_request, form_data_map)

        # in case the authentication was successful, the user must be
        # logged in the current account for the current session
        if authentication_user_information:
            # sets both the login flag attribute and the user information
            # (dictionary value) in the current session to be used for latter
            # configuration and model control (required for authentication)
            self.set_session_attribute(
                rest_request,
                "login",
                True,
                NAMESPACE_NAME
            )
            self.set_session_attribute(
                rest_request,
                "user_information",
                authentication_user_information,
                NAMESPACE_NAME
            )

        # otherwise the user must be removed from the current session in
        # other to avoid any possible side problem
        else:
            # unsets the login attribute in the session
            self.set_session_attribute(
                rest_request,
                "login",
                False,
                NAMESPACE_NAME
            )

        # retrieves the openid server from the session attribute
        openid_server = self.get_session_attribute(rest_request, "openid_server", NAMESPACE_NAME)

        # in case there is an openid validation pending
        if openid_server:
            # retrieves the openid structure
            openid_structure = openid_server.get_openid_structure()

            # retrieves the username from the
            username = openid_structure.get_username_claimed_id()

            # retrieves the authentication user information username
            authentication_user_information_username = authentication_user_information.get(USERNAME_VALUE, None)

            # in case the username is not the same as the authentication
            # user information username
            if not username == authentication_user_information_username:
                # raises the user information error
                raise hive_openid.exceptions.UserInformationError("invalid username for openid claimed id")

            # processes the request in the server
            openid_server.openid_request()

        # redirects to the redirect page
        self.redirect_base_path(rest_request, "redirect")

    @mvc_utils.serialize
    def handle_logout(self, rest_request, parameters = {}):
        """
        Handles the given logout request.

        @type rest_request: RestRequest
        @param rest_request: The logout rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # unsets the login attribute in the session
        self.set_session_attribute(rest_request, "login", False, NAMESPACE_NAME)

        # redirects to the user page
        self.redirect_base_path(rest_request, "index")

    @mvc_utils.serialize
    def handle_redirect(self, rest_request, parameters = {}):
        """
        Handles the given redirect request.

        @type rest_request: RestRequest
        @param rest_request: The redirect rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the login session attribute
        login = self.get_session_attribute(rest_request, "login", NAMESPACE_NAME)

        # in case the user is not logged in
        if not login:
            # redirects to the signin page
            self.redirect_base_path(rest_request, "signin")

        # retrieves the openid server from the session attribute
        openid_server = self.get_session_attribute(rest_request, "openid_server", NAMESPACE_NAME)

        # in case the openid server is defined
        if openid_server:
            # retrieves the return url from the openid server
            return_url = openid_server.get_return_url()

            # redirects to the return url page
            self.redirect_base_path(rest_request, return_url, quote = False)
        else:
            # redirects to the index page
            self.redirect_base_path(rest_request, "index")

        # unsets the openid server as session attribute
        self.unset_session_attribute(rest_request, "openid_server", NAMESPACE_NAME)

    def process_login(self, rest_request, user_data):
        # retrieves the main authentication plugin
        authentication_plugin = self.plugin.authentication_plugin

        # retrieves the info user plugin
        info_user_plugin = self.plugin.info_user_plugin

        # retrieves the authentication properties map
        authentication_properties_map = self.system.authentication_properties_map

        # in case the authentication handler property is not defined
        if not AUTHENTICATION_HANDLER_VALUE in authentication_properties_map:
            # raises the missing property exception
            raise hive_openid.exceptions.MissingProperty(AUTHENTICATION_HANDLER_VALUE)

        # in case the arguments property is not defined
        if not ARGUMENTS_VALUE in authentication_properties_map:
            # raises the missing property exception
            raise hive_openid.exceptions.MissingProperty(ARGUMENTS_VALUE)

        # retrieves the username
        username = user_data.get(USERNAME_VALUE, None)

        # retrieves the password
        password = user_data.get(PASSWORD_VALUE, None)

        # retrieves the authentication handler
        authentication_handler = authentication_properties_map[AUTHENTICATION_HANDLER_VALUE]

        # retrieves the arguments
        arguments = authentication_properties_map[ARGUMENTS_VALUE]

        # authenticates the user with the main authentication plugin retrieving the result
        authentication_result = authentication_plugin.authenticate_user(username, password, authentication_handler, arguments)

        # retrieves the authentication result
        authentication_result_valid = authentication_result.get(VALID_VALUE, False)

        # in case the authentication fails
        if not authentication_result_valid:
            # retrieves the authentication result exception
            authentication_result_exception = authentication_result.get(EXCEPTION_VALUE, {})

            # retrieves the authentication result exception message
            authentication_result_exception_message = authentication_result_exception.get(MESSAGE_VALUE, "undefined error")

            # raises the authentication failed exception
            raise hive_openid.exceptions.AuthenticationFailed(authentication_result_exception_message)

        # retrieves the authentication username
        authentication_username = authentication_result.get(USERNAME_VALUE, None)

        # retrieves the user information from the info user plugin
        # using the authentication username
        authentication_user_information = info_user_plugin.get_user_info(authentication_username)

        # in case there is no authentication user information
        if not authentication_user_information:
            # raises the user information error
            raise hive_openid.exceptions.UserInformationError("missing user information")

        # returns the authentication user information
        return authentication_user_information

    def process_associate(self, rest_request, openid_data):
        # retrieves the api openid plugin
        api_openid_plugin = self.plugin.api_openid_plugin

        # creates the openid server
        openid_server = api_openid_plugin.create_server({})

        # retrieves the provider url
        provider_url = self._get_provider_url(rest_request)

        # retrieves the openid attributes
        association_type = openid_data["assoc_type"]
        session_type = openid_data["session_type"]

        # retrieves the diffie hellman attributes
        prime_value = openid_data.get("dh_modulus", None)
        base_value = openid_data.get("dh_gen", None)
        consumer_public = openid_data.get("dh_consumer_public", None)

        # generates the openid structure
        openid_server.generate_openid_structure(provider_url, association_type, session_type, prime_value, base_value, consumer_public)

        # associates the server and the provider, retrieving the
        # openid structure
        openid_structure = openid_server.openid_associate()

        # retrieves the openid association handle
        openid_association_handle = openid_structure.get_association_handle()

        # retrieves the encoded response parameters
        encoded_response_parameters = openid_server.get_encoded_response_parameters()

        # sets the request contents
        self.set_contents(rest_request, encoded_response_parameters, "text/plain")

        # sets the openid server in the association handle
        # openid server map for later retrieval
        self.association_handle_openid_server_map[openid_association_handle] = openid_server

        # returns true
        return True

    def process_check_id_setup(self, rest_request, openid_data):
        # retrieves the login session attribute
        login = self.get_session_attribute(rest_request, "login", NAMESPACE_NAME)

        # retrieves the user information attribute
        user_information = self.get_session_attribute(rest_request, "user_information", NAMESPACE_NAME)

        # retrieves the user information username
        user_information_username = user_information and user_information.get(USERNAME_VALUE, None) or None

        # retrieves the openid attributes
        identity = openid_data["identity"]
        claimed_id = openid_data.get("claimed_id", identity)
        association_handle = openid_data.get("assoc_handle", None)
        return_to = openid_data["return_to"]
        realm = openid_data.get("realm", None)
        invalidate_handle = None

        # in case the association handle does not exist in the association
        # handle openid server map
        if not association_handle in self.association_handle_openid_server_map:
            # invalidates the association handle, the communication is converted
            # into stateless mode
            invalidate_handle = association_handle
            association_handle = None

        # in case the association handle is defined
        if association_handle:
            # retrieves the openid server for the association handle
            openid_server = self.association_handle_openid_server_map[association_handle]
        # otherwise a new openid server should be created
        # for the stateless mode
        else:
            # retrieves the api openid plugin
            api_openid_plugin = self.plugin.api_openid_plugin

            # creates the openid server
            openid_server = api_openid_plugin.create_server({})

            # retrieves the provider url
            provider_url = self._get_provider_url(rest_request)

            # generates the openid structure
            openid_server.generate_openid_structure(provider_url)

            # associates the server and the provider, retrieving the
            # openid structure
            openid_structure = openid_server.openid_associate()

            # retrieves the openid association handle
            openid_association_handle = openid_structure.get_association_handle()

            # sets the openid server in the association handle
            # openid server map for later retrieval
            self.association_handle_openid_server_map[openid_association_handle] = openid_server

        # retrieves the openid structure
        openid_structure = openid_server.get_openid_structure()

        # sets the structure attributes
        openid_structure.set_claimed_id(claimed_id)
        openid_structure.set_identity(identity)
        openid_structure.set_return_to(return_to)
        openid_structure.set_realm(realm)
        openid_structure.set_invalidate_handle(invalidate_handle)

        # sets the openid structure in the session
        self.set_session_attribute(rest_request, "openid_server", openid_server, NAMESPACE_NAME)

        # retrieves the username from the
        username = openid_structure.get_username_claimed_id()

        # in case the user is already signed in
        # and the username is valid
        if login and username == user_information_username:
            # processes the request in the server
            openid_server.openid_request()

            # redirects to the redirect page
            self.redirect_base_path(rest_request, "redirect")

            # returns true
            return True
        else:
            # redirects to the signin page
            self.redirect_base_path(rest_request, "signin")

            # returns true
            return True

        # returns true
        return True

    def process_check_authentication(self, rest_request, openid_data):
        # retrieves the association handle
        association_handle = openid_data["assoc_handle"]

        # retrieves the other openid attributes
        ns = openid_data.get("ns", OPENID_NAMESPACE_VALUE)
        provider_url = openid_data["op_endpoint"]
        claimed_id = openid_data["claimed_id"]
        identity = openid_data["identity"]
        return_to = openid_data["return_to"]
        response_nonce = openid_data["response_nonce"]
        signed = openid_data["signed"]
        signature = openid_data["sig"]

        # retrieves the openid server for the association handle
        openid_server = self.association_handle_openid_server_map[association_handle]

        # retrieves the openid structure
        openid_structure = openid_server.get_openid_structure()

        # retrieves the openid attributes
        association_type = openid_structure.get_association_type()
        session_type = openid_structure.get_session_type()

        # creates the openid return structure
        return_openid_structure = openid_server.generate_openid_structure(provider_url, association_type, session_type, set_structure = False)

        # sets some of the items of the openid structure
        return_openid_structure.set_ns(ns)
        return_openid_structure.set_claimed_id(claimed_id)
        return_openid_structure.set_identity(identity)
        return_openid_structure.set_return_to(return_to)
        return_openid_structure.set_response_nonce(response_nonce)
        return_openid_structure.set_signed(signed)
        return_openid_structure.set_signature(signature)

        # checks the openid authentication
        openid_server.openid_check_authentication(return_openid_structure)

        # retrieves the encoded check authentication parameters
        encoded_check_authentication_parameters = openid_server.get_encoded_check_authentication_parameters()

        # sets the request contents
        self.set_contents(rest_request, encoded_check_authentication_parameters, "text/plain")

        # returns true
        return True

    def _assign_base(self, rest_request, template_file):
        # retrieves the host path for the server path as the openid server address
        openid_server = self._get_host_path(rest_request, "/server")

        # assigns the template variables
        template_file.assign("title", "Hive Solutions OpenID")
        template_file.assign(OPENID_SERVER_VALUE, openid_server)

    def _get_provider_url(self, rest_request):
        # retrieves the host path for the server path as the provider url
        provider_url = self._get_host_path(rest_request, "/server")

        # returns the provider url
        return provider_url
