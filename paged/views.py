from datetime import datetime
import pickle
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import TwilioRestClient
from twilio.twiml import Response
from models import Message, Subscriber

TWILIO_ACCOUNT_SID = 'AC0025eeba6ff0193ae8c9f683886c9499'
TWILIO_AUTH_TOKEN = '8b21aaf03c0aab322f42f01b146af4ab'
TWILIO_NUMBER = '+13213381577'


@csrf_exempt
def receive(request):
    post = request.POST

    if post.get('AccountSid', '') != TWILIO_ACCOUNT_SID:
        return HttpResponseNotFound()

    message = Message(
        received_date=datetime.utcnow(),
        sender=post['From'],
        message=post['Body'],
        post_serialized=pickle.dumps(post)
    )
    message.save()

    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for sub in Subscriber.objects.all():
        client.messages.create(
            body=post['Body'],
            to=sub.number,
            from_=TWILIO_NUMBER
        )

    return HttpResponse(str(Response()))

def test_message(request):
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    client.messages.create(
        body="1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890LONGTEXT",
        to="+19192719601",
        from_=TWILIO_NUMBER
    )

    return HttpResponse(str(Response()))
