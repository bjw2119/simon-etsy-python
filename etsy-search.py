import requests
import json
import re

stores = ['StoriedVintage2', 'EmeraldCloudArt', 'AtlasProject', 'TheGypsyChixCompany', 'MenLau', 'WeMakeBooks', 'MulberryWhisper', 'Dwarvendom', 'CrafterHaven', 'BarryBeaux']
garbage = ('', '39', 'the', 'a', 'and', 'it', 'an', 'quot', 'is', 'in', 'http', 'com', 'www', 'to', 'for', 'of', 'this')

def make_results(data):

    listings = []
    masterTitle = []
    masterDescription = []
    #Transform and aggregate listing titles and descriptions
    for listing in data['results']:
        masterDescription = transform_text(listing['description'], masterDescription)
        masterTitle = transform_text(listing['title'], masterTitle)
    
    masterDescription = purge_text(masterDescription)
    masterTitle = purge_text(masterTitle)
    
    
    return {'store': data['params']['shop_id'], 'topFive': top_five( masterTitle, masterDescription)}

def transform_text(text, master):
    #Split lowercased listing terms from text variable along non-word chars and add to master
    return master+re.split('\W', text.lower())

def purge_text(text):
    #Remove unwanted terms and artifacts from list of strings
    return [word for word in text if not word in garbage]

def top_five(masterTitle, masterDescription):
    #Takes two arguments of lists of strings and returns 5 most common terms
    topFive = {}
    fifth = ""
    storeDict = {}
    
    
    for i in range(max(len(masterDescription), len(masterTitle))):
	#Goes through each term, increments dictionary, and keeps track of top 5
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
    #goes through each store, hits Etsy API for listings
    r = requests.get('https://openapi.etsy.com/v2/shops/'+store+'/listings/active?api_key=h2e7qbewfwmq0cmh2lefa5kg')
    #Finds top 5 most common terms
    results = make_results(r.json())
    #Creates new list of sorted top 5 terms by frequency
    results['t5list'] = [(k, results['topFive'][k]) for k in sorted(results['topFive'], key=results['topFive'].get, reverse=True)]
    print(results['store']+": ")
    print(results['t5list'])



