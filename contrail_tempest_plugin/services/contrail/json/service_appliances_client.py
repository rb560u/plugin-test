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


class ServiceAppliancesClient(base.BaseContrailClient):
    def list_service_appliances(self, params=None):
        url = '/service-appliances'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_service_appliances(self, **kwargs):
        url = '/service-appliances'
        post_body = json.dumps({'service-appliance': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return body

    def show_service_appliances(self, appliance_id):
        url = '/service-appliance/%s' % str(appliance_id)
        return self.get(url)

    def delete_service_appliances(self, appliance_id):
        url = '/service-appliance/%s' % str(appliance_id)
        return self.delete(url)

    def update_service_appliances(self, appliance_id, **kwargs):
        url = '/service-appliance/%s' % str(appliance_id)
        post_body = json.dumps({'service-appliance': kwargs})
        return self.put(url, post_body)

    def list_service_appliance_sets(self, params=None):
        url = '/service-appliance-sets'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_service_appliance_sets(self, **kwargs):
        url = '/service-appliance-sets'
        post_body = json.dumps({'service-appliance-set': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return body

    def show_service_appliance_sets(self, appliance_id):
        url = '/service-appliance-set/%s' % str(appliance_id)
        return self.get(url)

    def delete_service_appliance_sets(self, appliance_id):
        url = '/service-appliance-set/%s' % str(appliance_id)
        return self.delete(url)

    def update_service_appliance_sets(self, appliance_id, **kwargs):
        url = '/service-appliance-set/%s' % str(appliance_id)
        post_body = json.dumps({'service-appliance-set': kwargs})
        return self.put(url, post_body)
