import json
from perfreporter.post_processor import PostProcessor
from time import sleep
from traceback import format_exc


def lambda_handler(event=None, context=None):
    try:
        sleep(10)
        galloper_url, project_id, bucket, prefix, config_file, junit, token = parse_event(event)
        post_processor = PostProcessor(config_file)
        post_processor.distributed_mode_post_processing(galloper_url, project_id, bucket, prefix, junit, token)
        return {
            'statusCode': 200,
            'body': json.dumps('Done')
        }
    except:
        return {
            'statusCode': 500,
            'body': format_exc()
        }


def parse_event(_event):

    # Galloper or AWS Lambda service
    event = _event if not _event.get('body') else json.loads(_event['body'])

    galloper_url = event.get('galloper_url')
    project_id = event.get('project_id')
    bucket = event.get('bucket')
    prefix = event.get('prefix')
    config_file = json.loads(event.get('config_file'))
    junit = event.get('junit', False)
    token = event.get('token')

    return galloper_url, project_id, bucket, prefix, config_file, junit, token
