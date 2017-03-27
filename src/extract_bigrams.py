#   1) open the file or just pass the name of count2w.txt
#       fi = open("count2w.txt", "r")
#   2) import math for the log10
#   3) and call write_vocabulary_and_transition_prob(fi, math.log10)
#   Results: Creates two files:
#       a)  vocabulary.txt
#       b)  bigram_counts 

def write_vocabulary_and_transition_prob(_file, f = lambda x: x):
    if not isinstance(_file, file):
        _file = open(_file)
    print("processing " + _file.name + "....")
    clean = [_preprocess(line) for line in _file]
    print("Done")
    print("Frequency of individual words is calculated ....")
    source_freq = _create_source_distr(clean)
    print("Done")
    print("Frequency of transitions is calculated ....")
    tuple_freq = _create_tuple_distr(clean)
    print("Done")
    print("Vocabulary is created ....")
    vocabulary = _get_vocab_from(clean)
    print("Done")
    print("Indexing words ...")
    word_to_index = _index_words(vocabulary)
    print("Done")
    print("Transition probabilities being calculated ...")
    trans_prob = _calculate_transition_prob(tuple_freq, source_freq, f)
    print("Done")
    print("Maps words to indexes....")
    trans_prob_indexed = _create_transition_prob_with_indexing(trans_prob, word_to_index)
    print("Done")
    fi_voc = open("vocabulary.txt", "w")
    print(fi_voc.name + " file has been created." )
    print("Writing vocabulary to " + fi_voc.name + "...") 
    for word in vocabulary:
        fi_voc.write(str(word[0]) + " " + word[1] + "\n")
    fi_voc.close()
    print("Done")
    fi_tr = open("bigram_count.txt", "w") 
    print(fi_tr.name + " file has been created." )
    print("Writing transition prob to " + fi_tr.name + "....") 
    for word in sorted(trans_prob_indexed):
        fi_tr.write(str(word[0]) + " " +str(word[1]) + " " + str(word[2]) + "\n")
    fi_tr.close()
    print("Done")


def _preprocess(s):
    a = s.replace("\t", " ").strip().split(" ")
    return (a[0], a[1], int(a[2]))

def _get_vocab_from(lines):
    a = []
    for line in lines:
        a.append(line[0])
        a.append(line[1])
    return [(x[0], x[1]) for x in enumerate(sorted(set(a)))]

def _create_tuple_distr(x):
    a = {}
    for line in x:
        a[(line[0], line[1])] = line[2]
    return a


def _create_source_distr(lines):
    a = {}
    for line in lines:
        key = line[0]
        value = line[2]
        if (a.has_key(line[0])):
            a[key] += value
        else:
            a[key] = value
    
    return a

def _calculate_transition_prob(tuple_distr, source_distr, l):
    transition_prob ={}
    for key in tuple_distr:
        prob = float(tuple_distr[key])/source_distr[key[0]]
        transition_prob[key] = l(prob)
    return transition_prob

def _index_words(vocabulary):
    a = {}
    for word in vocabulary:
        a[word[1]] = word[0]
    return a

def _create_transition_prob_with_indexing(tuple_trans_prob, word_to_index):
    tr = []
    for key in tuple_trans_prob:
       tr.append((word_to_index[key[0]], word_to_index[key[1]], tuple_trans_prob[key]))
    return tr;
