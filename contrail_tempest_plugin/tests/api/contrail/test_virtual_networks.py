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

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class NetworksTest(base.BaseContrailTest):

    @classmethod
    def setup_clients(cls):
        super(NetworksTest, cls).setup_clients()
        cls.client = cls.vn_client

    @classmethod
    def skip_checks(cls):
        super(NetworksTest, cls).skip_checks()
        if not CONF.identity.rbac_flag:
            raise cls.skipException(
                "%s skipped as RBAC Flag not enabled" % cls.__name__)
        if CONF.auth.tempest_roles != ['admin']:
            raise cls.skipException(
                "%s skipped because tempest roles is not admin" % cls.__name__)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="get_virtual_networks")
    @test.idempotent_id('375ebc8d-dc52-4d9c-877b-85aba35b1539')
    def test_get_virtual_networks(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            body = self.client.get_virtual_networks()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
