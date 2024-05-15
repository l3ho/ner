import json
import os
import random
from tqdm import tqdm
import spacy
from spacy.training import Example

test_data_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\test_data"


def train_model():
    with open(os.path.join(test_data_path, "training_emails.json"), encoding="utf-8") as f:
        test_data = json.loads(f.read())
    n_iterations = 100
    sp_model = spacy.blank('en')
    if "ner" not in sp_model.pipe_names:
        ner = sp_model.add_pipe("ner", last=True)
    else:
        ner = sp_model.get_pipe("ner")

    examples = []
    for text, annots in test_data:
        examples.append(Example.from_dict(sp_model.make_doc(text), annots))

    other_pipes = [pipe for pipe in sp_model.pipe_names if pipe != 'ner']
    with sp_model.disable_pipes(*other_pipes):
        optimizer = sp_model.begin_training()
        for it in range(n_iterations):
            random.shuffle(examples)
            losses = {}
            for batch in spacy.util.minibatch(examples, size=5):
                sp_model.update(batch, drop=0.5, sgd=optimizer, losses=losses)
            print(it, losses)

    for text, _ in test_data:
        doc = sp_model(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

train_model()
aaa = 1