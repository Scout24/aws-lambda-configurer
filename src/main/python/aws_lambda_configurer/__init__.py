__version__ = '${version}'

import json

import boto3

aws_lambda = boto3.client('lambda')
s3_client = boto3.client('s3')


def _lookup_s3(config):
    bucket = config.get('bucket')
    key = config.get('key')

    if not bucket:
        raise Exception("S3 lookup config needs field 'bucket'")
    if not key:
        raise Exception("S3 lookup config needs field 'key'")

    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read()
    return json.loads(content)


def _lookup(config):
    lookup = config.get('_lookup')

    if lookup:
        if lookup.get('s3'):
            config.update(_lookup_s3(lookup.get('s3')))
        del config['_lookup']

    return config


def load_config(context):
    # http://docs.aws.amazon.com/de_de/lambda/latest/dg/python-context-object.html
    description = aws_lambda.get_function_configuration(
        FunctionName=context.invoked_function_arn,
        Qualifier=context.function_version
    )['Description']

    try:
        return _lookup(json.loads(description))
    except ValueError:
        raise Exception('Description of function must contain JSON, but was "{0}"'.format(description))
