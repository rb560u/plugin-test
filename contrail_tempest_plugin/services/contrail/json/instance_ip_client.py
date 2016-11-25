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

import json

from contrail_tempest_plugin.services.contrail.json import base
from six.moves.urllib import parse as urllib
from tempest.common.utils import data_utils

class InstanceIPClient(base.BaseContrailClient):

    def list_instance_ips(self, params=None):
        url = '/instance-ips'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_instance_ip(self, fq_name=None, **kwargs):
        if fq_name is None:
            fq_name = data_utils.rand_name('instance-ip')
        url = '/instance-ips'
        post_body = {
            'instance-ip': {
                'fq_name': [
#                    'default-domain',
#                    'admin',
                    fq_name
                ],
                'instance_ip_address': '1.2.3.4'
#                'virtual_network_refs': []
#                [{
#                    'to': [
#                        'default-domain'
#                    ],
#                    'attr': 'null',
#                    'href': 'null',
#                    'uuid': 'null'
#                }]
            }
        }
        if kwargs:
            post_body['instance-ip'].update(kwargs)

        print '+++++++++++++++++++++++++++++++++'
        print json.dumps(post_body)
        print '+++++++++++++++++++++++++++++++++'

        resp, body = self.post(url, json.dumps(post_body))
        resp_body = json.loads(body)

        print '+++++++++++++++++++++++++++++++++'
        print resp
        print body
        print '+++++++++++++++++++++++++++++++++'

        if 'instance-ip' in resp_body:
            return resp, resp_body['instance-ip']['uuid']
        return resp, None

    def show_instance_ip(self, uuid):
        url = '/instance-ip/{0}'.format(uuid)
        return self.get(url)

    def update_instance_ip(self, uuid, **kwargs):
        url = '/instance-ip/{0}'.format(uuid)
        put_body = {
            'instance-ip': {
                'display_name': data_utils.rand_name('instance-ip')
            }
        }
        if kwargs:
            post_body['instance-ip'].update(kwargs)
        return self.put(url, json.dumps(put_body))

    def delete_instance_ip(self, uuid):
        url = '/instance-ip/{0}'.format(uuid)
        return self.delete(url)
