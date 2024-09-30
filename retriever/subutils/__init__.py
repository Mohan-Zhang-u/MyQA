#!/usr/bin/env python3

import os
DATA_DIR = 'mydata'

DEFAULTS = {
    'db_path': os.path.join(DATA_DIR, 'wikipedia/docs.db'),
    'tfidf_path': os.path.join(
        DATA_DIR,
        'wikipedia/docs-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz'
    ),
}

def set_default(key, value):
    global DEFAULTS
    DEFAULTS[key] = value

def get_class(name):
    if name == 'tfidf':
        return TfidfDocRanker
    if name == 'sqlite':
        return DocDB
    # Enriching the exception with additional details using .add_note()
    error = RuntimeError(f'Invalid retriever class: {name}')
    error.add_note("Ensure that the class name is either 'tfidf' or 'sqlite'.")
    raise error

from .doc_db import DocDB
from .tfidf_doc_ranker import TfidfDocRanker
