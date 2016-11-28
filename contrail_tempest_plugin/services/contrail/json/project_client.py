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


class ProjectClient(base.BaseContrailClient):

    def list_projects(self, params=None):
        url = '/projects'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_project(self, fq_name=None, **kwargs):
        if fq_name is None:
            fq_name = data_utils.rand_name('project')
        url = '/projects'
        post_body = {
            'project': {
                'parent_type': 'domain',
                'fq_name': ['default-domain', fq_name]
            }
        }
        if kwargs:
            post_body['project'].update(kwargs)

        resp, body = self.post(url, json.dumps(post_body))
        resp_body = json.loads(body)

        if 'project' in resp_body:
            return resp, resp_body['project']['uuid']
        return resp, None

    def show_project(self, uuid, params=None):
        url = '/project/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def update_project(self, uuid, **kwargs):
        url = '/project/{0}'.format(uuid)
        put_body = {
            'project': {
                'display_name': data_utils.rand_name('project')
            }
        }
        if kwargs:
            put_body['project'].update(kwargs)
        return self.put(url, json.dumps(put_body))

    def delete_project(self, uuid):
        url = '/project/{0}'.format(uuid)
        return self.delete(url)
