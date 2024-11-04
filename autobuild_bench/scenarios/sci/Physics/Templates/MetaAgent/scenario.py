import autogen
import testbed_utils
from autogen.agentchat.contrib.meta_agent import MetaAgent
from autogen.agentchat.contrib.meta_user_proxy_agent import MetaUserProxyAgent

testbed_utils.init()

PROBLEM = ""
with open("prompt.txt", "rt") as fh:
    PROBLEM = fh.read()

UNIT = ""
with open("unit.txt", "rt") as fh:
    UNIT = fh.read()

ANSWER = ""
with open("expected_answer.txt", "rt") as fh:
    ANSWER = fh.read()
config1 = '__CONFIG_LIST_PATH__'
config2 = '__CONFIG_LIST_PATH2__'

####################
# Task parameters
general_llm_config = {
    "temperature": 0,
    "config_list": autogen.config_list_from_json(config2, filter_dict={"tags": ["gpt-4", "0125", "1106", "claude3", "haiku", "llama3"]}),
}
nested_mode_config = {
    "autobuild_init_config": {
        "config_file_or_env": config1,
        "builder_model_tags": ['gpt-4', '1106', '0125', 'claude3', 'haiku', 'sonnet', 'gemini-1.5', 'llama3', '8b', '70b', 'mixtral', '8x22b', '8x7b'],
        "agent_model_tags": ['gpt-4', '1106', '0125', 'claude3', 'haiku', 'sonnet', 'gemini-1.5', 'llama3', '8b', '70b', 'mixtral', '8x22b', '8x7b'],
    },
    "autobuild_build_config": {
        "default_llm_config": {
            "temperature": 1,
            "top_p": 0.95,
            "max_tokens": 1500,
            "cache_seed": None,
        },
        "coding": True,
        "library_path_or_json": "/linxindisk/linxin/llm/autogen-autobuild-dev/autobuild_bench/scenarios/agent_library.json",
    },
    "autobuild_tool_config": {
        "tool_corpus": "/linxindisk/linxin/llm/autogen-autobuild-dev/tools/tool_description.tsv",
        "tool_root": "/linxindisk/linxin/llm/autogen-autobuild-dev/tools",
        "retriever": "all-mpnet-base-v2",
    },
    "group_chat_config": {"max_round": 15},
    "group_chat_llm_config": {
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 1500,
        "config_list": autogen.config_list_from_json(config2, filter_dict={"tags": ["gpt-4", "0125", "1106", "claude3", "haiku", "sonnet", 'llama3']}),
    },
}
## build agents
logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})

meta_agent = MetaAgent(name="meta_agent", llm_config=general_llm_config.copy(), nested_mode="autobuild")
meta_user_proxy = MetaUserProxyAgent(
    name="meta_user_proxy",
    nested_mode_config=nested_mode_config,
    code_execution_config={},
    agent_config_save_path="__AGENT_SAVE_PATH__"
)

## Run task
question = """Please solve the following physics problem: 
{problem}
Try to approximate by python instead of exact solutions for some problems that may be difficult to calculate. 
The following python packages are pre-installed: sympy numpy scipy
Do not plot or let the expert plot any figure.
The required unit of the answer is {unit}.
After verification, reply with the final answer in \\box{{}}."""
meta_user_proxy.initiate_chat(
    meta_agent,
    message=question.format(problem=PROBLEM, unit=UNIT)
)

## collect response
messages = []
key = list(meta_user_proxy.chat_messages.keys())[0]
chat_messages = meta_user_proxy.chat_messages[key]
for item in chat_messages:
    messages.append(item)
messages.reverse()

response_with_ans = "No answer."
for msg in messages:
    if (
        msg["content"] != "TERMINATE"
        and msg["content"] != "TERMINATE."
        and msg['role'] != 'assistant'
    ):
        response_with_ans = msg["content"]
        break

# ---------between "answer_checker" and "checker_proxy"---------
# define answer checker chat

check_sys_msg = """You are a helpful AI assistant. You will use your coding and language skills to verify the answer.
You are given:
    1. A problem (filled in [[...]]).
    2. A reply with the answer to the problem (filled in [[...]]).
    3. A ground truth answer (filled in [[...]]).
Please do the following:
1. Extract the answer in the reply: "The answer is <answer extracted>".
2. Check whether the answer in the reply matches the ground truth answer. When comparison is not obvious (for example, 3*\\sqrt(6) and 7.348), you may write code to check the answer and wait for the user to execute the code.
3. Your reply should be in the following options:
    - "The answer is correct."
    - "The answer is approximated but should be correct. Correct Answer: <ground truth answer> | Answer extracted: <answer extracted>."
    - "The answer is incorrect. Correct Answer: <ground truth answer> | Answer extracted: <answer extracted>."
    - "The reply doesn't contain an answer." """
checker_config_list = autogen.config_list_from_json(config2, filter_dict={"tags": ["gpt-4", "0125", "1106", "claude3", "haiku", 'llama3']})
checker_llm_config = testbed_utils.default_llm_config(checker_config_list, timeout=180)
answer_checker = autogen.AssistantAgent(
    name="checker",
    llm_config=checker_llm_config,
    system_message=check_sys_msg
)
checker_proxy = autogen.UserProxyAgent(
    "checker_proxy",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    max_consecutive_auto_reply=5,
    default_auto_reply="TERMINATE",
    is_termination_msg=lambda x: x.get("content", "").lower()
    and (
        "the answer is correct" in x.get("content", "").lower()
        or "the answer is incorrect" in x.get("content", "").lower()
        or "the reply doesn't contain an answer" in x.get("content", "").lower()
        or "the answer is approximated but should be correct" in x.get("content", "").lower()
    ),
)

message_to_check = f"Problem: [[{PROBLEM}]]\n\nReply: \n[[{response_with_ans}]]\n\nGround truth answer: \n[[{ANSWER}, unit: {UNIT}]]"
checker_proxy.initiate_chat(answer_checker, message=message_to_check)
autogen.runtime_logging.stop()

####################
testbed_utils.finalize(agents=[meta_agent, meta_user_proxy, answer_checker, checker_proxy])
