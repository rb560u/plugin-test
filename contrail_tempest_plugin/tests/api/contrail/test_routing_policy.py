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
    routing_policy_client import RoutingPolicyClient

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class RoutingPolicyTest(base.BaseContrailTest):

    @classmethod
    def setup_clients(cls):
        super(RoutingPolicyTest, cls).setup_clients()
        cls.client = RoutingPolicyClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_routing_policies")
    def test_list_policies(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.list_policies()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_routing_policy")
    def test_create_policy(self):
        was_created = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, policy_uuid = self.client.create_policy()
            was_created = resp.status == 200
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_policy(policy_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_routing_policy")
    def test_show_policy(self):
        resp, policy_uuid = self.client.create_policy()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_policy(policy_uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_policy(policy_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_routing_policy")
    def test_update_policy(self):
        resp, policy_uuid = self.client.create_policy()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_policy(policy_uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_policy(policy_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_routing_policy")
    def test_delete_policy(self):
        resp, policy_uuid = self.client.create_policy()
        was_created = resp.status == 200
        was_deleted = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, _ = self.client.delete_policy(policy_uuid)
            was_deleted = resp.status == 200
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created and not was_deleted:
                self.client.delete_policy(policy_uuid)
