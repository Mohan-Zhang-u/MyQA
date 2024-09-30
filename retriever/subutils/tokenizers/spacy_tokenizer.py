#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Tokenizer that is backed by spaCy (spacy.io).

Requires spaCy package and the spaCy english model.
"""

import spacy
import copy
from .tokenizer import Tokens, Tokenizer
from typing import TypeVar, Generic, Set, Tuple, Any, List, LiteralString
from dataclasses import dataclass

# Define a variadic generic type variable
Ts = TypeVar('Ts')

@dataclass
class TokenData:
    text: str
    whitespace: str
    span: Tuple[int, int]
    tag: str
    lemma: str
    ent_type: str

class SpacyTokenizer(Tokenizer, Generic[Ts]):

    def __init__(self, **kwargs: Any) -> None:
        """
        Args:
            annotators: set that can include pos, lemma, and ner.
            model: spaCy model to use (either path, or keyword like 'en').
        """
        model: LiteralString = kwargs.get('model', 'en')
        self.annotators: Set[str] = copy.deepcopy(kwargs.get('annotators', set()))
        nlp_kwargs = {'disable': ['parser']}
        if not any([p in self.annotators for p in ['lemma', 'pos', 'ner']]):
            nlp_kwargs['disable'].append('tagger')
        if 'ner' not in self.annotators:
            nlp_kwargs['disable'].append('ner')
        self.nlp = spacy.load(model, **nlp_kwargs)

    def tokenize(self, text: str) -> Tokens:
        # We don't treat new lines as tokens.
        clean_text = text.replace('\n', ' ')
        try:
            tokens = self.nlp(clean_text)
        except Exception as e:
            e.add_note("Error occurred while tokenizing text with spaCy.")
            raise

        data: List[TokenData] = []
        for i in range(len(tokens)):
            # Get whitespace
            start_ws = tokens[i].idx
            if i + 1 < len(tokens):
                end_ws = tokens[i + 1].idx
            else:
                end_ws = tokens[i].idx + len(tokens[i].text)

            data.append(TokenData(
                text=tokens[i].text,
                whitespace=text[start_ws: end_ws],
                span=(tokens[i].idx, tokens[i].idx + len(tokens[i].text)),
                tag=tokens[i].tag_,
                lemma=tokens[i].lemma_,
                ent_type=tokens[i].ent_type_,
            ))

        # Set special option for non-entity tag: '' vs 'O' in spaCy
        return Tokens(data, self.annotators, opts={'non_ent': ''})

# Note: Python 3.11 introduces fine-grained error locations in tracebacks by default,
# so no additional changes are needed for this feature.
