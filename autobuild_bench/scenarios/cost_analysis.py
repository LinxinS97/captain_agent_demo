import sqlite3
import json
from pathlib import Path
import pandas as pd


COST_MAP = {
    "MATH": 5000,
    "DA-bench": 257,
    "HumanEval": 164,
    "GAIA": 53 + 86 + 26,
    "sci/Chemistry": 20,
    "sci/Physics": 20
}


def get_log(db_path="logs.db", table="chat_completions"):
    con = sqlite3.connect(db_path)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data


def str_to_dict(s):
    return json.loads(s)


def find_files(directory, file_name):
    path = Path(directory)
    return list(path.rglob(file_name))


if __name__ == "__main__":
    directory = './'
    file_name = 'logs.db'
    files = find_files(directory, file_name)

    for file in files:
        cost = 1
        for cost_idx in COST_MAP.keys():
            if cost_idx in str(file):
                cost = COST_MAP[cost_idx]
                break
        print(file)
        log_data = get_log(file)
        log_data_df = pd.DataFrame(log_data)

        log_data_df["total_tokens"] = log_data_df.apply(
            lambda row: str_to_dict(row["response"])["usage"]["total_tokens"], axis=1
        )
        log_data_df["request"] = log_data_df.apply(lambda row: str_to_dict(row["request"])["messages"][0]["content"], axis=1)
        log_data_df["response"] = log_data_df.apply(
            lambda row: str_to_dict(row["response"])["choices"][0]["message"]["content"], axis=1
        )

        # Sum totoal tokens for all sessions
        total_tokens = log_data_df["total_tokens"].sum()

        # Sum total cost for all sessions
        total_cost = log_data_df["cost"].sum()

        print(f"Total cost: {str(round(total_cost * cost, 4))}")