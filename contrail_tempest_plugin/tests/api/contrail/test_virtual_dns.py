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

from contrail_tempest_plugin.tests.api.contrail import base

from contrail_tempest_plugin.services.contrail.json.virtual_dns_client import \
    VirtualDNSClient

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class VirtualDNSTest(base.BaseContrailTest):

    @classmethod
    def setup_clients(cls):
        super(VirtualDNSTest, cls).setup_clients()
        cls.client = VirtualDNSClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_virtual_DNSs")
    def test_list_virtual_DNSs(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            body = self.client.list_virtual_DNSs()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
