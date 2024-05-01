#
# Run this file to download the human_eval dataset, and create a corresponding testbed scenario:
# (default: ../scenarios/human_eval_two_agents_gpt4.jsonl and ./scenarios/human_eval_two_agents_gpt35.jsonl)
#

import argparse
import requests
import tarfile
import json
import os
import re
from autogen.agentchat.contrib.agent_builder import AgentBuilder

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

SCENARIO_DIR = os.path.realpath(os.path.join(SCRIPT_DIR, os.path.pardir))
TEMPLATES_DIR = os.path.join(SCENARIO_DIR, "Templates")
TASKS_DIR = os.path.join(SCENARIO_DIR, "Tasks")
SAVE_DIR = os.path.join(SCENARIO_DIR, "Saved_agents")
DOWNLOADS_DIR = os.path.join(os.path.join(SCENARIO_DIR, os.path.pardir), "Downloads")


SELECTED_CHEM_PROBLEMS = [
    f"{DOWNLOADS_DIR}/r_chem.json",
]

def load_data():
    """Load SCI Chemistry data.
    Return a JSON dictionary of selected problems."""

    selected_problems = dict()
    for file in SELECTED_CHEM_PROBLEMS:
        problems = json.load(open(file))
        selected_problems[file] = problems

    return selected_problems


def create_jsonl(name, problems, template, agent_list = None, config_list="OAI_CONFIG_LIST"):
    """Creates a JSONL scenario file with a given name, dictionary of Chemistry problems, and template path."""

    # Create a task directory if it doesn't exist
    if not os.path.isdir(TASKS_DIR):
        os.mkdir(TASKS_DIR)

    # Create the jsonl file
    cnt = 0
    with open(os.path.join(TASKS_DIR, name + ".jsonl"), "wt") as fh:
        for item in problems.items():
            data = item[1]

            id_prefix = item[0].split('/')[-1].replace('.json', '')
            for quest in data:
                task_id = id_prefix + quest['problemid']
                print(f"Converting: {task_id}")

                record = {
                    "id": task_id,
                    "template": os.path.join(os.path.pardir, template),
                    "substitutions": {
                        "prompt.txt": {"__PROMPT__": quest["problem_text"]},
                        "expected_answer.txt": {"__ANSWER__": quest["answer_number"]},
                        "unit.txt": {"__UNIT__": quest['unit']},
                        "agent_list.txt": {"__AGENT_LIST__": json.dumps(agent_list)},
                        "scenario.py": {
                            "__AGENT_SAVE_PATH__": SAVE_DIR,
                            "__CONFIG_LIST_PATH__": config_list
                        }
                    },
                }

                fh.write(json.dumps(record).strip() + "\n")
                cnt += 1
                if cnt >= 20:
                    return


###############################################################################
def main(args):
    problems = load_data()

    building_task = """We need a group of experts to solve some scientific problems.
Those problems are in the fields of "Quantum Chemistry", "Physical Chemistry" and "Physical Chemistry, Quanta, Matter, and Change".
They need to solve the problem collaboratively and check each other's answer. Also, they can write python code themselves to help solving the task if needed.
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

    # build agents
    if os.path.exists(f"{SAVE_DIR}/autobuild.json"):
        agent_configs = json.load(open(f"{SAVE_DIR}/autobuild.json"))
    else:
        builder = AgentBuilder(config_file_or_env=args.config_list,
                            builder_model_tags=['gpt-4', '1106', '0125', 'claude3', 'haiku', 'sonnet'],
                            agent_model_tags=['gpt-4', '1106', '0125', 'claude3', 'haiku', 'sonnet'],
                            max_agents=10)
        _, agent_configs = builder.build(building_task, default_llm_config, coding=True)

        if not os.path.isdir(SAVE_DIR):
            os.mkdir(SAVE_DIR)

        builder.save(f"{SAVE_DIR}/autobuild.json")

    for t in templates.items():
        create_jsonl(f"sci_chem_{t[0]}", problems, t[1], agent_list=agent_configs, config_list=args.config_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-list", type=str, default="OAI_CONFIG_LIST")
    args = parser.parse_args()
    main(args)

