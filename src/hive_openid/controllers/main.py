#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Solutions Openid
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony

import hive_openid

import base

OPENID_NAMESPACE_VALUE = "http://specs.openid.net/auth/2.0"
""" The openid namespace value """

mvc_utils = colony.__import__("mvc_utils")

class MainController(base.BaseController):

    handles_map = {}
    """ The map associating the association handle
    with the openid server, this is used at runtime
    to retrieve server instances for handles in auth """

    def __init__(self, plugin, system):
        base.BaseController.__init__(self, plugin, system)
        self.handles_map = {}

    @mvc_utils.serialize
    def index(self, request):
        self._template(
            request = request,
            partial_page = "index_contents.html.tpl"
        )

    @mvc_utils.serialize
    def user(self, request, username):
        # retrieves the info user plugin that is going to be used to retrieve
        # the information on the request user (through username matching)
        info_user_plugin = self.plugin.info_user_plugin

        # retrieves the host path for the xrds path as the openid xrds address
        # note that the address is "customized" using parameters
        openid_xrds = self._get_host_path(request, "/xrds?openid_user=" + username)

        # retrieves the user information from the info user plugin
        # using the openid user and in case no valid value is found
        # an exception is raised indicating the problem with the information
        openid_user_information = info_user_plugin.get_user_info(username)
        if not openid_user_information:
            raise hive_openid.UserInformationError("user information not found")

        # sets the xrds header value with the location of the information on
        # the requested used, this may be used by the client to request yadis
        request.set_header("X-XRDS-Location", openid_xrds)

        # runs the processing of the user information template, presenting
        # some visual information to the user agent
        self._template(
            request = request,
            partial_page = "user_contents.html.tpl",
            openid_user = username,
            openid_user_information = openid_user_information
        )

    @mvc_utils.serialize
    def user_vcard(self, request, username):
        info_user_plugin = self.plugin.info_user_plugin
        openid_user_information = info_user_plugin.get_user_info(username)
        self._template(
            request = request,
            template = "vcard.vcf.tpl",
            content_type = "text/x-vcard",
            openid_user = username,
            openid_user_information = openid_user_information
        )

    @mvc_utils.serialize
    def signin(self, request):
        self._template(
            request = request,
            partial_page = "signin_contents.html.tpl"
        )

    @mvc_utils.serialize
    def allow(self, request):
        self._template(
            request = request,
            partial_page = "allow_contents.html.tpl"
        )

    @mvc_utils.serialize
    def approve(self, request):
        self._template(
            request = request,
            partial_page = "approve_contents.html.tpl"
        )

    @mvc_utils.serialize
    def server(self, request):
        # processes the form data of the request in flat mode and uses
        # the resulting values to retrieve the openid information
        form_data_map = self.process_form_data_flat(request, "utf-8")
        openid_data = form_data_map.get("openid", {})
        openid_mode = openid_data.get("mode", "invalid")

        # prints a debug message mentioning the mode that is going
        # to be used in the interaction with the server
        self.plugin.debug("Receiving request '%s' from client" % openid_mode)

        # verifies the target execution mode of the openid request
        # and runs the "associated" processing for each mode, in
        # case an invalid type is defined an exception is raised
        if openid_mode == "associate":
            return self.process_associate(request, openid_data)
        elif openid_mode == "checkid_setup":
            return self.process_check_id_setup(request, openid_data)
        elif openid_mode == "check_authentication":
            return self.process_check_authentication(request, openid_data)
        else: raise hive_openid.InvalidMode(openid_mode)

    @mvc_utils.serialize
    def xrds(self, request):
        openid_user = request.field("openid_user", "invalid")
        openid_user_base = self._get_host_path(request, "/" + openid_user)
        self._template(
            request = request,
            template = "xrds.xml.tpl",
            content_type = "application/xrds+xml",
            openid_user_base = openid_user_base
        )

    @mvc_utils.serialize
    def login(self, request):
        # retrieves the reference to the openid plugin that is going
        # to be used for the re-creation of the openid server
        api_openid_plugin = self.plugin.api_openid_plugin

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data_flat(request, "utf-8")

        # processes the login, retrieving the authentication user information
        # this operation may raise exception in case authentication fails
        user_information = self.process_login(request, form_data_map)

        # in case the authentication was successful, the user must be
        # logged in the current account for the current session
        if user_information:
            # sets both the login flag attribute and the user information
            # (dictionary value) in the current session to be used for latter
            # configuration and model control (required for authentication)
            request.set_s("login", True)
            request.set_s("user_information", user_information)

        # otherwise the user must be removed from the current session in
        # other to avoid any possible side problem
        else:
            # unsets the login attribute the complete set of attributes
            # currently associated with the user (to avoid problems)
            request.set_s("login", False)

        # retrieves the openid structure from the session attribute, and verifies
        # that the value is currently set and valid creating the proper server
        # instance in case it's (server re-creation)
        openid_structure = request.get_s("openid_structure")
        if not openid_structure: return self.redirect_base_path(request, "redirect")
        openid_server = api_openid_plugin.create_server(
            dict(openid_structure = openid_structure)
        )

        # retrieves the openid structure and uses it to retrieve the claimed id
        # as the username that is going to be used for validation
        openid_structure = openid_server.get_openid_structure()
        username = openid_structure.get_username_claimed_id()

        # retrieves the user information username this is the value that is going
        # to be used for the matching and runs the matching raising an exception
        # in case the matching operation fails (username values are different)
        _username = user_information.get("username", None)
        if not username == _username:
            raise hive_openid.UserInformationError("invalid username for openid claimed id")

        # processes the request in the server and then runs the redirection to the
        # target redirect operator page (will use value from session)
        openid_server.openid_request()
        self.redirect_base_path(request, "redirect")

    @mvc_utils.serialize
    def logout(self, request):
        # unsets the login attribute in the session and then
        # redirects to the user page as requested
        request.set_s("login", False)
        self.redirect_base_path(request, "index")

    @mvc_utils.serialize
    def redirect_do(self, request):
        # retrieves the reference to the openid plugin that is going
        # to be used for the re-creation of the openid server
        api_openid_plugin = self.plugin.api_openid_plugin

        # retrieves the login session attribute and verifies if
        # the user is logged in (or in the middle of auth) and
        # in case it's not redirects the user agent to the signin
        # page (as expected) that's the typical strategy
        login = request.get_s("login")
        if not login: self.redirect_base_path(request, "signin")

        # retrieves the openid structure from the session attribute
        # an in case it's defined runs the redirection to the
        # the defined return url (external url), note that the open
        # id server instance must be re-created for such usage
        openid_structure = request.get_s("openid_structure")
        if openid_structure:
            openid_server = api_openid_plugin.create_server(
                dict(openid_structure = openid_structure)
            )
            return_url = openid_server.get_return_url()
            self.redirect_base_path(request, return_url, quote = False)

        # otherwise this is a fallback situation and the user agent
        # is redirected to the default index page, this should be
        # a normal "in-site" login operation (typical situation)
        else: self.redirect_base_path(request, "index")

        # unsets the openid structure as session attribute as it may
        # be defined and should be removed from session (touch operation)
        request.unset_s("openid_structure")

    def process_login(self, request, user_data):
        # retrieves the various plugins that are going to be used
        # in the processing of the login attempt
        authentication_plugin = self.plugin.authentication_plugin
        info_user_plugin = self.plugin.info_user_plugin

        # retrieves the authentication properties map, that is going
        # to be used in the authentication process
        authentication_properties_map = self.system.authentication_properties_map

        # in case the authentication handler property is not defined, raises
        # the missing property exception indicating the problem
        if not "authentication_handler" in authentication_properties_map:
            raise hive_openid.MissingProperty("authentication_handler")

        # in case the arguments property is not defined, raises the missing
        # property exception indicating the problem
        if not "arguments" in authentication_properties_map:
            raise hive_openid.MissingProperty("arguments")

        # unpacks the provider user data into the username and the password
        # so that they may be used by the authentication handler
        username = user_data.get("username", None)
        password = user_data.get("password", None)

        # retrieves the complete information for the authentication process
        # (both the handler and the arguments) and runs the process validating
        # the result of the authentication at the end of the call
        authentication_handler = authentication_properties_map["authentication_handler"]
        arguments = authentication_properties_map["arguments"]
        authentication_result = authentication_plugin.authenticate_user(
            username, password, authentication_handler, arguments
        )
        authentication_result_valid = authentication_result.get("valid", False)

        # in case the authentication fails, unpacks the exception contents/message
        # and raises an exception about the authentication failed process
        if not authentication_result_valid:
            exception = authentication_result.get("exception", {})
            exception_message = exception.get("message", "undefined error")
            raise hive_openid.AuthenticationFailed(exception_message)

        # retrieves the authentication username and uses it as the base for the
        # gathering od the information about the user
        authentication_username = authentication_result.get("username", None)
        user_information = info_user_plugin.get_user_info(authentication_username)

        # in case there is no authentication user information, must raise an
        # exception indicating the need for more user information
        if not user_information:
            raise hive_openid.UserInformationError("missing user information")

        # returns the authentication user information to the caller method as
        # this is considered the result from the login operation
        return user_information

    def process_associate(self, request, openid_data):
        # retrieves the api openid plugin using it in the generation
        # of the service instance for the current auth workflow
        api_openid_plugin = self.plugin.api_openid_plugin
        openid_server = api_openid_plugin.create_server({})

        # retrieves the provider url associated with the current
        # request (to be used in the structure creation)
        provider_url = self._get_provider_url(request)

        # retrieves the openid attributes
        association_type = openid_data["assoc_type"]
        session_type = openid_data["session_type"]

        # retrieves the diffie hellman attributes, and uses them to
        # generate the proper structure information to be used latter
        prime_value = openid_data.get("dh_modulus", None)
        base_value = openid_data.get("dh_gen", None)
        consumer_public = openid_data.get("dh_consumer_public", None)
        openid_server.generate_openid_structure(
            provider_url,
            association_type,
            session_type,
            prime_value,
            base_value,
            consumer_public
        )

        # associates the server and the provider, retrieving the
        # openid structure and uses it to retrieve the handle
        openid_structure = openid_server.openid_associate()
        openid_association_handle = openid_structure.get_association_handle()

        # retrieves the encoded response parameters as a plain text
        # data structure and serializes it into the current response
        data = openid_server.get_encoded_response_parameters()
        self.set_contents(request, data, "text/plain")

        # sets the openid server in the association handle
        # openid server map for later retrieval, this is going to
        # be used latter in the check id part of the process
        self.handles_map[openid_association_handle] = openid_server

    def process_check_id_setup(self, request, openid_data):
        # retrieves the login session attribute
        login = request.get_s("login")

        # retrieves the user information attribute and tries to retrieve
        # the username attribute from that same information package
        user_information = request.get_s("user_information", {})
        user_information_username = user_information.get("username", None)

        # retrieves the openid attributes from the provided openid data
        # these are going to be used in the openid structure
        identity = openid_data["identity"]
        claimed_id = openid_data.get("claimed_id", identity)
        association_handle = openid_data.get("assoc_handle", None)
        return_to = openid_data["return_to"]
        realm = openid_data.get("realm", None)
        invalidate_handle = None

        # in case the association handle does not exist in the association
        # handle openid server map
        if not association_handle in self.handles_map:
            # invalidates the association handle, the communication is converted
            # into stateless mode
            invalidate_handle = association_handle
            association_handle = None

        # in case the association handle is defined
        if association_handle:
            openid_server = self.handles_map[association_handle]

        # otherwise a new openid server should be created
        # for the stateless mode
        else:
            # retrieves the api openid plugin and creates a new
            # server instance using this same plugin
            api_openid_plugin = self.plugin.api_openid_plugin
            openid_server = api_openid_plugin.create_server({})

            # retrieves the provider url and
            provider_url = self._get_provider_url(request)
            openid_server.generate_openid_structure(provider_url)

            # associates the server and the provider, retrieving the
            # openid structure
            openid_structure = openid_server.openid_associate()

            # retrieves the openid association handle and sets the
            # openid server in the association handle openid server
            # map for later retrieval
            openid_association_handle = openid_structure.get_association_handle()
            self.handles_map[openid_association_handle] = openid_server

        # retrieves the openid structure for the current loaded
        # server and set the complete set of attributes from data
        openid_structure = openid_server.get_openid_structure()
        openid_structure.set_claimed_id(claimed_id)
        openid_structure.set_identity(identity)
        openid_structure.set_return_to(return_to)
        openid_structure.set_realm(realm)
        openid_structure.set_invalidate_handle(invalidate_handle)

        # sets the openid structure in the current session, so that
        # it may be used latter for the login process
        request.set_s("openid_structure", openid_structure)

        # retrieves the username from the the structure
        # and verifies if the current situation is a login one
        # and if the claimed and verified username are the same
        username = openid_structure.get_username_claimed_id()
        if login and username == user_information_username:
            openid_server.openid_request()
            self.redirect_base_path(request, "redirect")
        else:
            self.redirect_base_path(request, "signin")

    def process_check_authentication(self, request, openid_data):
        # retrieves the association handle
        association_handle = openid_data["assoc_handle"]

        # retrieves the other openid attributes, most of these
        # values are going to be used as part of the return
        # openid structure creation/population
        ns = openid_data.get("ns", OPENID_NAMESPACE_VALUE)
        provider_url = openid_data["op_endpoint"]
        claimed_id = openid_data["claimed_id"]
        identity = openid_data["identity"]
        return_to = openid_data["return_to"]
        response_nonce = openid_data["response_nonce"]
        signed = openid_data["signed"]
        signature = openid_data["sig"]

        # retrieves the openid server for the association handle
        # and uses it to retrieve the underlying openid structure
        # gathering then some of its attributes
        openid_server = self.handles_map[association_handle]
        openid_structure = openid_server.get_openid_structure()
        association_type = openid_structure.get_association_type()
        session_type = openid_structure.get_session_type()

        # creates the openid return structure populating many of it's
        # fields from the received openid data and then uses it to run
        # the check authentication part of the process
        return_openid_structure = openid_server.generate_openid_structure(
            provider_url,
            association_type,
            session_type,
            set_structure = False
        )
        return_openid_structure.set_ns(ns)
        return_openid_structure.set_claimed_id(claimed_id)
        return_openid_structure.set_identity(identity)
        return_openid_structure.set_return_to(return_to)
        return_openid_structure.set_response_nonce(response_nonce)
        return_openid_structure.set_signed(signed)
        return_openid_structure.set_signature(signature)
        openid_server.openid_check_authentication(return_openid_structure)

        # retrieves the encoded check authentication parameters and
        # sets it as plain text encoded for the current response
        data = openid_server.get_encoded_check_authentication_parameters()
        self.set_contents(request, data, "text/plain")

    def _get_provider_url(self, request):
        # retrieves the host path for the server path as the provider url
        # and returns it to the caller method to be used
        provider_url = self._get_host_path(request, "/server")
        return provider_url
