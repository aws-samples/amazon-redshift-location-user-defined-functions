const AWS = require("aws-sdk");

// See related documentation: https://docs.aws.amazon.com/location/latest/developerguide/searching-for-places.html

const credentials = new AWS.CognitoIdentityCredentials({
   IdentityPoolId: "<identity pool ID>" // e.g., us-east-1:54f2ba88-9390-498d-aaa5-0d97fb7ca3bd
});

const client = new AWS.Location({
   credentials,
   region: AWS.config.region // region containing Cognito pool
});

// rsp.Results contains search results
const rsp = await location.searchPlaceIndexForText({
    IndexName: "ExamplePlaceIndex",
    Text: "Anyplace",
    BiasPosition: [-123.4567, 45.6789]
}).promise();
