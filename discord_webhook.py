import asyncio

from discord import Webhook, Embed, colour
from datetime import datetime
from aiohttp import ClientSession

import settings


def build_embed(offer: dict[str, str], title: str, color: colour) -> Embed:
    embed = Embed(title=title, color=color, timestamp=datetime.strptime(offer['createTime'], "%Y-%m-%dT%H:%M:%S.%fZ"))

    embed.add_field(name='SKU', value=offer['sku'], inline=False)
    embed.add_field(name='Price', value=str(offer['price']), inline=False)
    embed.add_field(name='Size', value=offer['europeanSize'], inline=False)
    embed.add_field(name='Listing price', value=str(offer['listingPrice']), inline=False)
    embed.add_field(name='Variant', value=str(offer['variantId']), inline=False)
    embed.add_field(name='Offer ID', value=offer['id'], inline=False)
    embed.set_footer(text='WTN Offer Sniper | github@xlorek')
    embed.set_thumbnail(url=offer['image'])

    return embed


def accepted_webhook(data: dict[str, str], additional_mess: str = ''):
    title = 'Offer accepted! - ' + data['name'] + additional_mess
    embed = build_embed(offer=data, title=title, color=0x00c703)

    asyncio.run(send_webhook(embed=embed))


def offer_webhook(data: dict[str, str]):
    title = 'New offer - ' + data['name']
    embed = build_embed(offer=data, title=title, color=0xbfbfbf)

    asyncio.run(send_webhook(embed=embed))


def failed_webhook(data: dict[str, str]):
    title = 'Failed to accept offer - ' + data['name']
    embed = build_embed(offer=data, title=title, color=0xff2b2b)

    asyncio.run(send_webhook(embed=embed))


def error_webhook(mess: str):
    embed = Embed(title=mess, color=0xff2b2b, timestamp=datetime.utcnow().strptime("%Y-%m-%dT%H:%M:%S.%fZ"))

    asyncio.run(send_webhook(embed=embed))


async def send_webhook(embed: Embed):
    try:
        async with ClientSession() as client:
            webhook = Webhook.from_url(url=settings.WEBHOOK_URL, session=client)
            await webhook.send(embed=embed)
    except Exception:
        pass
