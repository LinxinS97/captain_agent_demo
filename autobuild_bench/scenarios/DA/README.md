# DA bench
## How to run
Download files in this [link](https://github.com/InfiAgent/InfiAgent/tree/main/examples/DA-Agent/data/da-dev-tables) to `autobuild_bench/scenarios/DA/Templates/TwoAgents/files` and `autobuild_bench/scenarios/DA/Templates/MetaPrompt/files`.

Generate task jsonl files.
```bash
python Scripts/init_tasks.py
```
This will randomly select 20 tasks from the original task list and convert it to the desired format.

Run all the tasks.
```bash
echo 'Yes' | autogenbench run Tasks/two_agents.jsonl --native
```

## TO-DOs
- Write the scenarios to run autobuild

## Notes
- 有些任务在目前框架下是无法完成的，如id: 733

{"id": 733, "question": "Apply feature engineering techniques to create a new feature in the dataset that represents the GDP per capita in logarithmic scale (base 10). Implement this feature transformation using Python code.", "concepts": ["Feature Engineering"], "constraints": "Calculate the logarithm with base 10.\nWhile calculating the logarithm, assume all GDP per capita figures are positive.", "format": "**@has_nan_values_in_new_feature[boolean]**\n@new_feature_mean[mean]\n@new_feature_std[std]\nwhere \"boolean\" is True or False, indicating whether there are NaN values in the newly created feature.\nwhere \"mean\" is a number (rounded to 2 decimal places) representing the mean of the newly created feature.\nwhere \"std\" is a number (rounded to 2 decimal places) representing the standard deviation of the newly created feature.", "file_name": "gapminder_cleaned.csv", "answer": [**["has_nan_values_in_new_feature", "False"]**, ["new_feature_mean", "3.54"], ["new_feature_std", "0.54"]]}

需要检查新特征里是否有nan value，新特征的mean和avg。这个检测标准在问题里没有提到，故assistant的回答没有包含相关信息，无法用checker_proxy直接提取其中的内容，所以会导致checker返回：答案没有提供，导致一直错误。

目前的workaround：人为检查，保证task是QA相关的，回答可以从assistant的回答中提取。
