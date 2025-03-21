# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import logging

from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkdeh.v1 import *

from c7n.utils import type_schema
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo

log = logging.getLogger("custodian.huaweicloud.resources.deh")


@resources.register('deh')
class Deh(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'deh'
        enum_spec = ("list_dedicated_hosts", 'dedicated_hosts', 'offset')
        id = 'dedicated_host_id'
        tag = True

@Deh.action_registry.register("update-dedicated-host")
class UpdateDedicatedHost(HuaweiCloudBaseAction):
    """Update Dedicated Host.

    :Example:

    .. code-block:: yaml

        policies:
          - name: update-dedicated-host
            resource: huaweicloud.deh
            flters:
              - type: value
                key: metadata.__system__encrypted
                value: "0"
            actions:
              - delete
    """

    schema = type_schema(
        "update-dedicated-host",
        required=['dedicated_host_id'],
        **{
            "dedicated_host_id": {"type": "string"},
            "dedicated_host": {
                "type": "object",
                "properties": {
                    "auto_placement": {"type": "string", "enum": ["on", "off"]},
                    "name": {"type": "string"},
                }

            },
        }
    )

    def perform_action(self, resource):
        client = self.manager.get_client()
        request = UpdateDedicatedHostRequest()
        response = client.update_dedicated_host(request)
        log.info(f"Received Job ID:{response.job_id}")
        # TODO: need to track whether the job succeed
        response = None
        return response