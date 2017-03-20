import requests, nltk

def get_bigrams_and_vocabulary(_file):
    titles = _read_titles_from(_file)
    return _get_bigrams_and_vocabulary_forall(titles)

def _read_titles_from(_file):
    if not isinstance(_file, file):
        _file = open(_file, 'rU')

    titles = [_extract_title(line.strip()) for line in _file]
    return [title for title in titles if _preprocess(title) != '']

def _extract_title(title):
    return title[title.rfind(":") + 1:]

def _preprocess(x):
    if  ' ' in x:
        return x
    elif len([w for w in x if w.isupper()]) == 1:
        return x
    return "" 

def _get_bigrams_and_vocabulary_forall(articles):
    sample =  [_get_bigrams_and_vocabulary_for(article) for article in articles]
    return reduce(lambda t1, t2: (t1[0] + t2[0], t1[1] | t2[1]), sample)

def _get_bigrams_and_vocabulary_for(article):
    entry = _get_content_for(article)
    entry = [w['extract'] for w in entry]
    entry = reduce(lambda l1, l2: l1 + l2, entry)
    entry = entry.encode('ascii', 'ignore')
    entry = entry.strip()
    tokens = nltk.wordpunct_tokenize(entry)
    return ([l for l in nltk.bigrams(tokens)], set(tokens))

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

