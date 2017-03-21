import requests, nltk

#Let the client to write the internals, to the file he wants. 

def create_vocabulary_and_digram_files_from(_file):
    """Return (transition_probabilities, vocabulary) lists ready to be
    written in the file, with the correct format."""
    tranp, vocab = _generate_transition_prob_and_vocab_from(_file)
    word2idx = _get_word2idx_from(vocab)
    final_tranp = _get_tranp_to_be_written(tranp, word2idx)
    return ([_makeit(line) for line in final_tranp], [str(idx) +' '+ word for idx, word in enumerate(vocab)])

def _generate_transition_prob_and_vocab_from(_file):
    bigrams, vocabulary = _get_bigrams_and_vocabulary(_file)
    source_dict = _calculate_sources_distribution_from(bigrams)
    transition_prob = _calculate_transition_prob_from(bigrams, source_dict)
    return (transition_prob, sorted(vocabulary))
    
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

def _get_tranp_to_be_written(tranp, word2idx):
    to_write_dic = {}
    for bigram in tranp:
        to_write_dic[_get_indexes_for_bigram_elements(bigram, word2idx)] = tranp[bigram] 
    return sorted(to_write_dic.items())

def _get_word2idx_from(vocab):
    word2idx = {}
    for idx, word in enumerate(vocab):
        word2idx[word] = idx
    return word2idx

def _get_indexes_for_bigram_elements(bigram, word2idx):
    return (word2idx[bigram[0]], word2idx[bigram[1]])

def _makeit(item):
    return str(item[0][0]) + ' ' + str(item[0][1]) + ' ' + str(item[1]) 

