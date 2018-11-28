#!/usr/bin/env bash

# set source
export PATH="/anaconda/envs/py36QA/bin:$PATH"
# alias pip=/anaconda/envs/py36/bin/pip
alias anaconda-navigator=/anaconda/bin/anaconda-navigator
export CLASSPATH=$CLASSPATH:data/corenlp/*

# temp, export DIR=

rm mydata/10wikijson/*
rm mydata/10wikiDataBase/db.db
rm mydata/10wikiTFIDF/*


python retriever/FromPureTextToJsons.py mydata/10wiki1 mydata/10wikijson
python retriever/build_db.py mydata/10wikijson mydata/10wikiDataBase/db.db
python retriever/build_tfidf.py mydata/10wikiDataBase/db.db mydata/10wikiTFIDF
python retriever/RetrieverProcess.py mydata/10wikiTFIDF/db-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz "Neural Network" 5 mydata/retrieved.json



# python retriever/interactive.py --model mydata/10wikiTFIDF/db-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz
# Here, interactive can see how the retriever works!
