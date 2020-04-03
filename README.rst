=====================================================
 A Python LSTM-based POS-tagger for Udmurt language
=====================================================

This module contains a utility for part-of-speech tagging of Udmurt text.
The tool based on LSTM neural network and takes a word order into account.

Installation
============

The tool could be installed with pip

::

    pip3 install udmurttagger
    
**Note:** the model for the utility must be downloaded separately. 
Due to limitations on the size of the project, I could not place it 
on a github or PiPy. After launching the program it will download 
and unpack the model. No action is necessary on your part. But you 
will need an Internet connection and about 150 megabytes of incoming 
traffic.


Usage example
==============

Tagging one sentence at a time

::

    >>> from udmurttagger import Tagger
    >>> t = Tagger()
    >>> sentence = "Сьӧд зарезе."
    >>> tagged_sentence = t.predict_pos(sentence)
    >>> print(tagged_sentence)
    [('сьӧд', 'N'), ('зарезе', 'N')]
    
Tagset
==============

Tagset based on `UDMURT CORPORA <http://udmurt.web-corpora.net/>`_ 

* ADJ — adjective
* ADJPRO — adjectival pronoun
* ADV — adverb
* ADVPRO — adverbial pronoun
* CNJ — conjunction
* IMIT — ideophone
* INTRJ — interjection
* N — noun
* NUM — numeral
* PARENTH — parenthetic word
* PART — particle
* PN — proper noun (subtype of nouns)
* POST — postposition
* PREDIC — predicative
* PRO — pronoun
* V — verb

See the `page <http://udmurt.web-corpora.net/index_en.html>`_ for the details.

Model
==============


This tool can be used for disambiguation of rule-based markup.

You can make your own wrap of the trained model.

Model's evaluation: loss: 0.2281 - acc: 0.9845 - val_loss: 0.2643 - val_acc: 0.9782.


Contacts
==============

You can contact the contriutor of the project via email:

`Boris Orekhov <http://nevmenandr.net/bo.php>`_ (nevmenandr)

@ gmail