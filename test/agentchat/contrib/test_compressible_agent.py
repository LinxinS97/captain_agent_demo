import pytest
import sys
import autogen
import os
from autogen.agentchat.contrib.compressible_agent import CompressibleAgent

here = os.path.abspath(os.path.dirname(__file__))
KEY_LOC = "notebook"
OAI_CONFIG_LIST = "OAI_CONFIG_LIST"


config_list = autogen.config_list_from_json(
    OAI_CONFIG_LIST,
    file_location=KEY_LOC,
    filter_dict={
        "model": ["gpt-4", "gpt4", "gpt-4-32k", "gpt-4-32k-0314"],
    },
)

try:
    import openai

    OPENAI_INSTALLED = True
except ImportError:
    OPENAI_INSTALLED = False


@pytest.mark.skipif(
    sys.platform in ["darwin", "win32"] or not OPENAI_INSTALLED,
    reason="do not run on MacOS or windows or dependency is not installed",
)
def test_compressible_agent():
    conversations = {}

    assistant = CompressibleAgent(
        name="assistant",
        llm_config={
            "request_timeout": 600,
            "seed": 43,
            "config_list": config_list,
        },
        compress_config={
            "mode": "COMPRESS",
            "trigger_count": 600,
            "verbose": True,
        },
    )

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
        or x.get("content", "").rstrip().endswith("TERMINATE."),
        code_execution_config={"work_dir": here},
    )

    user_proxy.initiate_chat(
        assistant,
        message="Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval notation.",
    )

    assistant.reset()
    print(conversations)


@pytest.mark.skipif(
    sys.platform in ["darwin", "win32"] or not OPENAI_INSTALLED,
    reason="do not run on MacOS or windows or dependency is not installed",
)
def test_compress_messsage():
    assistant = CompressibleAgent(
        name="assistant",
        llm_config={
            "request_timeout": 600,
            "seed": 43,
            "config_list": config_list,
        },
        compress_config={
            "mode": "COMPRESS",
            "trigger_count": 600,
            "verbose": True,
        },
    )

    assert assistant.compress_messages([{"content": "hello world", "role": "user"}]) == (
        False,
        None,
    ), "Single message should not be compressed"
    is_success, compressed = assistant.compress_messages(
        [
            {"content": "Hello!", "role": "user"},
            {"content": "How can I help you today?", "role": "assistant"},
            {"content": "Can you tell me a joke about programming?", "role": "assistant"},
        ]
    )
    assert is_success, "Compression should be successful"


if __name__ == "__main__":
    test_compress_messsage()
    test_compressible_agent()
