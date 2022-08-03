import json
from perfreporter.post_processor import PostProcessor


def lambda_handler(event=None, context=None):
    try:
        galloper_url, project_id, bucket, prefix, config_file, token,\
        integration, report_id, influx_host, influx_user, influx_password = parse_event(event)
        post_processor = PostProcessor(config_file)
        post_processor.distributed_mode_post_processing(galloper_url, project_id, bucket, prefix, token,
                                                        integration, report_id, influx_host,
                                                        influx_user, influx_password)

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }


def parse_event(_event):
    # Galloper or AWS Lambda service
    event = _event if not _event.get('body') else json.loads(_event['body'])

    galloper_url = event.get('galloper_url')
    project_id = event.get('project_id')
    bucket = event.get('bucket')
    prefix = event.get('prefix')
    config_file = json.loads(event.get('config_file'))
    integration = event.get('integration', {})
    token = event.get('token')
    report_id = event.get('report_id')
    influx_host = event.get('influx_host')
    influx_user = event.get('influx_user')
    influx_password = event.get('influx_password')

    return galloper_url, project_id, bucket, prefix, config_file, token, integration, report_id, influx_host, \
           influx_user, influx_password
