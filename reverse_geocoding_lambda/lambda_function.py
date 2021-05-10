from datetime import datetime
import json
import os
import boto3
from botocore.exceptions import ClientError
import logging as log

PLACE_INDEX = os.environ['PLACE_INDEX']

"""
Valid request
{
  "arguments": [
    "[48.199323, 11.612921]"
  ]
}
"""
def handler(event, context):
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

    log.getLogger().setLevel(log.INFO)
    client = boto3.client("location")
    arguments = event["arguments"]

    log.info('Received arguments: {}'.format(arguments))

    results = []

    try:
        for arg in arguments:
            req = {'IndexName': PLACE_INDEX}
            if arg and json.loads(arg):
                req['Position'] = json.loads(arg)
            
            response = client.search_place_index_for_position(**req)
            results.append(response)

        return {
            "success": True,
            "num_records": len(results),
            "results": results
        }
    except ClientError as e:
        log.error('Error: {}'.format(e))
        return {
            "success": False,
            "error_msg": str(e),
            "num_records": 0,
            "results": []
        }
