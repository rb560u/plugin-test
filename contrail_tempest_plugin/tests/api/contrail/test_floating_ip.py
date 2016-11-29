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


class BaseFloatingIpTest(base.BaseContrailTest):

    @classmethod
    def skip_checks(cls):
        super(BaseFloatingIpTest, cls).skip_checks()

        if not CONF.identity.rbac_flag:
            raise cls.skipException(
                '%s skipped as RBAC flag not enabled' % cls.__name__)
        if 'admin' not in CONF.auth.tempest_roles:
            raise cls.skipException(
                "%s skipped - RBAC tests require tempest_roles to be admin"
                % cls.__name__)

    @classmethod
    def resource_setup(cls):
        super(BaseFloatingIpTest, cls).resource_setup()

        # Create network to test floating ip pool CRUD
        net_name = data_utils.rand_name('rbac-pool-network')
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
        super(BaseFloatingIpTest, cls).resource_cleanup()

    def _create_floating_ip_pool(self):

        pool_name = data_utils.rand_name('rbac-fip-pool')
        fq_name = ['default-domain', 'admin', self.network['name'], pool_name]

        post_body = {'display_name': pool_name}
        post_body['parent_type'] = 'virtual-network'
        post_body['fq_name'] = fq_name

        resp, body = self.fip_client.create_floating_ip_pool(**post_body)
        fip_pool = body['floating-ip-pool']

        self.addCleanup(self._try_delete_resource,
                        self.fip_client.delete_floating_ip_pool,
                        fip_pool['uuid'])

        return fip_pool


class FloatingIpPoolTest(BaseFloatingIpTest):

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_floating_ip_pools")
    def test_create_floating_ip_pool(self):

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self._create_floating_ip_pool()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_floating_ip_pools")
    def test_list_floating_ip_pools(self):

        self._create_floating_ip_pool()['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.list_floating_ip_pools()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="get_floating_ip_pool")
    def test_show_floating_ip_pool(self):

        uuid = self._create_floating_ip_pool()['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.show_floating_ip_pool(uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_floating_ip_pool")
    def test_update_floating_ip_pool(self):

        uuid = self._create_floating_ip_pool()['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.update_floating_ip_pool(
                uuid,
                display_name='rbac-fip-pool-new-name')
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_floating_ip_pool")
    def test_delete_floating_ip_pool(self):

        uuid = self._create_floating_ip_pool()['uuid']
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.delete_floating_ip_pool(uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)


class FloatingIpTest(BaseFloatingIpTest):

    @classmethod
    def skip_checks(cls):
        super(FloatingIpTest, cls).skip_checks()

        raise cls.skipException(
            '%s skipped as subnet creation via api is not working yet'
            % cls.__name__)

    @classmethod
    def resource_setup(cls):
        super(FloatingIpTest, cls).resource_setup()

        # Network is created in base class
        # Create subnet for the network to test floating ip CRUD
        """
        subnet_name = data_utils.rand_name('rbac-pool-subnet')
        fq_name_subnet = ['default-domain',
                          'admin',
                          self.network['name'],
                          subnet_name]

        subnet_ip_prefix = {'ip_prefix': '10.11.12.0', 'ip_prefix_len': 24}

        subnet_post_body = {'display_name' : subnet_name}
        subnet_post_body['parent_type'] = 'TBD'
        subnet_post_body['subnet_ip_prefix'] = subnet_ip_prefix
        subnet_post_body['fq_name'] = fq_name_subnet

        resp, body = cls.vn_client.create_subnet(**subnet_post_body)
        cls.subnet = body['subnet']['name']
        """

    @classmethod
    def resource_cleanup(cls):

        super(FloatingIpTest, cls).resource_cleanup()

    def _create_floating_ip(self, fip_pool):

        fip_name = data_utils.rand_name('rbac-fip')
        fq_name = ['default-domain', 'admin', self.network['name'],
                   fip_pool['name'], fip_name]
        project_refs = {'to': ['default-domain', 'admin']}

        post_body = {'display_name': fip_name}
        post_body['parent_type'] = 'floating-ip-pool'
        post_body['fq_name'] = fq_name
        post_body['project_refs'] = [project_refs]

        resp, body = self.fip_client.create_floating_ip(**post_body)
        fip = body['floating-ip']

        self.addCleanup(self._try_delete_resource,
                        self.fip_client.delete_floating_ip,
                        fip['uuid'])
        return fip

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="create_floating_ips")
    def test_create_floating_ip(self):

        # Create floating ip pool
        fip_pool = self._create_floating_ip_pool()

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self._create_floating_ip(fip_pool)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="list_floating_ips")
    def test_list_floating_ips(self):

        # Create floating ip pool
        fip_pool = self._create_floating_ip_pool()
        self._create_floating_ip(fip_pool)

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.list_floating_ips()
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="get_floating_ip")
    def test_show_floating_ip(self):

        # Create floating ip pool
        fip_pool = self._create_floating_ip_pool()
        uuid = self._create_floating_ip(fip_pool)['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.show_floating_ip(uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_floating_ip")
    def test_update_floating_ip(self):

        # Create floating ip pool
        fip_pool = self._create_floating_ip_pool()
        uuid = self._create_floating_ip(fip_pool)['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.update_floating_ip(
                uuid,
                display_name='rbac-fip-new-name')
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_floating_ip")
    def test_delete_floating_ip(self):

        # Create floating ip pool
        fip_pool = self._create_floating_ip_pool()
        uuid = self._create_floating_ip(fip_pool)['uuid']

        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.fip_client.delete_floating_ip(uuid)
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
