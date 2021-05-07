# Amazon Redshift User Defined Functions to call Amazon Location Service APIs

This repository contain the code necessary to deploy [Amazon Redshift](https://github.com/fbdo/redshift-location-udf.git) Lambda-based [User Defined Functions](https://docs.aws.amazon.com/redshift/latest/dg/udf-creating-a-lambda-sql-udf.html) (UDF) to allow a user to call [Amazon Location Service](https://aws.amazon.com/location/) APIs, such as geocoding and reverse geocoding, as part of SQL queries.

## How to install

You can launch the code provided in this repository directly in you AWS account using the lauch button below:

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=RedshiftALS&templateURL=https://redshift-udf-als-dev.s3.eu-central-1.amazonaws.com/resources/cloudformation/create-lambda.yaml)

This CloudFormation temaplate uses a Custom Resource to copy lambdas from a central repository and install it in your account as described [here](https://aws.amazon.com/blogs/infrastructure-and-automation/deploying-aws-lambda-functions-using-aws-cloudformation-the-portable-way/). The template has the following parameters:

* OriginBucketName: The S3 bucket from where you are copying the lambda functions from. Should be kept unchanged (unless you know what are you doing).
* OriginKeyPrefix: The S3 bucket prefix that contains the lambda functions. Should be kept unchanged (unless you know what are you doing).
* PlaceIndex: A pre-existing place index. You need to create one before applying this template, please check [how to create a place index](https://docs.aws.amazon.com/location/latest/developerguide/create-place-index-resource.html).