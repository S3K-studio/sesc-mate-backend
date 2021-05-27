from json.decoder import JSONDecodeError
import logging
import json

logger = logging.getLogger('logdna')


def request_logger(process_request):
    def middleware(request):
        if request.path.startswith('/admin'):
            return process_request(request)
        meta = {
            'request': {
                'headers': {key: request.META[key] for key in request.META.keys() if
                            key[:4] == 'HTTP'},
                'path': request.path
            }
        }
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                meta['request']['body'] = json.loads(
                    request.body.decode('utf-8'))
            except Exception as e:
                meta['request']['body'] = {
                    'error': str(e)
                }
        elif request.method == 'GET':
            try:
                meta['request']['body'] = dict(request.GET)
            except Exception as e:
                meta['request']['body'] = {
                    'error': str(e)
                }
        if 'HTTP_X_VK_DATA' in meta['request']['headers'].keys():
            vk_headers = meta['request']['headers']['HTTP_X_VK_DATA']
            for item in vk_headers.split('&'):
                [key, value] = item.split('=')
                if key == 'vk_user_id' and value.isdigit():
                    user = int(value)
                    break
            else:
                user = 'Unauthorized user'
        else:
            user = 'Unauthorized user'
        meta['user'] = user
        logger.info(f'Received a request {request.path} from {user}.', {
            'meta': meta
        })
        return process_request(request)

    return middleware
