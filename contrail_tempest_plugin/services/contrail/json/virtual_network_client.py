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
from oslo_log import log as logging

from contrail_tempest_plugin.services.contrail.json import base
from six.moves.urllib import parse as urllib

LOG = logging.getLogger(__name__)


class VirtualNetworkClient(base.BaseContrailClient):
    def create_virtual_networks(self, **kwargs):
        url = '/virtual-networks'
        post_body = json.dumps({'virtual-network': kwargs})
        LOG.debug("\n\nBeep creating a vn\n\n")
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return body

    def delete_virtual_networks(self, instance_id):
        url = '/virtual-network/%s' % str(instance_id)
        LOG.debug("\n\nBoop deleting a vn\n\n")
        return self.delete(url)
