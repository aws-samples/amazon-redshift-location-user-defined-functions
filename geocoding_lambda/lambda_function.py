from datetime import datetime
import json
import os
from botocore.exceptions import ClientError
import logging as log

import boto3

PLACE_INDEX = os.environ['PLACE_INDEX']

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
            log.info('Received search text: {}'.format(text))
            log.info('Received bias position: {}'.format(bias_position))
            log.info('Received filter countries: {}'.format(filter_countries))
            fc = json.loads(filter_countries) if not filter_countries == "" else []
            bp = json.loads(bias_position) if not bias_position == "" else None
            response = client.search_place_index_for_text(
                Text=text,
                IndexName=PLACE_INDEX,
                FilterCountries=fc,
                BiasPosition=bp
            )
            results.append(response)

        return {
            "success": true,
            "num_records": len(results),
            "results": results
        }

    except ClientError as e:
        log.error('Error: {}'.format(e))
        return {
            "success": false,
            "error_msg": str(e),
            "num_records": 0,
            "results": []
        }
