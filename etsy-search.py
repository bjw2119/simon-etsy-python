import requests
import json
import re

stores = ['StoriedVintage2', 'EmeraldCloudArt', 'AtlasProject', 'TheGypsyChixCompany', 'MenLau', 'WeMakeBooks', 'MulberryWhisper', 'Dwarvendom', 'CrafterHaven', 'BarryBeaux']
garbage = ('', '39', 'the', 'a', 'and', 'it', 'an', 'quot', 'is', 'in', 'http', 'com', 'www', 'to', 'for', 'of', 'this')

def make_results(data):

    listings = []
    masterTitle = []
    masterDescription = []
    
    for listing in data['results']:
        #listings.append({'title': listing['title'], 'description': listing['description']})
        masterDescription = transform_text(listing['description'], masterDescription)
        masterTitle = transform_text(listing['title'], masterTitle)
    
    masterDescription = purge_text(masterDescription)
    masterTitle = purge_text(masterTitle)
    
    
    return {'store': data['params']['shop_id'], 'topFive': top_five( masterTitle, masterDescription)}

def transform_text(text, master):
    return master+re.split('\W', text.lower())

def purge_text(text):
    return [word for word in text if not word in garbage]

def top_five(masterTitle, masterDescription):
    topFive = {}
    fifth = ""
    storeDict = {}
    
    
    for i in range(max(len(masterDescription), len(masterTitle))):
 
        if i< len(masterTitle):
            if masterTitle[i] not in storeDict:
                storeDict[masterTitle[i]] = 1
            else:
                storeDict[masterTitle[i]] += 1
                
            if fifth not in topFive or topFive[fifth] < storeDict[masterTitle[i]]:
                topFive[masterTitle[i]] = storeDict[masterTitle[i]]
            
                if len(topFive) > 5: 
                    del topFive[min(topFive, key=topFive.get)]
                    fifth = min(topFive, key=topFive.get)   
    
        if i< len(masterDescription):
            if masterDescription[i] not in storeDict:
                storeDict[masterDescription[i]] = 1
            else:
                storeDict[masterDescription[i]] += 1
                
            if fifth not in topFive or topFive[fifth] < storeDict[masterDescription[i]]:
                topFive[masterDescription[i]] = storeDict[masterDescription[i]]
            
                if len(topFive) > 5: 
                    del topFive[min(topFive, key=topFive.get)]
                    fifth = min(topFive, key=topFive.get)            
        
        
    return topFive
    
for store in stores:
    r = requests.get('https://openapi.etsy.com/v2/shops/'+store+'/listings/active?api_key=h2e7qbewfwmq0cmh2lefa5kg')
    results = make_results(r.json())
    results['t5list'] = [(k, results['topFive'][k]) for k in sorted(results['topFive'], key=results['topFive'].get, reverse=True)]
    print(results['store']+": ")
    print(results['t5list'])



