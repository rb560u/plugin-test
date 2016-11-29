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
    service_appliances_client
from contrail_tempest_plugin.tests.api.contrail import base

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils
from tempest.common.utils import data_utils

from tempest import config
from tempest import test

CONF = config.CONF


class ServiceAppliancesClientTest(base.BaseContrailTest):
    @classmethod
    def setup_clients(cls):
        super(ServiceAppliancesClientTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider
        cls.client = service_appliances_client.ServiceAppliancesClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)
        cls.admin_client = cls.os_adm.network_client

    def _create_service_appliance_sets(self):
        set_name = data_utils.rand_name('test-set')
        set_fq_name = ['default-global-system-config', set_name]

        new_set = self.client.create_service_appliance_sets(
                parent_type='global-system-config',
                fq_name=set_fq_name)['service-appliance-set']

        self.addCleanup(self._try_delete_resource,
                        self.client.delete_service_appliance_sets,
                        new_set['uuid'])
        return new_set

    def _create_service_appliances(self, app_set):
        appliance_name = data_utils.rand_name('test-appliance')
        appliance_fq_name = app_set['fq_name']
        appliance_fq_name.append(appliance_name)

        new_appliance = self.client.create_service_appliances(
                parent_type='service-appliance-set',
                fq_name=appliance_fq_name)['service-appliance']

        self.addCleanup(self._try_delete_resource,
                        self.client.delete_service_appliances,
                        new_appliance['uuid'])
        return new_appliance

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_service_appliances")
    @test.idempotent_id('6b5fc17c-34e6-4d21-a53e-a0dfe69afd31')
    def test_list_service_appliances(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_service_appliances()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_service_appliances")
    @test.idempotent_id('0563c0c8-b986-466e-8540-aa8ad7a10367')
    def test_create_service_appliances(self):
        new_set = self._create_service_appliance_sets()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            new_appliance = self._create_service_appliances(new_set)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_service_appliances")
    @test.idempotent_id('ea30dcfe-8657-4a7d-9cf1-3176d334bf27')
    def test_show_service_appliances(self):
        new_set = self._create_service_appliance_sets()
        new_appliance = self._create_service_appliances(new_set)
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_service_appliances(new_appliance['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_service_appliances")
    @test.idempotent_id('a54ca33a-8590-4844-96d7-b96882b59e86')
    def test_update_service_appliances(self):
        new_set = self._create_service_appliance_sets()
        new_appliance = self._create_service_appliances(new_set)
        update_name = data_utils.rand_name('test')
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_service_appliances(new_appliance['uuid'],
                                                  display_name=update_name)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_service_appliances")
    @test.idempotent_id('362deff5-7b72-4929-ba81-972cfcfa1309')
    def test_delete_service_appliances(self):
        new_set = self._create_service_appliance_sets()
        new_appliance = self._create_service_appliances(new_set)
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_service_appliances(new_appliance['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_service_appliance_sets")
    @test.idempotent_id('c1e74da9-00b6-4c88-adda-2ce49094e570')
    def test_list_service_appliance_sets(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_service_appliance_sets()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_service_appliance_sets")
    @test.idempotent_id('eb00d6cf-590f-41bf-8ee4-5be625d9cb93')
    def test_create_service_appliance_sets(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            new_set = self._create_service_appliance_sets()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_service_appliance_sets")
    @test.idempotent_id('dd35dd04-e7d9-46bb-8f36-26835f122572')
    def test_show_service_appliance_sets(self):
        new_set = self._create_service_appliance_sets()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_service_appliance_sets(new_set['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_service_appliance_sets")
    @test.idempotent_id('952f063b-bc71-4f62-83b1-719bce5ad4ed')
    def test_update_service_appliance_sets(self):
        new_set = self._create_service_appliance_sets()
        update_name = data_utils.rand_name('test')
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_service_appliance_sets(new_set['uuid'],
                                                      display_name=update_name)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_service_appliance_sets")
    @test.idempotent_id('7b56ce24-da1d-4565-bd22-c58dc57d7045')
    def test_delete_service_appliance_sets(self):
        new_set = self._create_service_appliance_sets()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_service_appliance_sets(new_set['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
