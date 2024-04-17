import pandas as pd
from sentence_transformers import SentenceTransformer, util
import json
import os
import re
from autogen.tool_utils import standardize, standardize_category, change_name, process_retrieval_document, build_tool_description, reformat_api_json
from autogen.tool_utils import find_callables
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import UserProxyAgent, AssistantAgent

class ToolBuilder:
    TOOL_USING_PROMPT = """## Functions
    You have access to the following functions. They can be accessed from the module called 'functions' by their function names.
For example, if there is a function called `foo` you could import it by writing `from functions import foo`

{functions}
"""

    def __init__(self, corpus_path, retriever):

        self.df = pd.read_csv(corpus_path, sep='\t')
        document_list = self.df['document_content'].tolist()

        self.model = SentenceTransformer(retriever)
        self.embeddings = self.model.encode(document_list)
    
    def retrieve(self, query, top_k=3):
        # Encode the query using the Sentence Transformer model
        query_embedding = self.model.encode([query])

        hits = util.semantic_search(query_embedding, self.embeddings, top_k=top_k)
        
        results = []
        for hit in hits[0]:
            results.append(self.df.iloc[hit['corpus_id'], 1])
        return results
    
    def bind(self, agent: AssistantAgent, functions: str):
        """Binds the function to the agent so that agent is aware of it."""
        sys_message = agent.system_message
        sys_message += self.TOOL_USING_PROMPT.format(functions=functions)
        agent.update_system_message(sys_message)
        print("Updated system message for ", agent.name, ": ", sys_message)
        return
    
    def bind_user_proxy(self, agent: UserProxyAgent, tool_root: str):
        """
        Updates user proxy agent with a executor so that code executor can successfully execute function-related code.
        Returns an updated user proxy.
        """
        # Find all the functions in the tool root
        functions = find_callables(tool_root)

        code_execution_config = agent._code_execution_config
        executor = LocalCommandLineCodeExecutor(
            timeout=code_execution_config.get("timeout", 180),
            work_dir=code_execution_config.get("work_dir", "groupchat"),
            functions=functions
        )
        code_execution_config = {
            "executor": executor,
            "last_n_messages": code_execution_config.get("last_n_messages", 1)
        }
        updated_user_proxy = UserProxyAgent(
            name=agent.name,
            is_termination_msg=agent._is_termination_msg,
            code_execution_config=code_execution_config,
            human_input_mode="NEVER",
            default_auto_reply=agent._default_auto_reply
        )
        return updated_user_proxy


# class ToolRetriever:
#     def __init__(self, corpus_tsv_path = "tools/corpus_dedup.tsv", model_path="ToolIR/", tool_path="tools/toollib"):
#         self.corpus_tsv_path = corpus_tsv_path
#         self.model_path = model_path
#         self.tool_path = tool_path
#         self.corpus, self.corpus2tool = self.build_retrieval_corpus()
#         self.embedder = self.build_retrieval_embedder()
#         self.corpus_embeddings = self.build_corpus_embeddings()

#     def build_retrieval_corpus(self):
#         print("Building corpus...")
#         documents_df = pd.read_csv(self.corpus_tsv_path, sep='\t')
#         corpus, corpus2tool = process_retrieval_document(documents_df)
#         corpus_ids = list(corpus.keys())
#         corpus = [corpus[cid] for cid in corpus_ids]
#         return corpus, corpus2tool

#     def build_retrieval_embedder(self):
#         print("Building embedder...")
#         embedder = SentenceTransformer(self.model_path)
#         return embedder

#     def build_corpus_embeddings(self):
#         print("Building corpus embeddings with embedder...")
#         corpus_embeddings = self.embedder.encode(self.corpus, convert_to_tensor=True)
#         return corpus_embeddings

#     def retrieving(self, query, top_k=5, excluded_tools={}):
#         print("Retrieving...")
#         query_embedding = self.embedder.encode(query, convert_to_tensor=True)
#         hits = util.semantic_search(query_embedding, self.corpus_embeddings, top_k=10*top_k, score_function=util.cos_sim)
#         retrieved_tools = []
#         for rank, hit in enumerate(hits[0]):
#             # category, tool_name, api_name, example_response = self.corpus2tool[self.corpus[hit['corpus_id']]].split('\t') 
#             category, tool_name, api_name = self.corpus2tool[self.corpus[hit['corpus_id']]].split('\t') 
#             category = standardize_category(category)
#             tool_name = standardize(tool_name) # standardizing
#             api_name = change_name(standardize(api_name)) # standardizing
#             if category in excluded_tools:
#                 if tool_name in excluded_tools[category]:
#                     top_k += 1
#                     continue
#             tmp_dict = {
#                 "category": category,
#                 "tool_name": tool_name,
#                 "api_name": api_name,
#                 # "response": example_response
#             }
#             retrieved_tools.append(tmp_dict)
#         return retrieved_tools
    
#     def retrieve(self, query, top_k=5):
#         retrieved_tools = self.retrieving(query=query, top_k=top_k)

#         valid_api_count = 0
#         data_dict = {"api_list": []}
#         for tool_dict in retrieved_tools:
#             if valid_api_count == top_k:
#                 break
#             category = tool_dict["category"]
#             tool_name = tool_dict["tool_name"]
#             api_name = tool_dict["api_name"]
#             # example_response = tool_dict["response"]
#             # check if api exists
#             if os.path.exists(self.tool_path):
#                 if os.path.exists(os.path.join(self.tool_path, category)):
#                     if os.path.exists(os.path.join(self.tool_path, category, tool_name+".json")):
#                         valid_api_count += 1
#                         tool_name = standardize(tool_name)
#                         api_name = change_name(standardize(api_name))
#                         tool_json = json.load(open(os.path.join(self.tool_path, category, tool_name + ".json"), "r"))
#                         api_dict_names = []
#                         append_flag = False
#                         for api_dict in tool_json["api_list"]:
#                             api_dict_names.append(api_dict["name"])
#                             pure_api_name = change_name(standardize(api_dict["name"]))
#                             if pure_api_name != api_name:
#                                 continue
#                             api_json = {}
#                             api_json["category_name"] = category
#                             api_json["api_name"] = api_dict["name"]
#                             api_json["api_description"] = api_dict["description"]
#                             api_json["required_parameters"] = api_dict["required_parameters"]
#                             api_json["optional_parameters"] = api_dict["optional_parameters"]
#                             api_json["tool_name"] = tool_json["tool_name"]
#                             # api_json["example_response"] = example_response
#                             data_dict["api_list"].append(api_json)
#                             append_flag = True
#                             break
#                         if not append_flag:
#                             print("[WARNING] Tool not found:")
#                             print(api_name, api_dict_names)
#                     else:
#                         raise Exception()

#         functions = []
#         for k, api_json in enumerate(data_dict["api_list"]):
#             openai_function_json, _, _ = reformat_api_json(api_json)
#             functions.append(openai_function_json)
#         return functions