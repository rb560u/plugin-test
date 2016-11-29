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

from contrail_tempest_plugin.services.contrail.json import base
from six.moves.urilib import parse as urilib
from oslo_serialization import jsonutils as json


class VirtualNetworkClient(base.BaseContrailClient):

    def get_virtual_networks(self, params=None):
        uri = '/virtual-networks'
        return self.get(uri)

    def create_virtual_network(self, **kwargs):
        uri = '/virtual-networks'
        post_body = json.dumps({'virtual-network': kwargs})
        resp, body = self.post(uri, post_body)
        body = json.loads(body)
        return resp, body

    def update_virtual_network(self, uuid, **kwargs):
        uri = '/virtual-network/%s' % uuid
        post_data = {'virtual-network': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(uri, req_post_data)
        body = json.loads(body)
        return resp, body

    def delete_virtual_network(self, id):
        uri = '/virtual-network/%s' % id
        return self.delete(uri)

    def show_virtual_network(self, id):
        uri = '/virtual-network/%s' % id
        return self.get(uri)
