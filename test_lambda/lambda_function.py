# -*- coding: utf-8 -*-
import os
import time
import datetime
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logs = boto3.client('logs')

# environment variable
LOGS_GROUP_NAME = os.environ['LOGS_GROUP_NAME']
LOGS_STREAM_NAME = os.environ['LOGS_STREAM_NAME']


def put_log_events(message):

    # events format
    events = [
        dict([('timestamp', int(time.time())*1000), ('message', message)])
    ]

    response = logs.describe_log_streams(
        logGroupName=LOGS_GROUP_NAME,
        logStreamNamePrefix=LOGS_STREAM_NAME)

    logger.info('describe_log_streams: {}'.format(response))

    stream = response['logStreams'][0]
    sequence_token = stream.get('uploadSequenceToken')

    if sequence_token:
        logs.put_log_events(
            logGroupName=LOGS_GROUP_NAME,
            logStreamName=LOGS_STREAM_NAME,
            logEvents=events,
            sequenceToken=sequence_token
        )
    else:
        logs.put_log_events(
            logGroupName=LOGS_GROUP_NAME,
            logStreamName=LOGS_STREAM_NAME,
            logEvents=events
        )
    logger.info('logs.put_log_event: {}'.format(events))


def lambda_handler(event, context):
    logger.info('event: {}'.format(event))

    try:
        for _ in range(100):
            # message = '2020-02-07T00:00:00.123456 Error foo bar'
            message = '{}, Error, {}, message'.format(
                datetime.datetime.now().strftime("%Y/%m/%dT%H:%M:%S"),
                'App1')
            put_log_events(message)
            time.sleep(1/2)

    except Exception as e:
        logger.error(e)
        raise e
