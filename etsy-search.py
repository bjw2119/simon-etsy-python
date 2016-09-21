import requests

def make_results(data):

    listings = []

    for listing in data.results:
        listings.append({'title': listing.title, 'description': listing.description, 'views': listing.views})
    return {'store': data.params.shop_id, 'listings': listings}

r = requests.get('https://openapi.etsy.com/v2/shops/StoriedVintage2/listings/active.js?sort_on=score&limit=5&api_key=h2e7qbewfwmq0cmh2lefa5kg')

print(r.)

#print(make_results(r.json()))