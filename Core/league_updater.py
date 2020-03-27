from discord_webhook import DiscordWebhook
from riotwatcher import LolWatcher, ApiError
import os


class WebhookHandler(object):
    def __init__(self):
        self.webhook_url = os.getenv("discord_webhook_url")

    def send_message(self, **kwargs):
        username = kwargs.get("username", "")
        content = kwargs.get("content", "")

        webhook = DiscordWebhook(url=self.webhook_url,
                                 username=username,
                                 content=content
                                 )
        response = webhook.execute()
        return response.content


class SummonerUpdater(object):
    def __init__(self):
        self.riot_api_code = os.getenv("riot_api_code")
        self.watcher = LolWatcher(self.riot_api_code)

    def update_summoner(self, summoner_name, region):
        summoner = self.watcher.summoner.by_name(region, summoner_name)
        print(summoner.keys())
        matches = self.watcher.match.matchlist_by_account(region, summoner["accountId"], begin_index=0, end_index=5)
        print(matches)



if __name__ == "__main__":
    upd = SummonerUpdater()
    print("Made SummonerUpdater class")
    upd.update_summoner("KongSnooze", "EUW1")