import os
import json
import logging
from json.decoder import JSONDecodeError
from typing import Tuple, Optional, List

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
    logger = logging.getLogger(__name__)
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]
    
    arguments = event["arguments"]
    logger.debug('Received arguments: %s.', arguments)

    results = []
    try:
        for arg in arguments:
            text = arg[0]
            logger.debug('Received search text: %s.', text)
            req = {'Text': text, 'IndexName': PLACE_INDEX}

            is_arg_valid, bias_position = validate_bias_position_arg(arg[1])
            if is_arg_valid:
                logger.debug('Received bias position: %s.', bias_position)
                req['BiasPosition'] = bias_position

            is_arg_valid, filter_countries = validate_filter_countries_arg(arg[2])
            if is_arg_valid:
                logger.debug('Received filter countries: %s.', filter_countries)
                req['FilterCountries'] = filter_countries

            response = client.search_place_index_for_text(**req)
            logger.debug('Response received from ALS client: %s.', response)

            if len(response["Results"]) >= 1:
                results.append(json.dumps({
                    "Longitude": response["Results"][0]["Place"]["Geometry"]["Point"][0],
                    "Latitude": response["Results"][0]["Place"]["Geometry"]["Point"][1],
                    "Label": response["Results"][0]["Place"]["Label"]
                }))
            else:
                results.append({})

        logger.debug('Returning results: %s.', results)

        return json.dumps({
            "success": True,
            "num_records": len(results),
            "results": results
        })

    except ClientError as e:
        logger.error('Error: %s.', e)
        return json.dumps({
            "success": False,
            "error_msg": str(e),
            "num_records": 0,
            "results": []
        })


def validate_bias_position_arg(arg: str) -> Tuple[bool, Optional[List[float]]]:
  logger = logging.getLogger(__name__)
  bias_position_arg = None
  try:
    assert isinstance(arg, str) and len(arg.strip())
    bias_position_arg = json.loads(arg)
  except (AssertionError, JSONDecodeError) as exc:
    logger.debug(exc)
    logger.error('Argument provided is not a JSON string.')
    return False, None

  try:
    assert isinstance(bias_position_arg, list) and len(bias_position_arg) == 2
    for bias_coord in bias_position_arg:
      assert isinstance(bias_coord, float)
  except AssertionError as exc:
    logger.debug(exc)
    logger.error('Argument provided is not a list of float numbers.')
    return False, None

  return True, bias_position_arg


def validate_filter_countries_arg(arg: str) -> Tuple[bool, Optional[List[str]]]:
    logger = logging.getLogger(__name__)
    filter_countries_arg = None
    try:
        assert isinstance(arg, str) and len(arg.strip())
        filter_countries_arg = json.loads(arg)
    except (AssertionError, JSONDecodeError) as exc:
        logger.debug(exc)
        logger.error('Argument provided is not a JSON string.')
        return False, None
    
    try:
        assert isinstance(filter_countries_arg, list) and len(filter_countries_arg) > 0
        for country_arg in filter_countries_arg:
            assert isinstance(country_arg, str) and len(country_arg.strip()) > 0
    except AssertionError as exc:
        logger.debug(exc)
        logger.error('Argument provided is not a list of strings.')
        return False, None
    
    return True, filter_countries_arg
