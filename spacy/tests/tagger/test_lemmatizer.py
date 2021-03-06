# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import io
import pickle

from spacy.lemmatizer import Lemmatizer, read_index, read_exc
from spacy import util

import pytest


@pytest.fixture
def path():
    return util.match_best_version('en', None,
                os.environ.get('SPACY_DATA', util.get_data_path()))


@pytest.fixture
def lemmatizer(path):
    return Lemmatizer.load(path)


def test_read_index(path):
    with (path / 'wordnet' / 'index.noun').open() as file_:
        index = read_index(file_)
    assert 'man' in index
    assert 'plantes' not in index
    assert 'plant' in index


def test_read_exc(path):
    with (path / 'wordnet' / 'verb.exc').open() as file_:
        exc = read_exc(file_)
    assert exc['was'] == ('be',)


def test_noun_lemmas(lemmatizer):
    do = lemmatizer.noun

    assert do('aardwolves') == set(['aardwolf'])
    assert do('aardwolf') == set(['aardwolf'])
    assert do('planets') == set(['planet'])
    assert do('ring') == set(['ring'])
    assert do('axes') == set(['axis', 'axe', 'ax'])


def test_base_form_dive(lemmatizer):
    do = lemmatizer.noun
    assert do('dive', number='sing') == set(['dive'])
    assert do('dive', number='plur') == set(['diva'])


def test_base_form_saw(lemmatizer):
    do = lemmatizer.verb
    assert do('saw', verbform='past') == set(['see'])


def test_smart_quotes(lemmatizer):
    do = lemmatizer.punct
    assert do('“') == set(['"'])
    assert do('“') == set(['"'])


def test_pickle_lemmatizer(lemmatizer):
    file_ = io.BytesIO()
    pickle.dump(lemmatizer, file_)

    file_.seek(0)
    
    loaded = pickle.load(file_)
