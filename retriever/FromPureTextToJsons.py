''' this file converts a set of UTF-8 encoded documents with no repeated names to a json file like:

{"id": "doc1", "text": "text of doc1"}
...
{"id": "docN", "text": "text of docN"}
'''

import json
import codecs
import os
import argparse
from typing import TypeVar, LiteralString

# Define a variadic generic for functions that accept multiple types
Ts = TypeVar('Ts')

def create_json_file(datafile_path: LiteralString, json_path: LiteralString) -> None:
    for filename in os.listdir(datafile_path):
        file_path = os.path.join(datafile_path, filename)
        try:
            with codecs.open(file_path, 'r', encoding='utf8') as fp:
                text = fp.read()
                dictionary = {
                    'id': filename,
                    'text': text
                }
                json_file_path = os.path.join(json_path, filename)
                with codecs.open(json_file_path, 'w', encoding='utf8') as fpw:
                    json.dump(dictionary, fpw, ensure_ascii=False)
        except (FileNotFoundError, PermissionError) as e:
            e.add_note(f"Error processing file {filename}: {e}")
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile_path', type=str, help='/path/to/datefiles')
    parser.add_argument('json_path', type=str, help='/path/to/store/jsonfiles')
    args = parser.parse_args()
    create_json_file(args.datafile_path, args.json_path)
