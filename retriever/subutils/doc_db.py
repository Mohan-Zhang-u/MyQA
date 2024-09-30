#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Documents, in a sqlite database."""

import sqlite3
from . import utils
from . import DEFAULTS
from typing import TypeVar, Generic, List, Optional, Self
from typing_extensions import LiteralString

T = TypeVar('T')

class DocDB(Generic[T]):
    """Sqlite backed document storage.

    Implements get_doc_text(doc_id).
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.path = db_path or DEFAULTS['db_path']
        self.connection = sqlite3.connect(self.path, check_same_thread=False)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def path(self) -> str:
        """Return the path to the file that backs this database."""
        return self.path

    def close(self) -> None:
        """Close the connection to the database."""
        self.connection.close()

    def get_doc_ids(self) -> List[str]:
        """Fetch all ids of docs stored in the db."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM documents")
            results = [r[0] for r in cursor.fetchall()]
        finally:
            cursor.close()
        return results

    def get_doc_text(self, doc_id: LiteralString) -> Optional[str]:
        """Fetch the raw text of the doc for 'doc_id'."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT text FROM documents WHERE id = ?",
                (utils.normalize(doc_id),)
            )
            result = cursor.fetchone()
        except sqlite3.DatabaseError as db_error:
            # Handle database-related exceptions
            db_error.add_note(f"Failed to fetch document text for doc_id: {doc_id}")
            print(f"Database error occurred: {db_error}")
            result = None
        except Exception as other_error:
            # Handle other exceptions
            other_error.add_note(f"An unexpected error occurred while fetching document text for doc_id: {doc_id}")
            print(f"An error occurred: {other_error}")
            result = None
        finally:
            cursor.close()
        return result if result is None else result[0]
