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
LOG = logging.getLogger(__name__)


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

    def _generate_names(self, name_list=None):
        if not name_list:
            name_list = ['default-domain', 'admin']
        name_list.append(data_utils.rand_name('test'))
        return name_list

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_routing_instances")
    def test_list_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            LOG.debug("\n\nStarting the test\n\n")
            self.client.list_routing_instances()
            LOG.debug("\n\nOkay that's it\n\n")
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_routing_instances")
    def test_create_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=False)
        new_vn =\
            self.vn_client.create_virtual_networks(
                parent_type='project',
                fq_name=self._generate_names())['virtual-network']
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            LOG.debug("\n\nStarting the test\n\n")
            self.client.create_routing_instances(
                parent_type='virtual-network',
                fq_name=self._generate_names(new_vn['fq_name']))
            LOG.debug("\n\nOkay that's it\n\n")
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            self.vn_client.delete_virtual_networks(new_vn['uuid'])

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_routing_instances")
    def test_show_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=False)
        new_vn =\
            self.vn_client.create_virtual_networks(
                parent_type='project',
                fq_name=self._generate_names())['virtual-network']
        new_names = self._generate_names(new_vn['fq_name'])
        new_instance =\
            self.client.create_routing_instances(
                parent_type='virtual-network',
                fq_name=new_names)['routing-instance']
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            LOG.debug("\n\nStarting the test\n\n")
            self.client.show_routing_instances(new_instance['uuid'])
            LOG.debug("\n\nOkay that's it\n\n")
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            self.vn_client.delete_virtual_networks(new_vn['uuid'])

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_routing_instances")
    def test_delete_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=False)
        new_vn =\
            self.vn_client.create_virtual_networks(
                parent_type='project',
                fq_name=self._generate_names())['virtual-network']
        new_instance =\
            self.client.create_routing_instances(
                parent_type='virtual-network',
                fq_name=self._generate_names(new_vn['fq_name']))['routing-'
                                                                 'instance']
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            LOG.debug("\n\nStarting the test\n\n")
            self.client.delete_routing_instances(new_instance['uuid'])
            LOG.debug("\n\nOkay that's it\n\n")
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            self.vn_client.delete_virtual_networks(new_vn['uuid'])

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_routing_instances")
    def test_update_routing_instances(self):
        rbac_utils.switch_role(self, switchToRbacRole=False)
        new_vn =\
            self.vn_client.create_virtual_networks(
                parent_type='project',
                fq_name=self._generate_names())['virtual-network']
        new_instance =\
            self.client.create_routing_instances(
                parent_type='virtual-network',
                fq_name=self._generate_names(new_vn['fq_name']))['routing-'
                                                                 'instance']
        update_names = self._generate_names(new_vn['fq_name'])
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            LOG.debug("\n\nStarting the test\n\n")
            self.client.update_routing_instances(
                new_instance['uuid'],
                fq_name=new_vn['fq_name'],
                routing_instance_is_default=True)
            LOG.debug("\n\nOkay that's it\n\n")
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            self.vn_client.delete_virtual_networks(new_vn['uuid'])
