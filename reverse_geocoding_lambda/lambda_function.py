from datetime import datetime
import json
import os
import boto3
import botocore
from botocore.exceptions import ClientError
import logging as log

PLACE_INDEX = os.environ['PLACE_INDEX']

"""
Valid request
{
  "arguments": [
    [48.199323, 11.612921]
  ]
}
"""
def handler(event, context):
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

    log.getLogger().setLevel(log.INFO)

    session_config = botocore.config.Config(
        user_agent="Redshift/1.0 Amazon Location Service UDF"
    )
    client = boto3.client(
        "location",
        config=session_config
    )
    arguments = event["arguments"]

    log.info('Received arguments: {}'.format(arguments))

    results = []

    try:
        for arg in arguments:
            req = {'IndexName': PLACE_INDEX, 'Position': arg}
            
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
        log.error('Error: {}'.format(e))
        return {
            "success": False,
            "error_msg": str(e),
            "num_records": 0,
            "results": []
        }
