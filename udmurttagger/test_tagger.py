#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tagger import Tagger

class TestTagger(object):
    def test_sentence(self):
        t = Tagger()
        tagged_sentence = t.predict_pos('Сьӧд зарезе.')
        assert [('сьӧд', 'N'), ('зарезе', 'N')] == tagged_sentence
        


