import requests
import urllib.parse

import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = 'pk_b6325ccbf1ff4cad8d7ba10082b31cd1';
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"].upper()
        }
    except (KeyError, TypeError, ValueError):
        return None

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def lookInCloud(symbol):
    # API: IRQ4Zx1CVhAIYrC-O6JKhW74GWP_9AaMWvv8bGSScZrL
    authenticator = IAMAuthenticator('cpuKkVNrkO0AAyCxJ0U8Y0OQNxQtR_a16CT_kqHffwYL')
    discovery = DiscoveryV1(
        version='2020-11-26',
        authenticator=authenticator
    )

    
    #discovery.set_service_url('https://api.eu-gb.discovery.watson.cloud.ibm.com/instances/aa8947c6-0ecb-45d8-8335-15a09c1a77a9')
    #discovery.set_service_url('https://api.eu-gb.discovery.watson.cloud.ibm.com/instances/aa8947c6-0ecb-45d8-8335-15a09c1a77a9/v1/environments/system/collections/news-en/query?version=2020-11-26&aggregation=filter%28enriched_title.entities.type%3A%3ACompany%29.term%28enriched_title.entities.text%29.timeslice%28crawl_date%2C1day%29.term%28enriched_text.sentiment.document.label%29&filter=IBM&deduplicate=false&highlight=true&passages=true&passages.count=12&query=')
    #discovery.set_service_url('https://api.eu-gb.discovery.watson.cloud.ibm.com/instances/3e86f8dd-e512-446f-8c24-e887f47c1ab9/v1/environments/system/collections/news-en/query?version=2018-12-03&count=1&aggregation=filter%28enriched_title.entities.type%3A%3ACompany%29.term%28enriched_title.entities.text%29.timeslice%28crawl_date%2C1day%29.term%28enriched_text.sentiment.document.label%29&filter=IBM&deduplicate=false&highlight=true&passages=true&passages.count=12&query=')

    discovery.set_service_url('https://api.eu-gb.discovery.watson.cloud.ibm.com/instances/b9e8228a-afed-4556-97f0-80073219bd22/v1/environments/system/collections/news-en/query?version=2018-12-03&aggregation=filter%28enriched_title.entities.type%3A%3ACompany%29.term%28enriched_title.entities.text%29.timeslice%28crawl_date%2C1day%29.term%28enriched_text.sentiment.document.label%29&filter=IBM&deduplicate=false&highlight=true&passages=true&passages.count=12&query=')

    # We are going to access a system collection with English news
    # You could change the language to news-de or news-es...
    news_environment_id = 'system'
    collection_id = 'news-en'

    response = discovery.query(
        news_environment_id,
        collection_id,
        query=symbol,
        count=6,
        deduplicate=True).get_result()

    return response
