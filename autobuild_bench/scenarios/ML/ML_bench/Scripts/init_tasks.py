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

SELECTED_PROBLEMS = [
    "gnn_1",
    "gnn_2",
    "gnn_3",
    "text_7",
    "text_8",
    "text_9",
    "molecular_15",
    "molecular_16",
    "molecular_17",
    "image_22",
    "image_23",
    "image_24",
    "video_45",
    "video_46",
    "video_47",
    "time_series_60",
    "time_series_61",
    "time_series_62",
    "time_series_63"
]

def get_readme(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find("article").text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return False


def create_jsonl(name, dataset, template, agent_list=None, readme_cache=None):
    """Creates a JSONL scenario file with a given name, dictionary of MATH problems, and template path."""

    # Create a task directory if it doesn't exist
    if not os.path.isdir(TASKS_DIR):
        os.mkdir(TASKS_DIR)

    # Create the jsonl file
    with open(os.path.join(TASKS_DIR, name + ".jsonl"), "wt") as fh:
        for item in dataset:
            data = json.loads(item)

            domain = data['domain'].lower().replace(' ', '_').replace('-', '_')
            task_id = f"{domain}_{data['id']}"
            if task_id not in SELECTED_PROBLEMS:
                continue

            print(f"Converting: {task_id}")

            readme = readme_cache.get(task_id, None)
            if readme is None:
                readme = get_readme(data['readme'])
                readme_cache[task_id] = readme

            record = {
                "id": task_id,
                "template": os.path.join(os.path.pardir, template),
                "substitutions": {
                    "prompt.txt": {"__PROMPT__": data["instruction"]},
                    "readme.txt": {"__README__": readme},
                    "expected_answer.txt": {"__ANSWER__": json.dumps(data["arguments"])},
                    "agent_list.txt": {"__AGENT_LIST__": json.dumps(agent_list)},
                },
            }

            fh.write(json.dumps(record).strip() + "\n")


###############################################################################
def main():
    with open(f"{DOWNLOADS_DIR}/ML_Bench_quarter.jsonl") as f:
        dataset = f.readlines()

    building_task = """We need a group of machine learning developers to satisfied the user's instruction. 
Those problems are in the fields of GNN, text, molecular, image, multimodal, video, time-series, and attention usage.
These experts will be given a user's instruction and a readme file. 
Their goal is to write a python bash script to fulfill user's need, taking care of the arguments in the script to match the user's instruction.
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

    readme_cache = {}
    for t in templates.items():
        create_jsonl(f"ml_bench_{t[0]}",
                     dataset,
                     t[1],
                     agent_list=agent_configs,
                     readme_cache=readme_cache)


if __name__ == "__main__" and __package__ is None:
    main()
