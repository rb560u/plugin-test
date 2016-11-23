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
from contrail_tempest_plugin.services.contrail.json.namespace_client import \
    NamespaceClient

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class NamespaceContrailTest(base.BaseContrailTest):

    @classmethod
    def setup_clients(cls):
        super(NamespaceContrailTest, cls).setup_clients()
        cls.client = NamespaceClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_namespaces")
    def test_list_namespaces(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_namespaces()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_namespace")
    def test_create_namespace(self):
        was_created = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, ns_uuid = self.client.create_namespace()
            was_created = resp.status == 200
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_namespace(ns_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_namespace")
    def test_show_namespace(self):
        resp, ns_uuid = self.client.create_namespace()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_namespace(ns_uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_namespace(ns_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_namespace")
    def test_update_namespace(self):
        resp, ns_uuid = self.client.create_namespace()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_namespace(ns_uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_namespace(ns_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_namespace")
    def test_delete_namespace(self):
        resp, ns_uuid = self.client.create_namespace()
        was_created = resp.status == 200
        was_deleted = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, _ = self.client.delete_namespace(ns_uuid)
            was_deleted = resp.status == 200
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created and not was_deleted:
                self.client.delete_namespace(ns_uuid)
