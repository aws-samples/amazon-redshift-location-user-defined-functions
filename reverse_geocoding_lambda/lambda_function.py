from datetime import datetime
import json
import os

import boto3


def lambda_handler(event, context):
  # load the side-loaded Amazon Location Service model; needed during Public Preview
  os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

  client = boto3.client("location")
  arguments = event["arguments"]

  results = []

  for arg in arguments:
    # populate the response list in the same orders as the arguments list

  return {
    "success": true,
    "num_records": len(response),
    "results": results
  }