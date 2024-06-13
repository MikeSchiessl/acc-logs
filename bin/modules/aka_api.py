#!/usr/bin/env python3

# Copyright 2022 Akamai Technologies, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import os
import logging

from urllib.parse import parse_qs
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import modules.aka_log as aka_log
import acc_config.default_config as default_cfg
import acc_config.version as acc_version


class AkaApi:
    """
    AKAMAI API CLASS for ACC EventViewer
    """
    def __init__(self, edgerc_section="default",
                        edgerc="~/.edgerc",
                         accountswitchkey=None ):
        # Instanciate logging
        aka_log.log.debug("Request logging enabled")

        edgerc = EdgeRc(os.path.expanduser(edgerc))
        section = edgerc_section
        self.baseurl = f"https://{edgerc.get(section, 'host')}"

        self.session = requests.Session()
        self.session.auth = EdgeGridAuth(
            client_token=edgerc.get(section, 'client_token'),
            client_secret=edgerc.get(section, 'client_secret'),
            access_token=edgerc.get(section, 'access_token'))
 
        # The NEW account_key way of doing account switching
        account_key = None
        self.account_key = None
        if accountswitchkey:
            account_key = accountswitchkey
            aka_log.log.debug(f"Found an accountSwitchKey as parameter: {account_key}")
            self.account_key = {'accountSwitchKey': account_key}
        else:       
            account_key = edgerc.get(section, 'account_key', fallback=None)
            if account_key:
                aka_log.log.debug(f"Found an accountSwitchKey (account_key) in the .edgerc file: {account_key}")
                self.account_key = {'accountSwitchKey': account_key}


    def _api_request(self, method="GET", path=None, params={}, headers={}, user_agent=None, expected_status_list=[200]):
        try:
            my_url = self.baseurl + path
            headers["Accept"]  = "application/json"
            headers['User-Agent'] = user_agent
            if self.account_key:
                params.update(self.account_key)
            aka_log.log.debug(f"Sending Request - Method: {method}, Path: {path}, Headers: {headers}")
            my_request = self.session.request(method=method.upper(), url=my_url, params=params, headers=headers)
            aka_log.log.debug(f"Sent Request URI: {my_request.url}")
            aka_log.log.debug(f"Received Status: {my_request.status_code}, Text: {my_request.text}")
            if my_request.status_code in expected_status_list and my_request.text:
                aka_log.log.debug(f"REQ finsihed, returning JSON")
                return my_request.json()
            elif my_request.status_code in expected_status_list:
                aka_log.log.debug(f"REQ finsihed, returning True")
                return True
            else:
                self.akalog.warn(f"Request returned wrong status: Status: {my_request.status_code}, Text: {my_request.text}")
                return False
        except Exception as error:
            self.akalog.warn(f"Request error: {error}")
            return False

    def get_events(self, method="GET", path='/', user_agent=None, params={}):
        """
        Get Event Viewer events
        :return: True on success
        """
        #aka_log.log.debug(f"Starting events collection")
        return self._api_request(method=method, path=path, params=params, user_agent=user_agent)

        