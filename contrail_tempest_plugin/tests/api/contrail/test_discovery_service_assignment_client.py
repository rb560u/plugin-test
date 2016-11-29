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
from contrail_tempest_plugin.services.contrail.json import \
    discovery_service_assignment_client as dsa_client
from contrail_tempest_plugin.tests.api.contrail import base

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils
from tempest.common.utils import data_utils

from tempest import config
from tempest import test

CONF = config.CONF


class DiscoveryServiceAssignmentClientTest(base.BaseContrailTest):
    @classmethod
    def setup_clients(cls):
        super(DiscoveryServiceAssignmentClientTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider
        cls.client = dsa_client.DiscoveryServiceAssignmentClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)
        cls.admin_client = cls.os_adm.network_client

    def _create_discovery_service_assignments(self):
        dsa_name = [data_utils.rand_name('test-dsa')]

        new_dsa = self.client.create_discovery_service_assignments(
                fq_name=dsa_name)['discovery-service-assignment']

        self.addCleanup(self._try_delete_resource,
                        self.client.delete_discovery_service_assignments,
                        new_dsa['uuid'])
        return new_dsa

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_discovery_service_assignments")
    @test.idempotent_id('9ac1e4ca-8983-403f-b644-7758935f2f36')
    def test_list_discovery_service_assignments(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_discovery_service_assignments()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_discovery_service_assignments")
    @test.idempotent_id('40ad1208-a039-4809-8516-41b4dfcbd00c')
    def test_create_discovery_service_assignments(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            new_dsa = self._create_discovery_service_assignments()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_discovery_service_assignments")
    @test.idempotent_id('63660fe9-22b8-456c-a757-a7da1abfbce8')
    def test_show_discovery_service_assignments(self):
        new_dsa = self._create_discovery_service_assignments()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_discovery_service_assignments(new_dsa['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_discovery_service_assignments")
    @test.idempotent_id('71ce1404-965b-4670-abb7-5b6fea3b24b7')
    def test_update_discovery_service_assignments(self):
        new_dsa = self._create_discovery_service_assignments()
        update_name = data_utils.rand_name('test')
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            (self.client.
                update_discovery_service_assignments(new_dsa['uuid'],
                                                     fq_name=new_dsa['fq_'
                                                                     'name'],
                                                     display_name=update_name))
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_discovery_service_assignments")
    @test.idempotent_id('e7ff845d-2140-4eb0-9720-26370459723b')
    def test_delete_discovery_service_assignments(self):
        new_dsa = self._create_discovery_service_assignments()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_discovery_service_assignments(new_dsa['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
