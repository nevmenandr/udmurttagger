#!/usr/bin/env python

import json
import os
from string import punctuation, digits
from keras.models import load_model
from keras.preprocessing import sequence
import numpy as np

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_URL = "https://linghub.ru/udmurt_pos_model.h5.zip"
MODEL_FILE = os.path.join(MODEL_DIR, "udmurt_pos_model.h5")
PUNCTUATION = punctuation + '«»—–…“”\\n\\t ' + digits

def download_model():
    """
    Download model as :py:const:`~udmurttagger.tagger.MODEL_DIR`.
    """

    import requests
    import tempfile

    print("Downloading model to {} from {}".format(MODEL_DIR, MODEL_URL))
    
    # You can make your own wrap for this model.

    if not os.path.isdir(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    tmp_fd, tmp_path = tempfile.mkstemp()
    try:
        r = requests.get(MODEL_URL, stream=True)
        with os.fdopen(tmp_fd, 'wb') as fd:
            for chunk in r.iter_content(64 * 1024):
                fd.write(chunk)
            fd.flush()

        if MODEL_URL.endswith('.zip'):
            import zipfile
            zip = zipfile.ZipFile(tmp_path)
            try:
                zip.extractall(MODEL_DIR)
            finally:
                zip.close()
        else:
            raise NotImplementedError("Could not download or unpack model from {}".format(MODEL_URL))
    finally:
        os.unlink(tmp_path)


def get_or_else(dictionary, key, default_value):
    try:
        return dictionary[key]
    except KeyError:
        return default_value


class Tagger(object):
    """
    Takes string as an input and gives 
    a list of tuples ("word", "POS-tag") as an output.
    """

    def __init__(self):
        if not os.path.isfile(MODEL_FILE):
            download_model()
        
        with open(os.path.join(BASE_DIR, 'index2tag.json')) as fj:
            self.index2tag = json.load(fj)
        self.tag2index = {v:k for k, v in self.index2tag.items()}
        
        with open(os.path.join(BASE_DIR, 'index2word.json')) as fj:
            self.index2word = json.load(fj)
        self.word2index = {v:k for k, v in self.index2word.items()}
        
        self.s_vocabsize = min(len(self.word2index), 50000) + 2
        self.t_vocabsize = len(self.tag2index)
        
        self.model = load_model(os.path.join(MODEL_DIR, 'udmurt_pos_model.h5'))
              
        
        
    def predict_pos(self, sentence):
        """
        This function takes one sentence as an input string and gives 
        a list of tuples ("word", "POS-tag") as an output.
        The sentence must be up to 40 words. Otherwise the size 
        would be fit to 40 tokens
        """
        
        words = sentence.strip(PUNCTUATION).lower().split()
        if len(words) > 40:
            words = words[:40]
        sent_words = [get_or_else(self.word2index, word, self.word2index["UNK"]) for word in words]
        sent_encoded = sequence.pad_sequences([sent_words], maxlen=40)
        res = self.model.predict(sent_encoded)
        res_indx = np.argmax(res, axis=2)
        pos_preds = [self.index2tag[str(x)].upper() for x in res_indx[0].tolist()]
        pos_preds = pos_preds[len(pos_preds)-len(words):]
        return [x for x in zip(words, pos_preds) if x[1] != "PAD"]
        
    def text_prc(self, text):
        """
        This function split text into sentences and returns 
        a list of sentences with tags.
        """
        
        import re
        
        patt = re.compile('([^А-ЯҘҢҪҮҺҒӘҠӨ][.?!] )|\n([А-ЯҘҢҪҮҺҒӘҠӨ])')
        
        sents = patt.sub(r'\1##&##\2', text)
        sents = sents.split('##&##')
        return [self.predict_pos(sent) for sent in sents]
