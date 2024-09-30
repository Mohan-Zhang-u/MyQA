#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
from typing import TypeVar, Callable, Any

DEFAULTS = {
    'corenlp_classpath': os.getenv('CLASSPATH')
}

T = TypeVar('T')

def set_default(key: str, value: Any) -> None:
    global DEFAULTS
    DEFAULTS[key] = value


from .corenlp_tokenizer import CoreNLPTokenizer
from .regexp_tokenizer import RegexpTokenizer
from .simple_tokenizer import SimpleTokenizer

# Spacy is optional
try:
    from .spacy_tokenizer import SpacyTokenizer
except ImportError:
    pass


def get_class(name: str) -> Callable[..., T]:
    if name == 'spacy':
        return SpacyTokenizer
    if name == 'corenlp':
        return CoreNLPTokenizer
    if name == 'regexp':
        return RegexpTokenizer
    if name == 'simple':
        return SimpleTokenizer

    error = RuntimeError(f'Invalid tokenizer: {name}')
    error.add_note("Ensure the tokenizer name is one of 'spacy', 'corenlp', 'regexp', or 'simple'.")
    raise error


def get_annotators_for_args(args: Any) -> set[str]:
    annotators = set()
    if args.use_pos:
        annotators.add('pos')
    if args.use_lemma:
        annotators.add('lemma')
    if args.use_ner:
        annotators.add('ner')
    return annotators


def get_annotators_for_model(model: Any) -> set[str]:
    return get_annotators_for_args(model.args)
