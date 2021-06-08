-- Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
-- SPDX-License-Identifier: MIT-0

-- See documentation on https://docs.aws.amazon.com/redshift/latest/dg/udf-creating-a-lambda-sql-udf.html
grant usage on language exfunc to PUBLIC;
CREATE OR REPLACE EXTERNAL FUNCTION public.geocode_address(
    VARCHAR, -- The address, name, city, or region to be used in the search. In free-form text format. For example, 123 Any Street. 
    VARCHAR, -- Bias position, a JSON array of doubles. Searches for results closest to the given position. An optional parameter defined by longitude, and latitude.
    VARCHAR -- Filter countries, a JSON array of strings. Limits the search to the given a list of countries/regions. An optional parameter.  
)
RETURNS VARCHAR -- A JSON with the address components (Latitude, Longitude, Label)
STABLE
LAMBDA 'RedshiftUDFGeocodeFunction'
IAM_ROLE 'arn:aws:iam::<AccountId>:role/RedshiftGeocodeFunctionRole';