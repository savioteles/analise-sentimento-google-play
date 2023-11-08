"""
### Data Scraping
Para fazer o scraping dos dados do Google Play Store, iremos utilizar a biblioteca [google-play-scraper](https://github.com/JoMingyu/google-play-scraper).

Google-Play-Scraper fornece APIs para facilmente obter dados do Google Play Store utilizando Python sem dependências externas.

"""
import os
import sys
from get_app_info import get_app_info
from get_reviews import get_reviews
from sentiment_conversion import to_sentiment
import functions_framework
from flask import Response


APPS_IDS = ['com.zzkko', 'com.shopee.br', 'com.mercadolibre', 'com.novapontocom.casasbahia',
            'com.luizalabs.mlapp', 'com.b2w.americanas', 'com.alibaba.aliexpresshd',
            'com.amazon.mShop.android.shopping', 'com.schibsted.bomnegocio.androidApp',
            'br.com.enjoei.app']
SIZE = 20

@functions_framework.http
def scrap_google_play(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(force=True)
    request_args = request.args

    if request_json and 'apps_ids' in request_json:
        apps_ids = request_json['apps_ids']
        size = request_json['size']
    elif request_args and 'apps_ids' in request_args:
        apps_ids = request_args['apps_ids']
        size = request_args['size']
    else:
        apps_ids = APPS_IDS
        size = SIZE

    print(f"request_json: {request_json}")

    app_infos_df = get_app_info(apps_ids)
    print(app_infos_df)

    app_reviews_df = get_reviews(apps_ids, size)
    return Response(app_reviews_df.to_json(orient="records"), mimetype='application/json')
