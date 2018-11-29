#!/usr/bin/env bash

# set source
export PATH="/anaconda/envs/py36QA/bin:$PATH"
# alias pip=/anaconda/envs/py36/bin/pip
alias anaconda-navigator=/anaconda/bin/anaconda-navigator
export CLASSPATH=$CLASSPATH:data/corenlp/*

# temp, export DIR=

# prepare corpus to do QA. Here we prepared a search source.
mkdir -p MyRetrievedData
mkdir -p MyRetrievedData/tmp
mkdir -p MyRetrievedData/tmp/MyCorpusJson
mkdir -p MyRetrievedData/tmp/MyCorpusDataBase
mkdir -p MyRetrievedData/myTFIDF
python retriever/FromPureTextToJsons.py MyCorpus MyRetrievedData/tmp/MyCorpusJson
python retriever/build_db.py MyRetrievedData/tmp/MyCorpusJson MyRetrievedData/tmp/MyCorpusDataBase/db.db
python retriever/build_tfidf.py MyRetrievedData/tmp/MyCorpusDataBase/db.db MyRetrievedData/myTFIDF
# clean data
rm -rf MyRetrievedData/tmp




mkdir -p MyRetrievedData/retrieved
python retriever/RetrieverProcess.py MyRetrievedData/myTFIDF/db-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz "Neural Network" 5 MyRetrievedData/retrieved/retrieved.json



# python retriever/interactive.py --model mydata/10wikiTFIDF/db-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz
# Here, interactive can see how the retriever works!
