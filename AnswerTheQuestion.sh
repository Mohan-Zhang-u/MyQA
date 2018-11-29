#!/usr/bin/env bash

# set source
export PATH="/anaconda/envs/py36QA/bin:$PATH"
# alias pip=/anaconda/envs/py36/bin/pip
alias anaconda-navigator=/anaconda/bin/anaconda-navigator
export CLASSPATH=$CLASSPATH:data/corenlp/*

#change to args!

mkdir -p MyRetrievedData/retrieved

# echo "Enter Your Questions:"
# read question
question="question answering"

python retriever/RetrieverProcess.py MyRetrievedData/myTFIDF/SearchBase.npz "$question" 5 MyRetrievedData/retrieved/retrieved.json
python retriever/Pipeline.py MyCorpus MyRetrievedData/retrieved/retrieved.json MyRetrievedData/retrieved/docToRead.json "$question"

