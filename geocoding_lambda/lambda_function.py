from datetime import datetime
import json
import os

import boto3

PLACE_INDEX = os.environmen['PLACE_INDEX']

def lambda_handler(event, context):
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

    client = boto3.client("location")
    arguments = event["arguments"]

    results = []

    try:
        for arg in arguments:
            text, bias_position, filter_countries = arg
            response = client.search_place_index_for_text(
                Text=text,
                IndexName=PLACE_INDEX,
                FilterCountries=json.loads(filter_countries),
                BiasPosition=json.loads(bias_position)
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
            "error_msg": str(e)
            "num_records": 0,
            "results": []
        }
