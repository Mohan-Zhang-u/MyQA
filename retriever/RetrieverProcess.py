import argparse
from subutils import tfidf_doc_ranker

def process(tfidf_model_path, question, k):
    ranker = tfidf_doc_ranker.TfidfDocRanker(tfidf_path=tfidf_model_path)
    doc_names, doc_scores = ranker.closest_docs(question, k)
    return doc_names, doc_scores

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tfidf_model_path', type=str, help='/path/to/tfidf_model.npz')
    parser.add_argument('question', type=str, help='the quetion to be answered')
    parser.add_argument('k', type=int, default=5, help='the maximum number of documents to be retrieved')
    args = parser.parse_args()
    process(args.tfidf_model_path, args.question, args.k)