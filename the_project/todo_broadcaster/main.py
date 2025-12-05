import os
import logging
import apprise
import asyncio
import nats

NATS_URL = os.environ.get('NATS_URL', 
                          'nats://localhost:4222')
NATS_SUBJECT = "todo"
NATS_QUEUE = "todo-notifiers"
APPRISE_URL = os.environ.get('APPRISE_URL', '')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Broadcaster:
    def __init__(self):        
        self.nats_conn = None

        if APPRISE_URL != "":
            self.notifier = apprise.Apprise()
            self.notifier.add(APPRISE_URL)
            logger.info(f"Notifications to {APPRISE_URL:.32}... enabled.")
        else:
            logger.error("Environment variable APPRISE_URL not set, notification disable.")

    async def init_nats(self):
        logger.info(f"Connecting to NATS server at {NATS_URL}...")
        self.nats_conn = await nats.connect(NATS_URL)

    async def run(self):
        async def message_handler(msg):
            subject = msg.subject
            reply = msg.reply
            data = msg.data.decode()

            logger.debug("Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data))

            self.notifier.notify(body=data, title='A todo item changed')

        # Use a queue to allow multiple broadcaster instance
        # that send the notification only once
        await self.init_nats()
        await self.nats_conn.subscribe(NATS_SUBJECT, NATS_QUEUE, cb=message_handler)

bc = Broadcaster()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bc.run())
    try:
        loop.run_forever()
    finally:
        loop.close()
