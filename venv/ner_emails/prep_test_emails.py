import string
import pathlib
import pandas as pd
import os
import random
import datetime
import time
import json
import re

test_data_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\test_data"
emails_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\ner_raw\emails\emails.csv"
placeholders = ["<ClientName>", "<DocNumber>"]

def gen_doc_nr():
    rnd_switch = random.randint(1,10)
    if rnd_switch > 2:
        doc_no = ''.join(random.choice(string.digits) for _ in range(random.randint(7, 12)))
    else:
        doc_no = ''.join(random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 3)))
        doc_no += ''.join(random.choice(string.digits) for _ in range(random.randint(6, 10)))
    return doc_no

def get_random_values(email_txt):
    random_values = placeholders.copy()
    tmp_str = " ".join(email_txt.split())
    match_count = re.findall("<DocNumber>", tmp_str)
    en_list = []
    for ii in range(len(match_count)):
        st_pos = tmp_str.find("<DocNumber>")
        tmp_doc = gen_doc_nr()
        tmp_str = tmp_str.replace("<DocNumber>", tmp_doc, 1)
        en_tup = (st_pos, st_pos+len(tmp_doc), "<DocNumber>")
        en_list.append(en_tup)
    cl_name = ''.join(random.choice(string.ascii_uppercase))
    cl_name += ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(6, 16)))
    st_pos = tmp_str.find("<ClientName>")
    tmp_str = tmp_str.replace("<ClientName>", cl_name)
    en_tup = (st_pos, st_pos + len(cl_name), "<ClientName>")
    en_list.append(en_tup)
    return tmp_str, en_list


def main():
    mail_df = pd.read_csv(emails_path, header=None)
    training_data = []
    for ii in range(len(mail_df)):
        email_txt, ents = get_random_values(mail_df.iloc[ii][0])
        training_doc = (email_txt, {'entities':ents})
        training_data.append(training_doc)

        json_object = json.dumps(training_data, indent=4, ensure_ascii=False)
        with open(os.path.join(test_data_path, "training_emails.json"), "w", encoding="utf8") as outfile:
            outfile.write(json_object)

main()