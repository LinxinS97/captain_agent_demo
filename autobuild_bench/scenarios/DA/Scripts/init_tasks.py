import os
import random
import json
import re
from autogen.agentchat.contrib.agent_builder import AgentBuilder

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

SCENARIO_DIR = os.path.realpath(os.path.join(SCRIPT_DIR, os.path.pardir))
TEMPLATES_DIR = os.path.join(SCENARIO_DIR, "Templates")
TASKS_DIR = os.path.join(SCENARIO_DIR, "Tasks")
DATA_DIR = os.path.join(SCENARIO_DIR, "data")
SAVE_DIR = os.path.join(SCENARIO_DIR, "Saved_agents")


def load_data():
    label_path = os.path.join(DATA_DIR, "da-dev-labels.jsonl")
    question_path = os.path.join(DATA_DIR, "da-dev-questions.jsonl")

    # Load label data
    label_data = []
    with open(label_path, "r") as label_file:
        for line in label_file:
            data = json.loads(line)
            label_data.append(data)

    # Load question data
    question_data = []
    with open(question_path, "r") as question_file:
        for line in question_file:
            data = json.loads(line)
            question_data.append(data)

    # Join data based on 'id' field
    joined_data = []
    for label, question in zip(label_data, question_data):
        assert label["id"] == question["id"]
        joined_data.append({**label, **question})

    return joined_data


def create_jsonl(name, problems, template, agent_list=None):
    if not os.path.isdir(TASKS_DIR):
        os.mkdir(TASKS_DIR)

    with open(os.path.join(TASKS_DIR, name + ".jsonl"), "wt") as fh:
        for problem in problems:
            answers = []
            for ans in problem["common_answers"]:
                answers.append(f"@{ans[0]}[{ans[1]}]")
            answer = ",".join(answers)

            record = {
                "id": str(problem["id"]),
                "template": os.path.join(os.path.pardir, template),
                "substitutions": {
                    "constraint.txt": {"__CONSTRAINT__": problem["constraints"]},
                    "file.txt": {"__FILE__": "../files/" + problem["file_name"]},
                    "expected_answer.txt": {"__ANSWER__": answer},
                    "format.txt": {"__FORMAT__": problem["format"]},
                    "question.txt": {"__QUESTION__": problem["question"]},
                    "agent_list.txt": {"__AGENT_LIST__": json.dumps(agent_list)},
                },
            }

            fh.write(json.dumps(record).strip() + "\n")


def main():
    problems = load_data()

    # randomly select 20 problems
    random.shuffle(problems)
    problems = problems[:20]

    # sort problems based on the 'id' field
    problems = sorted(problems, key=lambda x: x["id"])

    # build agents
    building_task = """We need a group of experts to solve some scientific problems.
Those problems are in the fields of "Quantum Chemistry", "Physical Chemistry" and "Physical Chemistry, Quanta, Matter, and Change".
They need to solve the problem collaboratively and check each other's answer. Also, they can write python code themselves to help solving the task if needed.
"""

    default_llm_config = {
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 1024,
    }
    if os.path.exists(f"{SAVE_DIR}/autobuild.json"):
        agent_configs = json.load(open(f"{SAVE_DIR}/autobuild.json"))
    else:
        builder = AgentBuilder(config_file_or_env='OAI_CONFIG_LIST',
                            builder_model='gpt-4-1106',
                            agent_model='gpt-4-1106',
                            max_agents=10)
        _, agent_configs = builder.build(building_task, default_llm_config, coding=True)

        if not os.path.isdir(SAVE_DIR):
            os.mkdir(SAVE_DIR)

        builder.save(f"{SAVE_DIR}/autobuild.json")

    templates = {}
    for entry in os.scandir(TEMPLATES_DIR):
        if entry.is_dir():
            templates[re.sub(r"\s", "", entry.name)] = entry.path

    for t in templates.items():
        create_jsonl(f"da_{t[0]}", problems, t[1], agent_configs)


if __name__ == "__main__":
    main()
