from discord_webhook import DiscordWebhook
from random import randint
import os

class WebhookHandler(object):
    def __init__(self):
        self.webhook_url = os.getenv("discord_webhook_url")
        if self.webhook_url is None:
            raise Exception("url not found")

    def send_message(self, **kwargs):
        username = kwargs.get("username", "RehoboamBot")
        content = kwargs.get("content", f"Bip Bop  {randint(1, 100000)}")

        webhook = DiscordWebhook(url=self.webhook_url,
                                 username=username,
                                 content=content
                                 )
        response = webhook.execute()
        print(response.content)
