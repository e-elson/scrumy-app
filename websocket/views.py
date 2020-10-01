from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatMessage, Connection
import boto3

# Create your views here.

@csrf_exempt
def test(request):
    return JsonResponse({'message': 'hello Daud'}, status=200)

def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)

@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.create(connection_id=connection_id)
    return JsonResponse({'message': 'connect successfully'}, status=200)

@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.get(connection_id=body['connectionId']).delete()
    return JsonResponse({'message': 'disconnect successfully'}, status=200)

@csrf_exempt
def _send_to_connection(connection_id, data):
     gatewayapi=boto3.client('apigatewaymanagementapi', endpoint_url='wss://kekley04pf.execute-api.us-east-2.amazonaws.com/test',
                              region_name='us-east-2', aws_access_key_id='AKIAW2YX5CZIFF52AG4K', aws_secret_access_key='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')
     return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))

@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    ChatMessage.objects.create(message=body["body"]["content"], username=body["body"]["username"], timestamp=body["body"]["timestamp"])
    data = {'messages': [body]}
    connections = Connection.objects.all()
    for connection in connections:
        _send_to_connection(str(connection), data)

@csrf_exempt
def get_messages(request):
    body = _parse_body(request.body)
    messages = [ obj.as_dict() for obj in ChatMessage.objects.all() ]
    data = {'messages': messages}
    _send_to_connection(body["connectionId"], data)
    return JsonResponse({'messages': data})

