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
from contrail_tempest_plugin.services.contrail.json import routing_client
from contrail_tempest_plugin.services.contrail.json import \
    virtual_network_client
from contrail_tempest_plugin.tests.api.contrail import base

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils
from tempest.common.utils import data_utils

from tempest import config
from tempest import test

CONF = config.CONF


class RoutingClientTest(base.BaseContrailTest):
    @classmethod
    def setup_clients(cls):
        super(RoutingClientTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider
        cls.client = routing_client.RoutingClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)
        cls.vn_client = virtual_network_client.VirtualNetworkClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)
        cls.admin_client = cls.os_adm.network_client

    @classmethod
    def resource_setup(cls):
        super(RoutingClientTest, cls).resource_setup()

        net_name = data_utils.rand_name('test-net')
        net_fq_name = ['default-domain', 'admin', net_name]

        cls.network = cls.vn_client.create_virtual_networks(
                parent_type='project',
                fq_name=net_fq_name)['virtual-network']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_networks,
                                 cls.network['uuid'])
        super(RoutingClientTest, cls).resource_cleanup()

    def _create_routing_instances(self):
        instance_name = data_utils.rand_name('test-instance')
        instance_fq_name = ['default-domain', 'admin',
                            self.network['name'], instance_name]

        new_instance = self.client.create_routing_instances(
                parent_type='virtual-network',
                fq_name=instance_fq_name)['routing-instance']

        self.addCleanup(self._try_delete_resource,
                        self.client.delete_routing_instances,
                        new_instance['uuid'])
        return new_instance

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_routing_instances")
    @test.idempotent_id('054c56ba-76b2-4161-a702-40301d8de085')
    def test_list_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_routing_instances()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_routing_instances")
    @test.idempotent_id('3d44a46b-5436-43a8-b2f7-8581f0f04dbc')
    def test_create_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self._create_routing_instances()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_routing_instances")
    @test.idempotent_id('161abb37-6037-422b-b453-108a5d10caca')
    def test_show_routing_instances(self):
        new_instance = self._create_routing_instances()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_routing_instances(new_instance['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_routing_instances")
    @test.idempotent_id('1d3af01e-01bf-4347-a9bc-633732339e0e')
    def test_delete_routing_instances(self):
        new_instance = self._create_routing_instances()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_routing_instances(new_instance['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_routing_instances")
    @test.idempotent_id('ebcfd442-2a26-4954-968b-e17e414ed0d1')
    def test_update_routing_instances(self):
        new_instance = self._create_routing_instances()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_routing_instances(
                new_instance['uuid'],
                display_name=data_utils.rand_name('test-instance'))
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
