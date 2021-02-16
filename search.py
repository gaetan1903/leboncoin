from leboncoin_api_wrapper import Leboncoin

lbc = Leboncoin()
lbc.setCategory('Immobilier')
lbc.setLimit(10)

results = lbc.execute()

for ad in results["ads"]:
    """
        first_publication_date', 'index_date', 'status', 
        'category_id', 'category_name', 'subject', 'body', 
        'ad_type', 'url', 'price', 'price_calendar', 'images', 
        'attributes', 'location', 'owner', 'options', 'has_phone']
    """
    # ad est un dictionnaire contenant les clé ci-dessus, en choisir pour l'info voulu :) 
    print("\n")