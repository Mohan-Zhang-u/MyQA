import json
import codecs
import os
import argparse
from typing import List, Dict, Any, TypedDict, NotRequired, Self

# The structure looks like this:
# SQuAD:https://rajpurkar.github.io/SQuAD-explorer/
#

# file.json
# ├── "data"
# │   └── [i]
# │       ├── "paragraphs"
# │       │   └── [j]
# │       │       ├── "context": "paragraph text"
# │       │       └── "qas"
# │       │           └── [k]
# │       │               ├── "answers"
# │       │               │   └── [l]
# │       │               │       ├── "answer_start": N
# │       │               │       └── "text": "answer"
# │       │               ├── "id": "<uuid>"
# │       │               └── "question": "paragraph question?"
# │       └── "title": "document id"
# └── "version": 1.1


# data=[]
# version="my_ver"
#
# # now, things inside data: (multiple elements)
# title=""
# paragraphs=[]
#
# # now, things inside paragraphs: (multiple elements)
# context=""
# qas=[]
#
# # now, things inside qas: (multiple elements)
# answers=[]
# id=""
# question=""
#
# # now, things inside answers: (multiple elements)
# answer_start=-1
# text=""

class Answer(TypedDict):
    answer_start: int
    text: str

class QAS(TypedDict):
    answers: List[Answer]
    id: str
    question: str

class Paragraph(TypedDict):
    context: str
    qas: List[QAS]

class Data(TypedDict):
    title: str
    paragraphs: List[Paragraph]

class JSONDict(TypedDict):
    data: List[Data]
    version: str

def format_paragraph(paragraph: str) -> str:
    paragraph = paragraph.replace('\r\n', '\n')
    paragraph = paragraph.replace('\n', '\n')
    # paragraph.replace('\'', ' ')
    paragraph = paragraph.replace('\'', '\\\'')
    paragraph = paragraph.replace('\"', '\\\"')
    return paragraph


def generate_multi_test_cases(list_of_paragraphs: List[str], list_of_questions: List[str], document_reader_json_path: str) -> None:
    assert len(list_of_paragraphs) == len(list_of_questions)
    length_of_them = len(list_of_paragraphs)

    data: List[Data] = []
    version = "my_ver"

    jsondict: JSONDict = {}
    jsondict["data"] = data
    jsondict["version"] = version

    for j in range(length_of_them):
        new_paragraph: Paragraph = {}
        new_paragraph["context"] = list_of_paragraphs[j]
        new_paragraph["qas"] = [{"answers": [{"answer_start": -1, "text": ""}], "question": list_of_questions[j],
                                 "id": list_of_questions[j]}]
        data.append({"title": "", "paragraphs": [new_paragraph]})  # here we can have multiple paragraph in paragraphs

    with codecs.open(document_reader_json_path, 'w', encoding='utf-8') as fp:
        json.dump(jsondict, fp, ensure_ascii=False, indent=4)


def pipeline(corpus_path: str, retrieved_json_path: str, document_reader_json_path: str, question: str) -> None:
    document = ""
    doc_names: Dict[str, Any] = {}
    try:
        with codecs.open(retrieved_json_path, 'r', encoding='utf-8') as fpr:
            doc_names = json.load(fpr)
        doc_names = doc_names["doc_names"]
        for doc_name in doc_names:
            with codecs.open(os.path.join(corpus_path, doc_name), 'r', encoding='utf-8') as fprc:
                content = fprc.read()
                document += content
                document += os.linesep
                document += os.linesep
    except (FileNotFoundError, json.JSONDecodeError) as e:
        e.add_note(f"Error processing files: {e}")
        print(f"Error processing files: {e}")
        return

    document = format_paragraph(document)
    list_of_paragraphs = [document]
    list_of_questions = [question]
    generate_multi_test_cases(list_of_paragraphs, list_of_questions, document_reader_json_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus_path', type=str, help='/path/to/corpus')
    parser.add_argument('retrieved_json_path', type=str, help='/path/to/store/retrieved_json.json')
    parser.add_argument('document_reader_json_path', type=str, help='/path/to/file/to/be/read/by/document/reader.json')
    parser.add_argument('question', type=str, help='the question to be asked')
    args = parser.parse_args()
    pipeline(args.corpus_path, args.retrieved_json_path, args.document_reader_json_path, args.question)
