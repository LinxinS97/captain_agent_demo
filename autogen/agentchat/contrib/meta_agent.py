from typing import Callable, Dict, Literal, Optional, Union
from autogen.agentchat.conversable_agent import ConversableAgent


class MetaAgent(ConversableAgent):
    """
    (In preview) Meta agent, designed to solve a task with an agent or a group of agents.
    """

    META_PROMPTING_TOOL = {
        "type": "function",
        "function": {
            "name": "meta_prompting",
            "description": "Solve a task by querying an expert. Provide the expert identity and the task that needs to be solved, and the function will return the response of the expert.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "[REQUIRED] The task that needs to be solved by the expert.",
                    },
                    "expert_name": {
                        "type": "string",
                        "description": "[REQUIRED] Name of the expert. Should follow the format: Expert xxx.",
                    },
                    "expert_identity": {
                        "type": "string",
                        "description": "[REQUIRED] A high-quality description about the most capable and suitable expert to answer the instruction. In second person perspective. For example, You are a linguist, well-versed in the study of language and its structures. You are equipped with a good understanding of grammar rules and can differentiate between nouns, verbs, adjectives, adverbs, etc. You can quickly and accurately identify the parts of speech in a sentence and explain the role of each word in the sentence. Your expertise in language and grammar is highly valuable in analyzing and understanding the nuances of communication.",
                    },
                },
            },
        },
    }

    AUTOBUILD_QUERY_TOOL = {
        "type": "function",
        "function": {
            "name": "autobuild_by_name",
            "description": "Query a previously built group of experts by name and use them to solve the execution_task you provide.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_name": {"type": "string", "description": "[REQUIRED] Name of a built group."},
                    "execution_task": {
                        "type": "string",
                        "description": "[REQUIRED] task that needs the experts to solve by conversation. It should include 1. the problem that needs to be solved and 2. the possible outlines/steps/instructions of how to solve this problem.",
                    },
                },
            },
            "required": ["group_name", "execution_task"],
        },
    }

    AUTOBUILD_TOOL = {
        "type": "function",
        "function": {
            "name": "autobuild",
            "description": "Use building_task to build a group of experts to solve your execution_task by conversation. This function will return the summarization of the conversation history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_name": {"type": "string", "description": "[REQUIRED] Name of the group."},
                    "building_task": {
                        "type": "string",
                        "description": "[REQUIRED] instruction that helps a build manager to build a group of experts for your task. You must describe the building_task as detailed as possible without any ambigious, highlight the coding and verification skills, and suggest some possible experts' identity with corresponding description. Note that coding skill is useful in most situations. Building_task should also include the information of execution_task without any deletion or ambigious.",
                    },
                    "execution_task": {
                        "type": "string",
                        "description": "[REQUIRED] task that needs the experts to solve by conversation. It should include the problem that needs to be solved. You cannot modify any task information from meta_user_proxy, including code blocks, but you can provide extra information.",
                    },
                },
            },
            "required": ["group_name", "building_task", "execution_task"],
        },
    }

    AUTOBUILD_SYSTEM_MESSAGE = """
# Your role
You are a manager of a group of advanced experts.

# When a task is assigned to you...
1. Analysis of its constraints and conditions for completion. 
2. Response with a specific plan of how to solve the task.
3. Divide the task into smaller, logically consistent subtasks.

# How to solve the task
You can solve the task in two ways:
1. Delegate the resolution of tasks to other experts created by "autobuild" and derive conclusive insights from their conversation summarization.
2. Analysis and solve the task by your coding and language skills.

## Some useful instructions
- Solve the task step by step if you need to. 
- Be clear about which step uses code, which step uses your language skill, and which step to build a group chat.
- If the code's result indicates there is an error, fix the error and output the code again. 
- If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
- When you find an answer, verify the answer carefully. 
- Include verifiable evidence in your response if possible.

# About "autobuild"
## Overall
- Autobuild can build a group of experts and let them chat with each other in a group chat to solve the task you provided.
- The experts cannot access your previous messages, make sure you have provided enough information for them.
- Autobuild will summarize the essence of the experts' conversation and the derived conclusions.
- You cannot modify any task information from meta_user_proxy, including code blocks, but you can provide extra information.
- Within a single response, you are limited to initiating one group of experts.

## How to use autobuild?
You should suggest a building_task and an execution_task.

### building_task
- The instruction that helps a build manager to build a group of experts for your task.
- You must describe the building_task as detailed as possible.
- You should highlight the coding and verification part
- You should suggest some possible experts' name with corresponding descriptions, e.g., algebra_expert
- Coding skills are useful in most situations.
- building_task should also include the information of execution_task without any deletion or ambiguity.

### execution_task
- The task that needs the experts to solve by conversation. 
- It should include the problem that needs to be solved without any deletion or ambiguity.
- Every time you provide the execution_task, check the initial task again and make sure the modified execution task includes the user's task information. 

## What should do after autobuild?
- After you receive the summarization, you should conduct a thorough verification.
- If the experts cannot make a conclusion for your task, analyze the summarization and the execution task carefully and try again with the same group name but a modified execution task. 
- After completing all tasks and verifications, you should conclude the operation and reply "TERMINATE"
"""

    META_PROMPTING_SYSTEM_MESSAGE = """You are Meta-Expert, an extremely clever expert with the unique ability to collaborate with multiple experts (such as Expert Problem Solver, Expert Mathematician, Expert Essayist, etc.) to tackle any task and solve any complex problems. Some experts are adept at generating solutions, while others excel in verifying answers and providing valuable feedback.

As Meta-Expert, your role is to oversee the communication between the experts, effectively using their skills to answer a given question while applying your own critical thinking and verification abilities.

To communicate with a expert, call function "meta_prompting" with the expert's name, identity information and the task that needs to be solved. The function will return a response from the expert.

Ensure that your instructions are clear and unambiguous, and include all necessary information within the triple quotes. You should assign personas to the experts (e.g., "You are a physicist specialized in...").

You can interact with only one expert at a time, and break complex problems into smaller, solvable tasks if needed. Each interaction is treated as an isolated event, so include all relevant details in every call.

If you or an expert finds a mistake in another expert's solution, ask a new expert to review the details, compare both solutions, and give feedback. You can request an expert to redo their calculations or work, using input from other experts. Keep in mind that all experts, except yourself, have no memory! Therefore, always provide complete information in your instructions when contacting them. Since experts can sometimes make errors, seek multiple opinions or independently verify the solution if uncertain. Before providing a final answer, always consult an expert for confirmation. Ideally, obtain or verify the final solution with two independent experts. However, aim to present your final answer within 15 rounds or fewer.

Refrain from repeating the very same questions to experts. Examine their responses carefully and seek clarification if required, keeping in mind they don't recall past interactions.

Upon the completion of all tasks and verifications, you should conclude the operation and reply "TERMINATE" in the end.
"""

    DEFAULT_DESCRIPTION = "A helpful AI assistant that can build a group of agents at a proper time to solve a task."

    def __init__(
        self,
        name: str,
        system_message: Optional[str] = None,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "NEVER",
        code_execution_config: Optional[Union[Dict, Literal[False]]] = False,
        description: Optional[str] = DEFAULT_DESCRIPTION,
        nested_mode: Optional[str] = "autobuild",
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            system_message (str): system message for the ChatCompletion inference.
                Please override this attribute if you want to reprogram the agent.
            llm_config (dict): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            nested_mode (str): the mode meta agent use to create nested chat.
                Should be in "meta_prompting" or "autobuild".
            **kwargs (dict): Please refer to other kwargs in
                [ConversableAgent](conversable_agent#__init__).
        """
        super().__init__(
            name,
            is_termination_msg=is_termination_msg,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            code_execution_config=code_execution_config,
            llm_config=llm_config,
            description=description,
            **kwargs,
        )

        if nested_mode == "autobuild":
            if system_message is None:
                system_message = self.AUTOBUILD_SYSTEM_MESSAGE
            self.update_tool_signature(self.AUTOBUILD_TOOL, is_remove=False)
            # self.update_tool_signature(self.AUTOBUILD_QUERY_TOOL, is_remove=False)
        elif nested_mode == "meta_prompting":
            if system_message is None:
                system_message = self.META_PROMPTING_SYSTEM_MESSAGE
            self.update_tool_signature(self.META_PROMPTING_TOOL, is_remove=False)
        else:
            raise 'Invalid nested_mode, should be "autobuild" or "meta_prompting".'

        self.update_system_message(system_message)
