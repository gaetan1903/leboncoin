from leboncoin_api_wrapper import Leboncoin
from db import database
import mysql.connector, time


db0 = mysql.connector.connect(**database())
cursor = db0.cursor()

for cat in ['Immobilier', 'Locations', 'Colocations', 'Bureaux & Commerces']:
    print(cat)
    lbc = Leboncoin()
    lbc.setCategory(cat)
    lbc.setLimit(4000)

    results = lbc.execute()
    ads = []
    print(len(results["ads"]))
    for ad in results["ads"]:
        pub_id = ad.get('list_id')
        categorie = ad.get('category_name')
        type_ad = ad.get('ad_type')
        date_maj = ad.get('index_date')
        url = ad.get('url')
        titre = ad.get('subject')
        surface = ad['attributes'][2].get('value')
        prix = ad['price'][0]
        description = ad.get('body')
        loc = ad['location']
        localisation = f"{loc.get('city')} - {loc.get('region_name')} - {loc.get('department_name')} - {loc.get('zip_code')}"
        status = ad.get('status')
        propretaire = ad['owner'].get('name')
        images = str(ad['images'].get('urls'))
        
        ads.append(
            (
                pub_id, categorie, type_ad, date_maj, url, titre, surface, prix, 
                localisation, description, images, propretaire, status
            )
        )

    sql = 'INSERT IGNORE Leboncoin VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(sql, ads)
    db0.commit()
    time.sleep(15)
db0.close()
