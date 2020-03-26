from discord_webhook import DiscordWebhook
from secret import Info


class LeagueToDiscWebhook(object):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, **kwargs):
        pass
# webhook = DiscordWebhook(url=webhook_url,
#                          content="Hello",
#                          username="Gustav")
# response = webhook.execute()
#
# print(response)
