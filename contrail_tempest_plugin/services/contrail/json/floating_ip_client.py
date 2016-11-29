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
from oslo_serialization import jsonutils as json
from six.moves.urllib import parse as urllib


class FloatingIpClient(base.BaseContrailClient):

    def create_floating_ip_pool(self, **kwargs):
        uri = '/floating-ip-pools'

        post_data = {'floating-ip-pool': kwargs}
        req_post_data = json.dumps(post_data)

        resp, body = self.post(uri, req_post_data)
        body = json.loads(body)
        return resp, body

    def list_floating_ip_pools(self, **kwargs):
        uri = '/floating-ip-pools'

        if kwargs:
            uri += '?' + urllib.urlencode(kwargs)

        resp, body = self.get(uri)
        body = json.loads(body)
        return resp, body

    def update_floating_ip_pool(self, floatingip_pool_id, **kwargs):
        uri = '/floating-ip-pool/%s' % floatingip_pool_id

        post_data = {'floating-ip-pool': kwargs}
        req_post_data = json.dumps(post_data)

        resp, body = self.put(uri, req_post_data)
        body = json.loads(body)
        return resp, body

    def show_floating_ip_pool(self, floatingip_pool_id, **fields):
        uri = '/floating-ip-pool/%s' % floatingip_pool_id

        # fields is a dict which key is 'fields' and value is a
        # list of field's name. An example:
        # {'fields': ['id', 'name']}
        if fields:
            uri += '?' + urllib.urlencode(fields)

        resp, body = self.get(uri)
        body = json.loads(body)
        return resp, body

    def delete_floating_ip_pool(self, floatingip_pool_id):
        uri = '/floating-ip-pool/%s' % floatingip_pool_id
        return self.delete(uri)

    def create_floating_ip(self, **kwargs):
        uri = '/floating-ips'

        post_data = {'floating-ip': kwargs}
        req_post_data = json.dumps(post_data)

        resp, body = self.post(uri, req_post_data)
        body = json.loads(body)
        return resp, body

    def list_floating_ips(self, **kwargs):
        uri = '/floating-ips'

        if kwargs:
            uri += '?' + urllib.urlencode(kwargs)

        resp, body = self.get(uri)
        body = json.loads(body)
        return resp, body

    def show_floating_ip(self, floatingip_id, **fields):
        uri = '/floating-ip/%s' % floatingip_id

        # fields is a dict which key is 'fields' and value is a
        # list of field's name. An example:
        # {'fields': ['id', 'name']}
        if fields:
            uri += '?' + urllib.urlencode(fields)

        resp, body = self.get(uri)
        body = json.loads(body)
        return resp, body

    def update_floating_ip(self, floatingip_id, **kwargs):
        uri = '/floating-ip/%s' % floatingip_id

        post_data = {'floating-ip': kwargs}
        req_post_data = json.dumps(post_data)

        resp, body = self.put(uri, req_post_data)
        body = json.loads(body)
        return resp, body

    def delete_floating_ip(self, floatingip_id):
        uri = '/floating-ip/%s' % floatingip_id
        return self.delete(uri)
