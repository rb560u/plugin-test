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
from contrail_tempest_plugin.services.contrail.json.\
    virtual_ip_client import VirtualIPClient

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class VirtualIPTest(base.BaseContrailTest):

    @classmethod
    def setup_clients(cls):
        super(VirtualIPTest, cls).setup_clients()
        cls.client = VirtualIPClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_virtual_ips")
    def test_list_virtual_ips(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_virtual_ips()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_virtual_ip")
    def test_create_virtual_ip(self):
        was_created = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, virtual_ip_uuid = self.client.create_virtual_ip()
            was_created = resp.status == 200
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_virtual_ip(virtual_ip_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_virtual_ip")
    def test_show_virtual_ip(self):
        resp, virtual_ip_uuid = self.client.create_virtual_ip()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_virtual_ip(virtual_ip_uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_virtual_ip(virtual_ip_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_virtual_ip")
    def test_update_virtual_ip(self):
        resp, virtual_ip_uuid = self.client.create_virtual_ip()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_virtual_ip(virtual_ip_uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_virtual_ip(virtual_ip_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_virtual_ip")
    def test_delete_virtual_ip(self):
        resp, virtual_ip_uuid = self.client.create_virtual_ip()
        was_created = resp.status == 200
        was_deleted = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, _ = self.client.delete_virtual_ip(virtual_ip_uuid)
            was_deleted = resp.status == 200
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created and not was_deleted:
                self.client.delete_virtual_ip(virtual_ip_uuid)
