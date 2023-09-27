from tqdm import tqdm
import pandas as pd
from google_play_scraper import app


def get_app_info(apps_ids):
    """Vamos realizar o scraping dados para cada app. Nesta etapa iremos obter informações gerais dos apps."""
    app_info = []

    for ap in tqdm(apps_ids):
        info = app(ap, lang='pt', country='br')
        del info['comments']
        app_info.append(info)

    return pd.DataFrame(app_info)
