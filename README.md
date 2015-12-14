# aws_lambda_configurer

[![Build Status](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer.svg?branch=master)](https://travis-ci.org/ImmobilienScout24/aws-lambda-configurer)
[![Code Health](https://landscape.io/github/ImmobilienScout24/aws-lambda-configurer/master/landscape.svg?style=flat)](https://landscape.io/github/ImmobilienScout24/aws-lambda-configurer/master)

## configuration

```json
{
  // supported lambda-config lookup
  "_lookup" : {
    "s3" : {
      "bucket" : "my-bucket"
      "key" : "my-config.json"
    }
  }
  
  // timestamp field in logs. default: @timestamp
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

