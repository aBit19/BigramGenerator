import requests, nltk

def get_content_for(x):
    """Credits goes to: 
        http://stackoverflow.com/questions/4452102/how-to-get-plain-text-out-of-wikipedia.
        Author: Mark Amery"""
    response = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'query',
                'format': 'json',
                'titles': x,
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
            }
    ).json()
    return (iter(response['query']['pages'].values()))

def preprocess(x):
    if  ' ' in x:
        return x
    elif len([w for w in x if x.isupper]) > 1:
        return ''

def encode(x):
    return x.replace("\n", "").encode('ascii', 'ignored')


entry = get_content_for('Mathematics');
paragraph =  next(entry)['extract']


