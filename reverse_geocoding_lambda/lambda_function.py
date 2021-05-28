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
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

    arguments = event["arguments"]

    logger.debug('Received arguments: %s.', arguments)

    results = []

    try:
        for arg in arguments:
            req = {'IndexName': PLACE_INDEX, 'Position': [arg[1], arg[0]]}
            
            response = client.search_place_index_for_position(**req)
            results.append(json.dumps({
                    "Longitude": response["Results"][0]["Place"]["Geometry"]["Point"][0],
                    "Latitude": response["Results"][0]["Place"]["Geometry"]["Point"][1],
                    "Label": response["Results"][0]["Place"]["Label"]
                }))

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
