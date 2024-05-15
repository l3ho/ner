import json
import os
import random
from tqdm import tqdm
import spacy
from spacy.training import Example
from spacy.tokens import DocBin

test_data_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\test_data"

def convert(lang: str, TRAIN_DATA, output_path: str):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

def train_model():
    with open(os.path.join(test_data_path, "training_data.json"), encoding="utf-8") as f:
        test_data = json.loads(f.read())
    n_iterations = 100
    sp_model = spacy.blank('pl')
    if "ner" not in sp_model.pipe_names:
        ner = sp_model.add_pipe("ner", last=True)
    else:
        ner = sp_model.get_pipe("ner")

def create_test_data():
    with open(os.path.join(test_data_path, "training_emails.json"), encoding="utf-8") as f:
        test_data = json.loads(f.read())

    tr_data = test_data[:len(test_data)-10]
    ts_data = test_data[len(test_data)-10:]
    convert('en', tr_data, "train.spacy")
    convert('en', tr_data, "valid.spacy")

def main():
    with open(os.path.join(test_data_path, "valid_emails.json"), encoding="utf-8") as f:
        test_data = json.loads(f.read())
    ts_data = test_data[len(test_data) - 10:]

    tr_model = spacy.load("models/emails_output/model-best")
    for ts_doc in ts_data:
        txt = ts_doc[0]
        doc = tr_model(txt)
        print(txt)
        for ent in doc.ents:
            print(ent.text, ent.label_)

main()