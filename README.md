[![Build Status](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer.svg?branch=master)](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer)
[![Coverage Status](https://coveralls.io/repos/ImmobilienScout24/aws-lambda-configurer/badge.svg?branch=master&service=github)](https://coveralls.io/github/ImmobilienScout24/aws-lambda-configurer?branch=master)

# aws-lambda-configurer

This package allows to configure an AWS lambda function by JSON specified in the `description` of the lambda function.
The python function `aws_lambda_configurer.load_config` is passed the lambda-function `context` [argument](http://docs.aws.amazon.com/de_de/lambda/latest/dg/python-context-object.html) 
The result is a `dictionary` read from the JSON configuration.

## Basic usage

Lambda: Description
```JSON
{"foo":"bar"}
```

```python
from aws_lambda_configurer import load_config

def handler(event, context):
  myConfig = load_config(Context=context)
```  
  
## External configurations 

Since the lambda-description is limited to 256 chars, this module supports resolving the config from external locations.
To enable this, the configuration may contain a field `_lookup` which allows to define those lookups.
Any external configuration will be merged with the default one and the `_lookup` field gets removed.
During the merge all existing fields get overridden too.
   
### S3    

Configuration in S3 in bucket `my-bucket` as file `my-config.json`
```JSON
{
  "hello": 123,
  "override": "2"
}
```

Lambda: Description
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

## Todo

- Support more lookup types
