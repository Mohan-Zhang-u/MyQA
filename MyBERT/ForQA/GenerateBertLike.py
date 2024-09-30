import json
import codecs

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

def get_paragraph(filename):
    try:
        with codecs.open('Paragraphs/' + filename, 'r', encoding='utf8') as fp:
            paragraph = fp.read()
            paragraph = paragraph.replace('\r\n', '\n')
            paragraph = paragraph.replace('\n', '\n')
            paragraph = paragraph.replace('\'', '\\\'')
            paragraph = paragraph.replace('\"', '\\\"')
            return paragraph
    except* (FileNotFoundError, IOError) as e:
        print(f"Error reading file {filename}: {e}")
        return ""

def generate_multi_test_cases(list_of_paragraphs, list_of_questions, name_of_file):
    assert len(list_of_paragraphs) == len(list_of_questions)
    length_of_them = len(list_of_paragraphs)

    data = []
    version = "my_ver"

    jsondict = {}
    jsondict["data"] = data
    jsondict["version"] = version

    for j in range(length_of_them):
        new_paragraph = {}
        new_paragraph["context"] = list_of_paragraphs[j]
        new_paragraph["qas"] = [{"answers": [{"answer_start": -1, "text": ""}], "question": list_of_questions[j], "id": list_of_questions[j]}]
        data.append({"title": "", "paragraphs": [new_paragraph]})

    try:
        with open('Data/' + name_of_file + '.json', 'w', encoding='utf8') as fp:
            json.dump(jsondict, fp, ensure_ascii=False, indent=4)
    except* (FileNotFoundError, IOError) as e:
        print(f"Error writing file {name_of_file}.json: {e}")

if __name__ == "__main__":
    list_of_paragraphs = []
    list_of_questions = []
    list_of_paragraphs.append(get_paragraph("imperial_short.txt"))
    list_of_questions.append("Imperial's income is growing or decreasing?")
    list_of_paragraphs.append(get_paragraph("imperial_short.txt"))
    list_of_questions.append("How many barrels of petroleum product does Imperial sale each day during its highest quarterly sales?")
    list_of_paragraphs.append(get_paragraph("imperial_short.txt"))
    list_of_questions.append("How many barrels of Refinery throughput does Imperial sale per day during its highest quarterly sales?")

    generate_multi_test_cases(list_of_paragraphs, list_of_questions, "imperial_short")

    list_of_paragraphs = []
    list_of_questions = []
    list_of_paragraphs.append(get_paragraph("imperial_long.txt"))
    list_of_questions.append("How much is Bitumen realizations average barrel price for the second quarter of 2018?")
    list_of_paragraphs.append(get_paragraph("imperial_long.txt"))
    list_of_questions.append("How is the quarterly chemical net income?")
    list_of_paragraphs.append(get_paragraph("imperial_short.txt"))
    list_of_questions.append("Imperial's income is growing or decreasing?")

    generate_multi_test_cases(list_of_paragraphs, list_of_questions, "imperial_long")

    list_of_paragraphs = []
    list_of_questions = []
    list_of_paragraphs.append(get_paragraph("beeshort.txt"))
    list_of_questions.append("How do traditional beekeepers feel about GM bees?")

    generate_multi_test_cases(list_of_paragraphs, list_of_questions, "beeshort")

    list_of_paragraphs = []
    list_of_questions = []
    list_of_paragraphs.append(get_paragraph("bee.txt"))
    list_of_questions.append("What leads bees to abandon their hive?")
    list_of_paragraphs.append(get_paragraph("bee.txt"))
    list_of_questions.append("How do traditional beekeepers feel about GM bees?")
    list_of_paragraphs.append(get_paragraph("bee.txt"))
    list_of_questions.append("When will the bee's egg pop when injecting to it?")
    list_of_paragraphs.append(get_paragraph("bee.txt"))
    list_of_questions.append("What is already threatening crops worldwide?")
    list_of_paragraphs.append(get_paragraph("bee.txt"))
    list_of_questions.append("From when do people start to consuming honey?")

    generate_multi_test_cases(list_of_paragraphs, list_of_questions, "bee")
