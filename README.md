# aws_lambda_configurer

[![Build Status](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer.svg?branch=master)](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer)

## configuration

// supported lambda-config lookup

```json
{  
  "_lookup" : {
    "s3" : {
      "bucket" : "my-bucket"
      "key" : "my-config.json"
    }
  } 
  
  "foo": "bar" 
}

my-config.json
{
  "hello" : 123
}

final config
{
  "foo": "bar", 
  "hello" : 123
}

