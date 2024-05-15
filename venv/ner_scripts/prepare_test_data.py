import string
import pathlib
import pandas as pd
import os
import random
import datetime
import time
import json

test_data_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\test_data"
templates_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\ner_raw\POLARIS_txt"
names_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\ner_raw\names.csv"
adr_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\ner_raw\addresses.csv"
law_firms_path = r"C:\Users\P77906820\PycharmProjects\ner\venv\ner_raw\law_firms.csv"

placeholders = ["<CUSTOMERS_NAME_1>", "<CUSTOMERS_PESEL_1>", "<CUSTOMERS_ADDRESS_1>", "<CUSTOMERS_NAME_2>",
                "<CUSTOMERS_PESEL_2>", "<CUSTOMERS_ADDRESS_2>","<CUSTOMERS_CREDIT_NO>", "<CUSTOMERS_CREDIT_DATE>",
                "<CUSTOMERS_ATTORNEY>", "<CUSTOMERS_LAW_FIRM_NAME>", "<CUSTOMERS_LAW_FIRM_ADDRESS>"]

def gen_random_date(st_date, end_date):
    st_date_dt = datetime.datetime.strptime(st_date, "%d/%m/%Y")
    end_date_dt = datetime.datetime.strptime(end_date, "%d/%m/%Y")
    dt_dif = end_date_dt-st_date_dt
    dt_s = int(dt_dif.total_seconds())
    new_dt_s = random.randint(1, dt_s)
    new_dt_delta = datetime.timedelta(seconds=new_dt_s)
    rnd_date = st_date_dt + new_dt_delta
    final_rnd_date = rnd_date.date()
    return str(final_rnd_date)

def get_random_values(names_df, adr_df, law_df):
    random_values = placeholders.copy()
    customer_at = names_df.iloc[random.randint(1, len(names_df)-1)][0]
    customer_law_name = law_df.iloc[random.randint(1, len(law_df)-1)][0]
    cust_law_adr = adr_df.iloc[random.randint(1, len(adr_df)-1)][0]
    credit_no = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(10,16)))
    credit_date = gen_random_date("01/01/2020", "01/05/2024")
    cust_name1 = names_df.iloc[random.randint(1, len(names_df)-1)][0]
    cust_name2 = names_df.iloc[random.randint(1, len(names_df)-1)][0]
    cust_pesel1 = str(names_df.iloc[random.randint(1, len(names_df)-1)][2])
    cust_pesel2 = str(names_df.iloc[random.randint(1, len(names_df)-1)][2])
    cust_adr_1 = adr_df.iloc[random.randint(1, len(adr_df)-1)][0]
    cust_adr_2 = adr_df.iloc[random.randint(1, len(adr_df)-1)][0]
    random_values = [cust_name1, cust_pesel1, cust_adr_1, cust_name2, cust_pesel2, cust_adr_2, credit_no, credit_date,
                     customer_at, customer_law_name, cust_law_adr]
    return random_values


def main():
    template_lst = os.listdir(templates_path)
    tmp_count = 50
    names_df = pd.read_csv(names_path)
    adr_df = pd.read_csv(adr_path)
    law_df = pd.read_csv(law_firms_path)
    training_data = []
    for template_file in template_lst:
        template_file_name = os.path.basename(template_file)
        template_file_name = template_file_name.replace(".txt", "")
        tmp_str = pathlib.Path(os.path.join(templates_path, template_file)).read_text(encoding='utf-8-sig')
        tmp_str = " ".join(tmp_str.split())
        cntr = 1
        for jj in range(tmp_count):
            en_list = []
            rep_str = tmp_str
            rnd_ar = get_random_values(names_df, adr_df, law_df)
            for ii in range(len(placeholders)):
                pl_pos = rep_str.find(placeholders[ii])
                if  pl_pos > 0:
                    rnd_ar[ii] = " ".join(rnd_ar[ii].split())
                    rep_str = rep_str.replace(placeholders[ii], rnd_ar[ii])
                    en_tup = (pl_pos, pl_pos+len(rnd_ar[ii]), placeholders[ii])
                    en_list.append(en_tup)
            new_file_name = template_file_name + " " + str(cntr) +".txt"
            full_path = os.path.join(test_data_path, new_file_name)
            #pathlib.Path(full_path).write_text(rep_str, encoding='utf-8-sig')
            cntr += 1
            training_doc = (rep_str, {'entities':en_list})
            training_data.append(training_doc)

        json_object = json.dumps(training_data, indent=4, ensure_ascii=False)
        with open(os.path.join(test_data_path, "training_data.json"), "w", encoding="utf8") as outfile:
            outfile.write(json_object)

main()