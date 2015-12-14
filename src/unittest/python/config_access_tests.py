from __future__ import print_function

import os

os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"

import aws_lambda_configurer
import json
import unittest2
from mock import patch, MagicMock


class ConfigAccessTests(unittest2.TestCase):
    @patch('aws_lambda_configurer.aws_lambda')
    def test_get_config(self, aws_lambda_mock):
        aws_lambda_mock.get_function_configuration.return_value = {
            'Description': json.dumps({
                'endpoint': 'knuff.eu-west-1.es.amazonaws.com'
            })
        }

        config = aws_lambda_configurer.load_config(MockContext('function-arn-name', 'function-version'))
        aws_lambda_mock.get_function_configuration.assert_called_once_with(FunctionName='function-arn-name',
                                                                           Qualifier='function-version')
        self.assertEquals(config, {
            'endpoint': 'knuff.eu-west-1.es.amazonaws.com'
        })

    @patch('aws_lambda_configurer.aws_lambda')
    @patch('aws_lambda_configurer.s3_client')
    def test_lookup_s3(self, s3_mock, aws_lambda_mock):
        aws_lambda_mock.get_function_configuration.return_value = {
            'Description': json.dumps({
                "_lookup": {
                    "s3": {
                        "bucket": "mybucket",
                        "key": "my-key"
                    }
                },
                "abc": 123,
                "override": 1
            })
        }

        self.mock_s3_get(
            s3_mock,
            {
                "foo": "bar",
                "override": 2

            })

        config = aws_lambda_configurer.load_config(MockContext('function-arn-name', 'function-version'))
        self.assertEquals(config, {
            "abc": 123,
            "foo": "bar",
            "override": 2
        })
        s3_mock.get_object.assert_called_once_with(Bucket='mybucket', Key='my-key')

    def mock_s3_get(self, s3_mock, result):
        body_mock = MagicMock
        s3_mock.get_object.return_value = {
            'Body': body_mock
        }
        body_mock.read = MagicMock(return_value=json.dumps(result))

    @patch('aws_lambda_configurer.aws_lambda')
    def test_raise_json_error(self, aws_lambda_mock):
        aws_lambda_mock.get_function_configuration.return_value = {
            'Description': "i am not a json description"
        }

        with self.assertRaises(Exception) as cm:
            aws_lambda_configurer.load_config(MockContext('function-arn-name', 'function-version'))

        self.assertEqual('Description of function must contain JSON, but was "i am not a json description"',
                         cm.exception.message)

    @patch('aws_lambda_configurer.aws_lambda')
    def test_missing_description_error(self, aws_lambda_mock):
        aws_lambda_mock.get_function_configuration.return_value = {}

        with self.assertRaises(KeyError) as cm:
            aws_lambda_configurer.load_config(MockContext('function-arn-name', 'function-version'))

        self.assertEqual('Description', cm.exception.message)


class MockContext:
    def __init__(self, invoked_function_arn, function_version):
        self.invoked_function_arn = invoked_function_arn
        self.function_version = function_version
