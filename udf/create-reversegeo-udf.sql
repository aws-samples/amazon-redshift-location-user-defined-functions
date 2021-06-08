-- Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
-- SPDX-License-Identifier: MIT-0

-- See documentation on https://docs.aws.amazon.com/redshift/latest/dg/udf-creating-a-lambda-sql-udf.html
grant usage on language exfunc to PUBLIC;
CREATE OR REPLACE EXTERNAL FUNCTION public.reverse_geocode_position(
    DOUBLE PRECISION, -- Latitude
    DOUBLE PRECISION  -- Longitude  
)
RETURNS VARCHAR -- A JSON with the address components (Country, PostalCode, AddressNumber, Street, etc...)
STABLE
LAMBDA 'RedshiftUDFReverseGeocodeFunction'
IAM_ROLE 'arn:aws:iam::<AccountId>:role/RedshiftReverseGeocodeFunctionRole';