from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.conf import settings

import redis

REDIS_INSTANCE = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    charset='utf-8',
    db=0)


@api_view()
def health_check(request):
    dtime = datetime.now().isoformat(sep=' ', timespec='seconds')

    try:
        REDIS_INSTANCE.set('datetime', dtime)
        dtime = REDIS_INSTANCE.get('datetime').decode('UTF-8')
        response = {
            'app_id': '01-01-01',
            'status': 'Ok',
            'datetime': dtime
        }
    except redis.ConnectionError as error:
        response = {
            'app_id': '01-01-01',
            'status': 'Error',
            'reason': str(error),
            'datetime': dtime
        }

    return Response(response)
