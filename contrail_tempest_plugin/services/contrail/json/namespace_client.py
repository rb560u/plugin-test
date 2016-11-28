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


class NamespaceClient(base.BaseContrailClient):

    def list_namespaces(self, params=None):
        url = '/namespaces'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_namespace(self, fq_name=None, **kwargs):
        if fq_name is None:
            fq_name = data_utils.rand_name('namespace')
        url = '/namespaces'
        post_body = {
            'namespace': {
                'parent_type': 'domain',
                'fq_name': ['default-domain', fq_name]
            }
        }
        if kwargs:
            post_body['namespace'].update(kwargs)

        resp, body = self.post(url, json.dumps(post_body))
        resp_body = json.loads(body)

        if 'namespace' in resp_body:
            return resp, resp_body['namespace']['uuid']
        return resp, None

    def show_namespace(self, uuid):
        url = '/namespace/{0}'.format(uuid)
        return self.get(url)

    def update_namespace(self, uuid, **kwargs):
        url = '/namespace/{0}'.format(uuid)
        put_body = {
            'namespace': {
                'display_name': data_utils.rand_name('namespace')
            }
        }
        if kwargs:
            put_body['namespace'].update(kwargs)
        return self.put(url, json.dumps(put_body))

    def delete_namespace(self, uuid):
        url = '/namespace/{0}'.format(uuid)
        return self.delete(url)
