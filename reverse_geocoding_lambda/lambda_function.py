""" 
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import json
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

PLACE_INDEX = os.environ['PLACE_INDEX']

logging.basicConfig(level=logging.INFO)

client_config = Config(
    user_agent="Redshift/1.0 Amazon Location Service UDF",
    retries = {
        'mode': 'standard'
    }
)
client = boto3.client(
    "location",
    config=client_config
)

"""
Valid request
{
  "arguments": [
    [48.199323, 11.612921]
  ]
}
"""
def handler(event, context):
    logger = logging.getLogger(__name__)

    arguments = event["arguments"]

    logger.debug('Received arguments: %s.', arguments)

    results = []

    try:
        for arg in arguments:
            req = {'IndexName': PLACE_INDEX, 'Position': [arg[1], arg[0]]}
            
            response = client.search_place_index_for_position(**req)

            if len(response["Results"]) >= 1:
                results.append(json.dumps({
                    "Longitude": response["Results"][0]["Place"]["Geometry"]["Point"][0],
                    "Latitude": response["Results"][0]["Place"]["Geometry"]["Point"][1],
                    "Label": response["Results"][0]["Place"]["Label"]
                }))
            else:
                results.append({})

        return json.dumps({
            "success": True,
            "num_records": len(results),
            "results": results
        })
    except ClientError as e:
        logger.error('Error: %s.', e)
        return {
            "success": False,
            "error_msg": str(e),
            "num_records": 0,
            "results": []
        }
