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
    access_control_client
from contrail_tempest_plugin.tests.api.contrail import base

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils
from tempest.common.utils import data_utils

from tempest import config
from tempest import test

CONF = config.CONF


class AccessControlClientTest(base.BaseContrailTest):
    @classmethod
    def setup_clients(cls):
        super(AccessControlClientTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider
        cls.client = access_control_client.AccessControlClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)
        cls.admin_client = cls.os_adm.network_client

    def _create_api_access_lists(self):
        api_list_name = data_utils.rand_name('test-api-list')
        api_list_fq_name = ['default-domain', 'admin', api_list_name]

        new_api_list = self.client.create_api_access_lists(
                    fq_name=api_list_fq_name,
                    parent_type="project")['api-access-list']

        self.addCleanup(self._try_delete_resource,
                        self.client.delete_api_access_lists,
                        new_api_list['uuid'])
        return new_api_list

    def _create_access_control_lists(self):
        ctrl_list_name = data_utils.rand_name('test-set')
        ctrl_list_fq_name = ['default-domain', 'admin', 'default',
                             ctrl_list_name]

        new_ctrl_list = self.client.create_access_control_lists(
                    fq_name=ctrl_list_fq_name,
                    parent_type="security-group")['access-'
                                                  'control-list']

        self.addCleanup(self._try_delete_resource,
                        self.client.delete_access_control_lists,
                        new_ctrl_list['uuid'])
        return new_ctrl_list

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_api_access_lists")
    @test.idempotent_id('2bfde8fd-36fe-4e69-ba59-6f2db8941e7d')
    def test_list_api_access_lists(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_api_access_lists()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_api_access_lists")
    @test.idempotent_id('b2b5f50c-07d8-4d79-b9a4-78187ad97353')
    def test_create_api_access_lists(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            new_api_list = self._create_api_access_lists()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_api_access_lists")
    @test.idempotent_id('b82e8e6b-83b5-424d-9652-ef6a34067f4f')
    def test_show_api_access_lists(self):
        new_api_list = self._create_api_access_lists()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_api_access_lists(new_api_list['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_api_access_lists")
    @test.idempotent_id('edc88825-1e2e-47ff-b7b4-f68d6310fbad')
    def test_update_api_access_lists(self):
        new_api_list = self._create_api_access_lists()
        update_name = data_utils.rand_name('test')
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_api_access_lists(new_api_list['uuid'],
                                                display_name=update_name)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_api_access_lists")
    @test.idempotent_id('f27d9044-95f2-4733-81ed-df9340dbd421')
    def test_delete_api_access_lists(self):
        new_api_list = self._create_api_access_lists()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_api_access_lists(new_api_list['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_access_control_lists")
    @test.idempotent_id('c56a1338-a9d1-4286-8aeb-3a0d60d93037')
    def test_list_access_control_lists(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_access_control_lists()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_access_control_lists")
    @test.idempotent_id('9f225d2b-5376-42f5-97aa-cf63be47fa19')
    def test_create_access_control_lists(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            new_ctrl_list = self._create_access_control_lists()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_access_control_lists")
    @test.idempotent_id('f0ed882b-f3de-48b7-884a-637ee0b7d6b6')
    def test_show_access_control_lists(self):
        new_ctrl_list = self._create_access_control_lists()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_access_control_lists(new_ctrl_list['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_access_control_lists")
    @test.idempotent_id('9a4b3133-dd07-4a1a-b282-f7770c372fb8')
    def test_update_access_control_lists(self):
        new_ctrl_list = self._create_access_control_lists()
        update_name = data_utils.rand_name('test')
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_access_control_lists(new_ctrl_list['uuid'],
                                                    display_name=update_name)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_access_control_lists")
    @test.idempotent_id('36a8ace1-71ca-4c7c-8667-d8387d6f964a')
    def test_delete_access_control_lists(self):
        new_ctrl_list = self._create_access_control_lists()
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.delete_access_control_lists(new_ctrl_list['uuid'])
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
