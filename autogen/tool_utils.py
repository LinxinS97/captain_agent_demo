import json
import re
import torch
import transformers
import os
from tqdm import tqdm
from functools import partial
import requests


def standardize_category(category):
    save_category = category.replace(" ", "_").replace(",", "_").replace("/", "_")
    while " " in save_category or "," in save_category:
        save_category = save_category.replace(" ", "_").replace(",", "_")
    save_category = save_category.replace("__", "_")
    return save_category


def standardize(string):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9^_]")
    string = res.sub("_", string)
    string = re.sub(r"(_)\1+", "_", string).lower()
    while True:
        if len(string) == 0:
            return string
        if string[0] == "_":
            string = string[1:]
        else:
            break
    while True:
        if len(string) == 0:
            return string
        if string[-1] == "_":
            string = string[:-1]
        else:
            break
    if string[0].isdigit():
        string = "get_" + string
    return string


def change_name(name):
    change_list = ["from", "class", "return", "false", "true", "id", "and"]
    if name in change_list:
        name = "is_" + name
    return name


def process_retrieval_document(documents_df):
    ir_corpus = {}
    corpus2tool = {}
    for row in documents_df.itertuples():
        doc = json.loads(row.document_content)
        # if "template_response" not in doc:
        # continue
        ir_corpus[row.docid] = (
            (doc.get("category_name", "") or "")
            + ", "
            + (doc.get("tool_name", "") or "")
            + ", "
            + (doc.get("api_name", "") or "")
            + ", "
            + (doc.get("api_description", "") or "")
            + ", required_params: "
            + json.dumps(doc.get("required_parameters", ""))
            + ", optional_params: "
            + json.dumps(doc.get("optional_parameters", ""))
            + ", return_schema: "
            + json.dumps(doc.get("template_response", ""))
        )
        corpus2tool[
            (doc.get("category_name", "") or "")
            + ", "
            + (doc.get("tool_name", "") or "")
            + ", "
            + (doc.get("api_name", "") or "")
            + ", "
            + (doc.get("api_description", "") or "")
            + ", required_params: "
            + json.dumps(doc.get("required_parameters", ""))
            + ", optional_params: "
            + json.dumps(
                doc.get("optional_parameters", "")
            )  # ', return_schema: ' + json.dumps(doc.get('template_response', ''))] = doc['category_name'] + '\t' + doc['tool_name'] + '\t' + doc['api_name'] + '\t' + json.dumps(doc['template_response'])
            + ", return_schema: "
            + json.dumps(doc.get("template_response", ""))
        ] = (doc["category_name"] + "\t" + doc["tool_name"] + "\t" + doc["api_name"])
    return ir_corpus, corpus2tool


def reformat_api_json(api_json):
    description_max_length = 512
    template = {
        "name": "",
        "description": "",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "optional": [],
        },
        # "example_response:": api_json["example_response"]
    }

    map_type = {"NUMBER": "integer", "STRING": "string", "BOOLEAN": "boolean"}

    pure_api_name = change_name(standardize(api_json["api_name"]))
    template["name"] = f"{api_json['category_name']}.{standardize(api_json['tool_name'])}.{pure_api_name}"
    # templete["name"] = pure_api_name + f"_for_{standard_tool_name}"
    # templete["name"] = templete["name"][-64:]

    # template["description"] = f"This is the subfunction for tool \"{standard_tool_name}\", you can use this tool. "

    if api_json["api_description"].strip() != "":
        tuncated_description = (
            api_json["api_description"].strip().replace(api_json["api_name"], template["name"])[:description_max_length]
        )
        # template["description"] = template["description"] + f"The description of this function is: \"{tuncated_description}\""
        template["description"] = tuncated_description
    if "required_parameters" in api_json.keys() and len(api_json["required_parameters"]) > 0:
        for para in api_json["required_parameters"]:
            name = standardize(para["name"])
            name = change_name(name)
            if para["type"] in map_type:
                param_type = map_type[para["type"]]
            else:
                param_type = "string"
            prompt = {
                "type": param_type,
                "description": para["description"][:description_max_length],
            }

            default_value = para["default"]
            if len(str(default_value)) != 0:
                prompt = {
                    "type": param_type,
                    "description": para["description"][:description_max_length],
                    "example_value": default_value,
                }
            else:
                prompt = {"type": param_type, "description": para["description"][:description_max_length]}

            template["parameters"]["properties"][name] = prompt
            template["parameters"]["required"].append(name)
        for para in api_json["optional_parameters"]:
            name = standardize(para["name"])
            name = change_name(name)
            if para["type"] in map_type:
                param_type = map_type[para["type"]]
            else:
                param_type = "string"

            default_value = para["default"]
            if len(str(default_value)) != 0:
                prompt = {
                    "type": param_type,
                    "description": para["description"][:description_max_length],
                    "example_value": default_value,
                }
            else:
                prompt = {"type": param_type, "description": para["description"][:description_max_length]}

            template["parameters"]["properties"][name] = prompt
            template["parameters"]["optional"].append(name)

    return template, api_json["category_name"], pure_api_name


def get_white_list(tool_root_dir):
    # print(tool_root_dir)
    white_list_dir = os.path.join(tool_root_dir)
    white_list = {}
    for cate in tqdm(os.listdir(white_list_dir)):
        if not os.path.isdir(os.path.join(white_list_dir, cate)):
            continue
        for file in os.listdir(os.path.join(white_list_dir, cate)):
            if not file.endswith(".json"):
                continue
            standard_tool_name = file.split(".")[0]
            # print(standard_tool_name)
            with open(os.path.join(white_list_dir, cate, file)) as reader:
                js_data = json.load(reader)
            origin_tool_name = js_data["tool_name"]
            white_list[standardize(origin_tool_name)] = {
                "description": js_data["tool_description"],
                "standard_tool_name": standard_tool_name,
            }
    return white_list


def contain(candidate_list, white_list):
    output = []
    for cand in candidate_list:
        if cand not in white_list.keys():
            return False
        output.append(white_list[cand])
    return output


def build_tool_description(data_dict, tool_root="tools/toollib"):
    white_list = get_white_list(tool_root)
    origin_tool_names = [standardize(cont["tool_name"]) for cont in data_dict["api_list"]]
    tool_des = contain(origin_tool_names, white_list)
    tool_descriptions = [[cont["standard_tool_name"], cont["description"]] for cont in tool_des]
    return tool_descriptions


def call_api(name: str, api_input: str):
    names = name.split(".")
    if len(names) != 3:
        return "Invalid api_name."
    category, tool_name, name = names
    toolbench_key = os.environ["TOOLBENCH_KEY"]

    payload = {
        "category": category,
        "tool_name": tool_name,
        "api_name": name,
        "tool_input": api_input,
        "strip": "truncate",
        "toolbench_key": toolbench_key,
    }
    headers = {"toolbench_key": toolbench_key}
    response = requests.post("http://8.218.239.54:8080/rapidapi", json=payload, headers=headers, timeout=30)
    # print(response)
    if response.status_code != 200:
        return (
            json.dumps({"error": f"request invalid, data error. status_code={response.status_code}", "response": ""}),
            12,
        )
    try:
        response = response.json()
    except:
        print(response)
        return json.dumps({"error": "request invalid, data error", "response": ""})
    # response = response.json()
    return json.dumps(response)
