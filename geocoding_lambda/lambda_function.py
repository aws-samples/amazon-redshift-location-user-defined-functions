from datetime import datetime
import json
import os
from botocore.exceptions import ClientError
import logging as log

import boto3

PLACE_INDEX = os.environ['PLACE_INDEX']

""" 
Valid request:
{
  "arguments": [
    [
      "Englisch Garten",
      "[48.192087, 11.617126]",
      "[\"DEU\"]"
    ]
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
            text, bias_position, filter_countries = arg
            log.debug('Received search text: {}'.format(text))
            log.debug('Received bias position: {}'.format(bias_position))
            log.debug('Received filter countries: {}'.format(filter_countries))

            req = {'Text': text, 'IndexName': PLACE_INDEX}
            if filter_countries and json.loads(filter_countries):
                req['FilterCountries'] = json.loads(filter_countries)

            if bias_position and json.loads(bias_position):
                req['BiasPosition'] = json.loads(bias_position)

            response = client.search_place_index_for_text(**req)
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
