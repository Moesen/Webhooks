from discord_webhook import DiscordWebhook
from random import randint
from secret import Info

def send_message(**kwargs):
    username = kwargs.get("username", "RehoboamBot")
    content = kwargs.get("content", f"Bip Bop  {randint(1,100000)}")

    webhook = DiscordWebhook(url=Info.webhook_url,
                             username=username,
                             content=content
                             )
    response = webhook.execute()
    print(response)
