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
from tempest.common.utils import data_utils

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class NetworksTest(base.BaseContrailTest):

    @classmethod
    def skip_checks(cls):
        super(NetworksTest, cls).skip_checks()
        if not CONF.identity.rbac_flag:
            raise cls.skipException(
                "%s skipped as RBAC Flag not enabled" % cls.__name__)
        if CONF.auth.tempest_roles != ['admin']:
            raise cls.skipException(
                "%s skipped because tempest roles is not admin" % cls.__name__)

    @classmethod
    def setup_clients(cls):
        super(NetworksTest, cls).setup_clients()
        cls.client = cls.vn_client

    @classmethod
    def resource_setup(cls):
        super(NetworksTest, cls).resource_setup()

        # Create virtual network for tests
        net_name = data_utils.rand_name('rbac-virtual-network')
        fq_name = ['default-domain', 'admin', net_name]

        post_body = {'parent_type': 'project'}
        post_body['router_external'] = True
        post_body['fq_name'] = fq_name

        resp, body = cls.vn_client.create_virtual_network(**post_body)
        cls.network = body['virtual-network']

    @classmethod
    def resource_cleanup(cls):

        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        super(NetworksTest, cls).resource_cleanup()

    def _create_virtual_network(self):
        net_name = data_utils.rand_name('rbac-virtual-network')
        fq_name = ['default-domain', 'admin', net_name]
        post_body = {'parent_type': 'project'}
        post_body['router_external'] = True
        post_body['fq_name'] = fq_name
        resp, body = self.client.create_virtual_network(**post_body)
        network = body['virtual-network']
        self.addCleanup(self._try_delete_resource,
                        self.vn_client.delete_virtual_network,
                        network['uuid'])
        return network

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

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_virtual_networks")
    @test.idempotent_id('375ebc8d-dc52-4d9c-877b-96aba35b2530')
    def test_create_virtual_networks(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self._create_virtual_network()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_virtual_network")
    @test.idempotent_id('375ebc8d-dc52-4d9c-566b-150a025c1237')
    def test_update_virtual_networks(self):
        # Create virtual network
        uuid = self._create_virtual_network()['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_virtual_network(uuid, router_external='False')
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_virtual_networks")
    @test.idempotent_id('375ebc8d-dc52-4d9c-877b-17bcb53c3641')
    def test_delete_virtual_networks(self):
        uuid = self._create_virtual_network()['uuid']
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_virtual_network(uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_virtual_network")
    @test.idempotent_id('375ebc8d-dc52-4d9c-877b-27c1a1242a81')
    def test_show_virtual_networks(self):
        uuid = self._create_virtual_network()['uuid']
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_virtual_network(uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
