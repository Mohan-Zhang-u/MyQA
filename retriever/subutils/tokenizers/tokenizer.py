#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Base tokenizer/tokens classes and utilities."""

import copy
from typing import List, Tuple, Optional, Callable, Any, LiteralString
from dataclasses import dataclass, field

@dataclass
class Tokens:
    """A class to represent a list of tokenized text."""
    data: List[Tuple]
    annotators: set
    opts: Optional[dict] = field(default_factory=dict)

    TEXT: int = 0
    TEXT_WS: int = 1
    SPAN: int = 2
    POS: int = 3
    LEMMA: int = 4
    NER: int = 5

    def __len__(self) -> int:
        """The number of tokens."""
        return len(self.data)

    def slice(self, i: Optional[int] = None, j: Optional[int] = None) -> 'Tokens':
        """Return a view of the list of tokens from [i, j)."""
        new_tokens = copy.copy(self)
        new_tokens.data = self.data[i: j]
        return new_tokens

    def untokenize(self) -> str:
        """Returns the original text (with whitespace reinserted)."""
        return ''.join([t[self.TEXT_WS] for t in self.data]).strip()

    def words(self, uncased: bool = False) -> List[str]:
        """Returns a list of the text of each token

        Args:
            uncased: lower cases text
        """
        if uncased:
            return [t[self.TEXT].lower() for t in self.data]
        else:
            return [t[self.TEXT] for t in self.data]

    def offsets(self) -> List[Tuple[int, int]]:
        """Returns a list of [start, end) character offsets of each token."""
        return [t[self.SPAN] for t in self.data]

    def pos(self) -> Optional[List[str]]:
        """Returns a list of part-of-speech tags of each token.
        Returns None if this annotation was not included.
        """
        if 'pos' not in self.annotators:
            return None
        return [t[self.POS] for t in self.data]

    def lemmas(self) -> Optional[List[str]]:
        """Returns a list of the lemmatized text of each token.
        Returns None if this annotation was not included.
        """
        if 'lemma' not in self.annotators:
            return None
        return [t[self.LEMMA] for t in self.data]

    def entities(self) -> Optional[List[str]]:
        """Returns a list of named-entity-recognition tags of each token.
        Returns None if this annotation was not included.
        """
        if 'ner' not in self.annotators:
            return None
        return [t[self.NER] for t in self.data]

    def ngrams(self, n: int = 1, uncased: bool = False, filter_fn: Optional[Callable[[List[str]], bool]] = None, as_strings: bool = True) -> List[Any]:
        """Returns a list of all ngrams from length 1 to n.

        Args:
            n: upper limit of ngram length
            uncased: lower cases text
            filter_fn: user function that takes in an ngram list and returns
              True or False to keep or not keep the ngram
            as_string: return the ngram as a string vs list
        """
        def _skip(gram: List[str]) -> bool:
            if not filter_fn:
                return False
            return filter_fn(gram)

        words = self.words(uncased)
        ngrams = [(s, e + 1)
                  for s in range(len(words))
                  for e in range(s, min(s + n, len(words)))
                  if not _skip(words[s:e + 1])]

        # Concatenate into strings
        if as_strings:
            ngrams = ['{}'.format(' '.join(words[s:e])) for (s, e) in ngrams]

        return ngrams

    def entity_groups(self) -> Optional[List[Tuple[str, str]]]:
        """Group consecutive entity tokens with the same NER tag."""
        entities = self.entities()
        if not entities:
            return None
        non_ent = self.opts.get('non_ent', 'O')
        groups = []
        idx = 0
        while idx < len(entities):
            ner_tag = entities[idx]
            # Check for entity tag
            if ner_tag != non_ent:
                # Chomp the sequence
                start = idx
                while (idx < len(entities) and entities[idx] == ner_tag):
                    idx += 1
                groups.append((self.slice(start, idx).untokenize(), ner_tag))
            else:
                idx += 1
        return groups


class Tokenizer:
    """Base tokenizer class.
    Tokenizers implement tokenize, which should return a Tokens class.
    """
    def tokenize(self, text: LiteralString) -> Tokens:
        try:
            raise NotImplementedError("The 'tokenize' method must be implemented by subclasses.")
        except NotImplementedError as e:
            e.add_note("Ensure that the subclass implements the 'tokenize' method.")
            raise

    def shutdown(self) -> None:
        pass

    def __del__(self):
        self.shutdown()
