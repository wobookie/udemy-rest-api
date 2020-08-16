from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


@api_view()
def healthcheck(request):
    dtime = datetime.now().isoformat(sep=' ', timespec='seconds')

    response = {
        'app_id': '01-01-01',
        'status': 'Ok',
        'datetime': dtime
    }

    return Response(response)
