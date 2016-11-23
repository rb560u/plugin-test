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


class DomainClient(base.BaseContrailClient):

    def list_domains(self, params=None):
        url = '/domains'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_domain(self, fq_name=None, **kwargs):
        if fq_name is None:
            fq_name = data_utils.rand_name('domain')
        url = '/domains'
        post_body = {
            'domain': {
                'fq_name': [fq_name]
            }
        }
        if kwargs:
            post_body['domain'].update(kwargs)

        resp, body = self.post(url, json.dumps(post_body))
        resp_body = json.loads(body)

        if 'domain' in resp_body:
            return resp, resp_body['domain']['uuid']
        return resp, None

    def show_domain(self, uuid, params=None):
        url = '/domain/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def update_domain(self, uuid, **kwargs):
        url = '/domain/{0}'.format(uuid)
        put_body = {
            'domain': {
                'display_name': data_utils.rand_name('domain')
            }
        }
        if kwargs:
            post_body['domain'].update(kwargs)
        return self.put(url, json.dumps(put_body))

    def delete_domain(self, uuid):
        url = '/domain/{0}'.format(uuid)
        return self.delete(url)
