# -*- coding: utf-8 -*-
import os
import time
import datetime
import uuid
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logs = boto3.client('logs')

# environment variable
LOGS_GROUP_NAME = os.environ['LOGS_GROUP_NAME']
LOGS_STREAM_NAME = os.environ['LOGS_STREAM_NAME']


def create_stream():
    stream_name = LOGS_STREAM_NAME + \
                  '-' + \
                  time.strftime('%y-%m-%d-%H-%M-%S') + \
                  uuid.uuid4().hex
    logs.create_log_stream(logGroupName=LOGS_GROUP_NAME,
                           logStreamName=stream_name)
    return stream_name


def create_message_events():
    message = '{}, Error, {}, {}'.format(
        datetime.datetime.now().strftime("%Y/%m/%dT%H:%M:%S"),
        'App1',
        'Exception: ' + str(uuid.uuid4())
    )
    events = [
        dict([('timestamp', int(time.time()) * 1000),
              ('message', message)])
    ]
    return events


def put_log_events(stream_name):
    sequence_token = None
    for _ in range(10):
        events = create_message_events()
        if sequence_token:
            response = logs.put_log_events(
                logGroupName=LOGS_GROUP_NAME,
                logStreamName=stream_name,
                logEvents=events,
                sequenceToken=sequence_token
            )
        else:
            response = logs.put_log_events(
                logGroupName=LOGS_GROUP_NAME,
                logStreamName=stream_name,
                logEvents=events
            )
        sequence_token = response['nextSequenceToken']
        time.sleep(1 / 2)


def lambda_handler(event, context):
    logger.info('event: {}'.format(event))
    try:
        for _ in range(3):
            stream_name = create_stream()
            put_log_events(stream_name)
    except Exception as e:
        logger.error(e)
        raise e
