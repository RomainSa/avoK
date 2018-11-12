import bs4 as bs
import urllib.request

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# load French NET dataset
file = 'https://raw.githubusercontent.com/EuropeanaNewspapers/ner-corpora/master/enp_FR.bnf.bio/enp_FR.bnf.bio'
df = pd.read_csv(file, sep='\s', names=['TOKEN', 'ENTITY'], dtype={'TOKEN': str, 'ENTITY': str})

# load French names
names_url = 'https://fr.wikipedia.org/wiki/Liste_de_pr%C3%A9noms_fran%C3%A7ais_et_de_la_francophonie'
html = urllib.request.urlopen(names_url).read()
soup = bs.BeautifulSoup(html)
names = [e.text for e in soup.find_all('b')][2:]
titles = ['m.', 'mme', 'mlle', 'docteur']

# show it
print(' '.join(df.TOKEN.values))

# replace entities so that only 'O' and 'I-PER' are left
df['ENTITY'] = df['ENTITY'].replace('I-LOC', 'O').replace('I-ORG', 'O')
df['ENTITY'] = df['ENTITY'].replace('I-PER', 1).replace('O', 0)

# prepare data in list of sentences and list of entities
entities_flat = list(df['ENTITY'].values)
sentences, entities = [], []
s, e = [], []
for i, row in df.iterrows():
    s.append(row.TOKEN)
    e.append(row.ENTITY)
    if row.TOKEN == '.':
        sentences.append(s)
        entities.append(e)
        s, e = [], []
sentences.append(s)
entities.append(e)

# features extraction
features = []
for sentence in sentences:
    for i, word in enumerate(sentence):
        # previous and next words
        previous_word = sentence[i-1] if 0 <= i-1 < len(sentence) else 'BEG'
        next_word = sentence[i+1] if 0 <= i+1 < len(sentence) else 'END'

        # features
        word_index_in_sentence = i

        word_size = len(word)
        previous_word_size = len(previous_word) if previous_word != 'BEG' else -1
        next_word_size = len(next_word) if next_word != 'END' else -1

        is_lowercase = 1 if word.lower() == word else 0
        previous_is_lowercase = (1 if previous_word != 'BEG' else -1) if previous_word.lower() == previous_word else 0
        next_is_lowercase = (1 if next_word != 'END' else -1) if next_word.lower() == next_word else 0

        is_first_uppercase = 1 if len(word) > 0 and word[0].upper() == word[0] and word[1:].lower() == word[1:] else 0
        previous_is_first_uppercase = (1 if previous_word != 'BEG' else -1) if len(previous_word) > 0 and previous_word[0].upper() == previous_word[0] and previous_word[1:].lower() == previous_word[1:] else 0
        next_is_first_uppercase = (1 if next_word != 'END' else -1) if len(next_word) > 0 and next_word[0].upper() == next_word[0] and next_word[1:].lower() == next_word[1:] else 0

        is_uppercase = 1 if word.upper() == word else 0
        previous_is_uppercase = (1 if previous_word != 'BEG' else -1) if previous_word.upper() == previous_word else 0
        next_is_uppercase = (1 if next_word != 'END' else -1) if next_word.upper() == next_word else 0

        is_name = 1 if word in names else 0
        previous_is_name = 1 if previous_word in names else 0
        next_is_name = 1 if next_word in names else 0

        is_title = 1 if word in titles else 0
        previous_is_title = 1 if previous_word in titles else 0
        next_is_title = 1 if next_word in titles else 0

        features_ = [word_index_in_sentence, word_size, previous_word_size, next_word_size,
                     is_lowercase, previous_is_lowercase, next_is_lowercase,
                     is_first_uppercase, previous_is_first_uppercase, next_is_first_uppercase,
                     is_uppercase, previous_is_uppercase, next_is_uppercase,
                     is_name, previous_is_name, next_is_name,
                     is_title, previous_is_title, next_is_title]

        features.append(features_)

df['FEATURES'] = pd.Series(features)

# split data into training and test
np.random.seed(42)
training_size = 0.90
indexes = list(range(len(features)))
train_index = np.random.choice(indexes, size=int(len(indexes)*training_size), replace=False)
test_index = np.array([i for i in indexes if i not in train_index])
x_train, y_train = [features[i] for i in train_index], [entities_flat[i] for i in train_index]
x_test, y_test = [features[i] for i in test_index], [entities_flat[i] for i in test_index]

# train a RandomForestClassifier
for max_depth in [2, 3, 4, 5, 6, 7, 8]:
    model = RandomForestClassifier(max_depth=max_depth, class_weight='balanced', n_estimators=50)
    model.fit(x_train, y_train)
    print('--- Max depth: %s ---' % max_depth)
    print('Train AUC %.2f' % roc_auc_score(y_train, model.predict(x_train)))
    print('Test AUC %.2f' % roc_auc_score(y_test, model.predict(x_test)))

# add predictions to dataset
df['PREDICTIONS'] = model.predict(df['FEATURES'].values.tolist())
