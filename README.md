# Amazon Redshift User Defined Functions to call Amazon Location Service APIs

This repository contain the code necessary to deploy [Amazon Redshift](https://github.com/fbdo/redshift-location-udf.git) Lambda-based [User Defined Functions](https://docs.aws.amazon.com/redshift/latest/dg/udf-creating-a-lambda-sql-udf.html) (UDF) to allow a user to call [Amazon Location Service](https://aws.amazon.com/location/) APIs, such as geocoding and reverse geocoding, as part of SQL queries.

## How to install

As a pre-requisite, create a new Amazon Location Service place index if you don't have already one you use. Follow the instructions in [Create a place index resource](https://docs.aws.amazon.com/location/latest/developerguide/create-place-index-resource.html).

You can launch the code provided in this repository directly in you AWS account using the lauch button below:

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=RedshiftUDFsforAmazonLocationService&templateURL=https://redshift-udf-als-dev.s3.eu-central-1.amazonaws.com/resources/cloudformation/create-lambda.yaml)

This CloudFormation temaplate uses a Custom Resource to copy lambdas from a central repository and install it in your account as described [here](https://aws.amazon.com/blogs/infrastructure-and-automation/deploying-aws-lambda-functions-using-aws-cloudformation-the-portable-way/). The template has the following parameters:

* OriginBucketName: The S3 bucket from where you are copying the lambda functions from. Should be kept unchanged (unless you know what are you doing).
* OriginKeyPrefix: The S3 bucket prefix that contains the lambda functions. Should be kept unchanged (unless you know what are you doing).
* PlaceIndex: A pre-existing place index. You need to create one before applying this template.

## How to test
* Create a new RedShift cluster if you don't have one already. Follow the instructions in [Getting started with Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html).
* Attach the IAM roles RedshiftGeocodeFunctionRole and RedshiftReverseGeocodeFunctionPolicy created by this CloudFormation template to your cluster. You can add a role to a cluster or view the roles associated with a cluster by using the Amazon Redshift Management Console, CLI, or API. For more information, see [Associating an IAM Role With a Cluster](https://docs.aws.amazon.com/redshift/latest/mgmt/copy-unload-iam-role.html) in the Amazon Redshift Cluster Management Guide. 
* Connect to your database
* Open an Editor and execute the instructions in the file [create-geocoding-udf.sql](https://github.com/fbdo/redshift-location-udf/blob/master/udf/create-geocoding-udf.sql). This will give the required permissions and create public external function pointing to out lambda. Don't forget to replace the <AccountId> placeholder with your AWS account it.
* To test the geocoding, create a new table and populate it with data as below:

```sql
create table places(address varchar (200));
insert into places values 
('Domagkstraße 28'),
('Marcel-Breuer-Straße 12');
```
* Execute a query using the newly created lambda as in:

```sql
select address, 
json_extract_path_text(geocode_address(address, '[48.192087, 11.617126]','["DEU"]'), 'Label') as full_address
from places; 
```
