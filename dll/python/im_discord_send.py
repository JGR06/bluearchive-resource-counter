#https://discordpy.readthedocs.io/en/latest/api.html?highlight=webhook%20send#discord.Webhook.send

import imax
import requests
from discord import Webhook, RequestsWebhookAdapter
import discord
import os.path

def discord_send(url, name, text, photo_path):

#	imax.print('url: ', url)
#	imax.print('text: ', text)
#	imax.print('photo_path: ', photo_path)

	webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
#	if (photo_path == "") or (not os.path.isfile(photo_path)):
	if photo_path == "":
		webhook.send(text, username=name)
	else:
		if os.path.isfile(photo_path):
			webhook.send(text, username=name, file=discord.File(photo_path))
		else:
			imax.print('file does not exist: ', photo_path)
			webhook.send(text, username=name)
