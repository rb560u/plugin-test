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
from contrail_tempest_plugin.services.contrail.json.instance_ip_client import \
    InstanceIPClient
from contrail_tempest_plugin.services.contrail.json import \
    virtual_network_client

from tempest.common.rbac import rbac_rule_validation
from tempest.common.rbac.rbac_utils import rbac_utils
from tempest.common.utils import data_utils

from tempest import config
from tempest import test

CONF = config.CONF
LOG = logging.getLogger(__name__)


class InstanceIPTest(base.BaseContrailTest):

    @classmethod
    def setup_clients(cls):
        super(InstanceIPTest, cls).setup_clients()
        cls.auth_provider = cls.os.auth_provider
        cls.client = InstanceIPClient(
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
                                 rule="list_instance_ips")
    def test_list_instance_ips(self):
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            body = self.client.list_instance_ips()
            print '******************************'
            print 'test_list_instance_ips'
            print body
            print '******************************'
        finally:
            print '******************************'
            print 'test_list_instance_ips'
            print body
            print '******************************'
            rbac_utils.switch_role(self, switchToRbacRole=False)

    def test_create_instance_ip(self):
        was_created = False
        new_vn =\
            self.vn_client.create_virtual_networks(
                parent_type='project',
                fq_name=self._generate_names())['virtual-network']
        print '++++++++++++++++++++++++++++++++'
        print new_vn
        print '++++++++++++++++++++++++++++++++'
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, iip_uuid = self.client.create_instance_ip(
            virtual_network_refs=
                [{
                    'to': new_vn['fq_name'],
                    'href': new_vn['href'],
                    'uuid': new_vn['uuid']
                }]
            )
            was_created = resp.status == 200
            print '******************************'
            print 'test_create_instance_ip'
            print resp
            print iip_uuid
            print was_created
            print '******************************'
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_instance_ip(iip_uuid)
            self.vn_client.delete_virtual_networks(new_vn['uuid'])

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="show_instance_ip")
    def test_show_instance_ip(self):
        resp, iip_uuid = self.client.create_instance_ip()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.show_instance_ip(iip_uuid)
            print '******************************'
            print 'test_show_instance_ip'
            print resp
            print iip_uuid
            print was_created
            print '******************************'
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_instance_ip(iip_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="update_instance_ip")
    def test_update_instance_ip(self):
        resp, iip_uuid = self.client.create_instance_ip()
        was_created = resp.status == 200
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            self.client.update_instance_ip(iip_uuid)
            print '******************************'
            print 'test_update_instance_ip'
            print resp
            print iip_uuid
            print was_created
            print '******************************'
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created:
                self.client.delete_instance_ip(iip_uuid)

    @test.attr(type='rbac')
    @rbac_rule_validation.action(component="Contrail",
                                 rule="delete_instance_ip")
    def test_delete_instance_ip(self):
        resp, iip_uuid = self.client.create_instance_ip()
        was_created = resp.status == 200
        was_deleted = False
        rbac_utils.switch_role(self, switchToRbacRole=True)
        try:
            resp, _ = self.client.delete_instance_ip(iip_uuid)
            was_deleted = resp.status == 200
            print '******************************'
            print 'test_delete_instance_ip'
            print resp
            print iip_uuid
            print was_deleted
            print '******************************'
        finally:
            rbac_utils.switch_role(self, switchToRbacRole=False)
            if was_created and not was_deleted:
                self.client.delete_instance_ip(iip_uuid)
