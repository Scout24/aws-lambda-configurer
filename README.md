[![Build Status](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer.svg?branch=master)](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer)
[![Coverage Status](https://coveralls.io/repos/ImmobilienScout24/aws-lambda-configurer/badge.svg?branch=master&service=github)](https://coveralls.io/github/ImmobilienScout24/aws-lambda-configurer?branch=master)

# aws-lambda-configurer

This package allows to configure an AWS lambda function by JSON specified in the `description` of the lambda function.
The python function `aws_lambda_configurer.load_config` is passed the lambda-function `context` [argument](http://docs.aws.amazon.com/de_de/lambda/latest/dg/python-context-object.html) 
The result is a `dictionary` read from the JSON configuration.

## Basic usage

Set the `description` of your Lambda function to some valid JSON like
```JSON
{"foo":"bar"}
```
You can retrieve this data in your lambda function with
```python
from aws_lambda_configurer import load_config

def handler(event, context):
  my_config = load_config(Context=context)
```
The `my_config` variable is now set to the dictionary defined by the JSON.
  
## External configurations 

Since the lambda-description is limited to 256 chars, this module supports resolving the config from external locations.
To enable this, the configuration may contain a field `_lookup` which allows to define those lookups.
Any external configuration will be merged with the default one and the `_lookup` field gets removed.
   
### S3    

Configuration in S3 in bucket `my-bucket` as file `my-config.json`
```JSON
{
  "hello": 123,
  "override": "2"
}
```

Set the `description` of your lambda to
```JSON
{  
  "_lookup" : {
    "s3": {
      "bucket": "my-bucket",
      "key": "my-config.json"
    }
  }, 
  "foo": "bar",
  "override": "1"
}
```

The final configuration will be
```JSON
{
  "hello": 123,
  "foo": "bar", 
  "override": "2"
}
```
Notice that the `override` variable in the final config is "2", not "1". Values in the S3 bucket take precedence over those in the lambda function's description.

## Todo

- Support more lookup types
