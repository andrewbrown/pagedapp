from collections import OrderedDict
from datetime import datetime
import dateutil.parser
import email.parser
import pickle
from poplib import POP3, POP3_SSL
from django.core.management.base import BaseCommand
from twilio.rest import TwilioRestClient
from twilio.twiml import Response
from paged.models import Message, Subscriber

PAGED_POP3_SSL = True
PAGED_POP3_HOST = 'mail.messagingengine.com'
PAGED_POP3_PORT = 995
PAGED_POP3_USERNAME = 'roughfalls@fastmail.fm'
PAGED_POP3_PASSWORD = 'g0d!Damn'

TWILIO_ACCOUNT_SID = 'AC0025eeba6ff0193ae8c9f683886c9499'
TWILIO_AUTH_TOKEN = '8b21aaf03c0aab322f42f01b146af4ab'
TWILIO_NUMBER = '+13213381577'

class Command(BaseCommand):
    help = 'Fetches new messages from a POP3 server'

    def send_sms(self, message):
        client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        for sub in Subscriber.objects.all():
            client.messages.create(
                body=message.message,
                to=sub.number,
                from_=TWILIO_NUMBER
            )

    def handle(self, *args, **options):

        if PAGED_POP3_SSL:
            pop = POP3_SSL(PAGED_POP3_HOST)
        else:
            pop = POP3(PAGED_POP3_HOST)
        pop.user(PAGED_POP3_USERNAME)
        pop.pass_(PAGED_POP3_PASSWORD)

        # # Get messages from server and concatenate
        # retrieved_messages = [pop.retr(i) for i in range(1, len(pop.list()[1]) + 1)]
        # retrieved_messages = ["\n".join(m[1]) for m in retrieved_messages]
        #
        # #Parse message into an email object:
        # retrieved_messages = [parser.Parser().parsestr(m) for m in retrieved_messages]

        Message.objects.filter(debug=True).delete()

        for i in range(1, len(pop.list()[1]) + 1):

            m_id = pop.uidl(i)

            # TODO : if Message with m_id does not already exist, save a copy of it:
            if True:
                # Get messages from server and concatenate
                m = pop.retr(i)
                m = "\n".join(m[1])

                # Parse message into an email object:
                m = email.parser.Parser().parsestr(m)

                if 'Date' in m:
                    m_date = dateutil.parser.parse(m['Date'])
                else:
                    m_date = datetime.utcnow()

                message = Message(
                    received_date=m_date,
                    sender=m['From'],
                    message=m.get_payload(),
                    post_serialized=pickle.dumps(m),
                    sent = False,
                    debug = True # TODO
                )
                message.save()

                # pop.dele(i)

        pop.quit()

        # Loop through all unsent messages and send to subscribers
        for m in Message.objects.filter(sent=False):
            self.send_sms(m)
            m.sent = True
            m.save()
            break
