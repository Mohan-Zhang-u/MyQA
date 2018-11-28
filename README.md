### (still under developing)
# MyQA

- This repo is a question and answering system based on unlabeled large corpus. 
- The model has twocomponents: Document Retriever and Answer Extractor. 
- Document Retriever using bigram hashing and TF-IDF matching to pick the mostrelevant articles regarding to the question.
- Answer Extractor using the Deep Bidirectional Transformers invited byGoogle AI Languageon Oct.2018, pretrained on Wikipedia for Language understanding and fine-tuned onSQuAD 2.0for reading comprehension, to locate the answer fromrelevant articles extracted by Document Retriever.
- BERT large uncased pretrained weights are used here (340m parameteres, 1.2g to load, requires more than 24G of GPU memory)