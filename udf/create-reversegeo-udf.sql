CREATE OR REPLACE EXTERNAL FUNCTION public.reverse_geocode_position(
    decimal(20, 17), -- Latitude
    decimal(20, 17) -- Longitude  
)
RETURNS VARCHAR -- A JSON with the address components (Country, PostalCode, AddressNumber, Street, etc...)
STABLE
LAMBDA 'RedshiftUDFReverseGeocodeFunction'
IAM_ROLE 'arn:aws:iam::201880502539:role/RedshiftReverseGeocodeFunctionRole';