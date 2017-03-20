import requests, nltk

#TODO: Create appropriate input files for HMM,
#using transition prob and vocabulary.
def generate_transition_prob_from(_file):
    """The _file contains set of wikipedia articles which the transition
    probabilities is to be derived from.
    Returns a map having bigram (word1, word2) as key and as value the
    transition probability from word1 to word2."""
    bigrams, vocabulary = _get_bigrams_and_vocabulary(_file)
    source_dict = _calculate_sources_distribution_from(bigrams)
    transition_prob = _calculate_transition_prob_from(bigrams, source_dict)
    return transition_prob
    

def _calculate_sources_distribution_from(bigrams):
    tmp = {}
    for bigram in bigrams:
        source = bigram[0]
        if (tmp.has_key(source)):
            tmp[source] = tmp[source] + 1
        else:
            tmp[source] = 1

    return tmp

def _calculate_transition_prob_from(bigrams, source_dict):
    tuple_dict = nltk.FreqDist(bigrams)
    transition_prob = {} 
    for bigram in bigrams:
        prob = float(tuple_dict[bigram])/source_dict[bigram[0]]
        transition_prob[bigram] = prob 
    
    return transition_prob 


def _get_bigrams_and_vocabulary(_file):
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
    if len(sample) == 0:
        raise ValueError("The articles are empty")
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

def _print(x):
        for key in x:
            print "from {} to {} with likelihood {}".format(key[0], key[1], x[key])
