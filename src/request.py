import requests, nltk

def get_bigrams_and_vocabulary(article):
    if _preprocess(article) != '':
        entry = _get_content_for(article)
        entry = [w['extract'] for w in entry]
        entry = reduce(lambda l1, l2: l1 + l2, entry)
        entry = entry.encode('ascii', 'ignore')
        entry = entry.strip()
        tokens = nltk.wordpunct_tokenize(entry)
        return (nltk.bigrams(tokens), sorted(set(tokens)))
    return None

def _preprocess(x):
    if  ' ' in x:
        return x
    elif len([w for w in x if w.isupper()]) == 1:
        return x
    return "" 

def _get_content_for(x):
    """Credits goes to: 
        Author: Mark Amery
        See post for more details:
        http://stackoverflow.com/questions/4452102/how-to-get-plain-text-out-of-wikipedia.
        """
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

