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

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils

from tempest import test

LOG = logging.getLogger(__name__)

class ContrailTest(base.BaseContrailTest):


    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_bgp_services")
    @test.idempotent_id('375ebc8d-dc52-4d9c-877b-84aaa34b1539')
    def test_bgp_services(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            body = self.client.list_bgp_services()
            LOG.debug("\n\n\n\n\nab2434\n\n")
            LOG.debug(body)
            LOG.debug("\n\n\n------------") 
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    '''
    def test_list_virtual_routers(self):
        body = self.client.list_virtual_routers()
        self.assertEqual('1', '2')
        print body
    '''
