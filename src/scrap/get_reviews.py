from google_play_scraper import Sort, reviews, app
from tqdm import tqdm
import pandas as pd


def get_reviews(apps_ids, count=2000):
    """#### Scraping reviews dos apps

    O objetivo é criar um dataset balanceado com o mesmo número de reviews para cada score (1-5). A análise de sentimento será realizada utilizando o seguinte critério:

    *   **Negativo**: scores 1 e 2
    *   **Neutro**: score 3
    *   **Positivo**: scores 4 e 5

    Para termos um dataset balanceado entre avaliações negativas, neutras e positivas, iremos selecionar uma amostra de 2000 avaliações com score 3 e 1000 com para os outros scores. Desta forma, teremos para cada app 2000 avaliações para cada um dos três (negativo, neutro e positivo).
    """
    app_reviews = []

    for ap in tqdm(apps_ids):
        for score in list(range(1, 6)):
            for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
                rvs, _ = reviews(
                    ap,
                    lang='pt',
                    country='br',
                    sort=sort_order,
                    count=count,
                    filter_score_with=score
                )
                for r in rvs:
                    r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
                    r['appId'] = ap
                app_reviews.extend(rvs)

    return pd.DataFrame(app_reviews)
