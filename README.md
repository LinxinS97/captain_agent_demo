# Captain Agent
These are the supplementary files for the "Adaptive In-conversation Team Building for Language Model Agents." They contain code for running the experiments in the paper.

The codebase is developed upon the AutoGen.

## Instruction
We use `autogenbench` to test all scenarios in our benchmark. For the detailed instruction on using `autogenbench`, please refer to [autogenbench](https://microsoft.github.io/autogen/blog/2024/01/25/AutoGenBench/).
We also provided some brief instructions for `autogenbench` below.

## Installation
The codebase is built upon autogenbench and autogen. So instead of installing via pip, you should install pyautogen and autogenbench in editable way:
```bash
cd /path/to/CaptainAgent
pip install -e .
cd /path/to/CaptainAgent/samples/autogenbench
pip install -e .
```

Modify the first line in `requirement.txt` to the path of your autogen-autobuild-dev.

## Evaluations
This is the general method to run evaluations on different scenarios. Use the following command to run the benchmark for each scenario:
```bash
cd [SCENARIO FOLDER. For example, /path/to/scenarios/MATH]
python Scripts/init_tasks.py  // initialize the tasks
autogenbench run Tasks/[TASK YOU WANT TO RUN].jsonl --native  // run the task. native is use to run the scenario without docker. If you have a docker environment, you can remove it.
autogenbench tabulate Results/[TASK YOU WANT TO RUN]  // print the results in tabulate.
```

If you want to debug, set `-s 1` to use a single data for testing:
```bash
cd [SCENARIO FOLDER. For example, /path/to/scenarious/MATH]
autogenbench run Tasks/[TASK YOU WANT TO RUN].jsonl -s 1
```
If you want to debug a specific problem, you can run the `scenario.py` in `Results/[YOUR TASK]/[PROBLEM ID]/0/scenario.py` manually in debug mode.

Note that every time the `autogenbench run TASK` is run, it checks the `Results` folder and only runs problems that are not in it. If you want to rerun the tasks, delete the corresponding files in the `Results` folder.

Some templates requires manual addition to the Templates/scenarios.py, it is recommended to check the code and fill out the placeholders. For detailed instructions on running each benchmark, please take a look at the respective readme in the folder.
