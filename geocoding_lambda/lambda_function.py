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
            # populate the response list in the same orders as the arguments list

        return {
            "success": true,
            "num_records": len(response),
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
