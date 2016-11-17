# Copyright 2016 AT&T Corp
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from oslo_log import log as logging
from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class BaseContrailTest(test.BaseTestCase):
    """Base class for Contrail tests."""
    credentials = ['primary', 'admin']

    '''
    @classmethod
    def skip_checks(cls):
        super(BaseContrailTest, cls).skip_checks()
        if not CONF.service_available.contrail:
            raise cls.skipException("Contrail support is required")
    '''

    @classmethod
    def setup_credentials(cls):
        super(BaseContrailTest, cls).setup_credentials()

    @classmethod
    def setup_clients(cls):
        super(BaseContrailTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider
        cls.admin_client = cls.os_adm.network_client
