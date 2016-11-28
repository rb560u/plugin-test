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


class RoutingPolicyClient(base.BaseContrailClient):

    def list_policies(self, params=None):
        url = '/routing-policys'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_policy(self, fq_name=None, **kwargs):
        if fq_name is None:
            fq_name = data_utils.rand_name('routing-policy')
        url = '/routing-policys'
        post_body = {
            'routing-policy': {
                'parent_type': 'project',
                'fq_name': ["default-domain", "default-project", fq_name]
            }
        }
        if kwargs:
            post_body['routing-policy'].update(kwargs)

        resp, body = self.post(url, json.dumps(post_body))
        resp_body = json.loads(body)

        if 'routing-policy' in resp_body:
            return resp, resp_body['routing-policy']['uuid']
        return resp, None

    def show_policy(self, uuid, params=None):
        url = '/routing-policy/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def update_policy(self, uuid, **kwargs):
        url = '/routing-policy/{0}'.format(uuid)
        put_body = {
            'routing-policy': {
                'display_name': data_utils.rand_name('routing-policy')
            }
        }
        if kwargs:
            put_body['routing-policy'].update(kwargs)
        return self.put(url, json.dumps(put_body))

    def delete_policy(self, uuid):
        url = '/routing-policy/{0}'.format(uuid)
        return self.delete(url)
