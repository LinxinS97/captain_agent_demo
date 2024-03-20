#
# Run this file to download the human_eval dataset, and create a corresponding testbed scenario:
# (default: ../scenarios/human_eval_two_agents_gpt4.jsonl and ./scenarios/human_eval_two_agents_gpt35.jsonl)
#

import json
import os
import re
import requests
from bs4 import BeautifulSoup
from autogen.agentchat.contrib.agent_builder import AgentBuilder


SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

SCENARIO_DIR = os.path.realpath(os.path.join(SCRIPT_DIR, os.path.pardir))
TEMPLATES_DIR = os.path.join(SCENARIO_DIR, "Templates")
TASKS_DIR = os.path.join(SCENARIO_DIR, "Tasks")
DOWNLOADS_DIR = os.path.join(SCENARIO_DIR, "Downloads")
SAVE_DIR = os.path.join(SCENARIO_DIR, "Saved_agents")


def get_readme(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find("article").text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return False

def create_jsonl(name, dataset, template, agent_list = None):
    """Creates a JSONL scenario file with a given name, dictionary of MATH problems, and template path."""

    # Create a task directory if it doesn't exist
    if not os.path.isdir(TASKS_DIR):
        os.mkdir(TASKS_DIR)

    # Create the jsonl file
    with open(os.path.join(TASKS_DIR, name + ".jsonl"), "wt") as fh:
        for item in dataset:
            data = json.loads(item)
            if data['prefix_code'] != "":
                continue

            domain = data['domain'].lower().replace(' ', '_').replace('-', '_')
            task_id = f"{domain}_{data['id']}"
            print(f"Converting: {task_id}")

            record = {
                "id": task_id,
                "template": os.path.join(os.path.pardir, template),
                "substitutions": {
                    "prompt.txt": {"__PROMPT__": data["instruction"]},
                    "readme.txt": {"__README__": get_readme(data['readme'])},
                    "expected_answer.txt": {"__ANSWER__": data["output"]},
                    "agent_list.txt": {"__AGENT_LIST__": json.dumps(agent_list)},
                },
            }

            fh.write(json.dumps(record).strip() + "\n")


###############################################################################
def main():
    # TODO: problems selection
    with open(f"{DOWNLOADS_DIR}/ML_Bench_quarter.jsonl") as f:
        dataset = f.readlines()

    building_task = """We need a group of machine learning developers to solve some machine learning problems. 
Those problems are in the fields of GNN, text, molecular, image, multimodal, video, time-series, and attention Usage.
They need to solve the problem collaboratively and check each other's answer.
"""

    # list all directories in the Templates directory
    # and populate a dictionary with the name and path
    templates = {}
    for entry in os.scandir(TEMPLATES_DIR):
        if entry.is_dir():
            templates[re.sub(r"\s", "", entry.name)] = entry.path

    default_llm_config = {
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 1024,
    }

    ## build agents
    builder = AgentBuilder(config_file_or_env='OAI_CONFIG_LIST',
                           builder_model='gpt-4-1106',
                           agent_model='gpt-4-1106',
                           max_agents=10)
    _, agent_configs = builder.build(building_task, default_llm_config, coding=False)
    builder.save(f"{SAVE_DIR}/autobuild.json")

    for t in templates.items():
        create_jsonl(f"ml_bench_{t[0]}", dataset, t[1], agent_list=agent_configs)

if __name__ == "__main__" and __package__ is None:
    main()
