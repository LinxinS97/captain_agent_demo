echo "*********************DA-Bench*********************"
cd DA/DA-bench
python Scripts/init_tasks.py
wait
echo "*********************DA-Bench/MetaPrompt_autogen*********************"
echo "Yes" | autogenbench run Tasks/da_MetaPrompt_autogen.jsonl --native -s 1
wait
echo "*********************DA-Bench/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/da_MetaAgent.jsonl --native -s 1
wait
echo "*********************DA-Bench/AutoBuild*********************"
echo "Yes" | autogenbench run Tasks/da_AutoBuild.jsonl --native -s 1
wait
echo "*********************DA-Bench/TwoAgents*********************"
echo "Yes" | autogenbench run Tasks/da_TwoAgents.jsonl --native -s 1
wait
echo "*********************DA-Bench/SingleLLM*********************"
echo "Yes" | autogenbench run Tasks/da_SingleLLM.jsonl --native -s 1
wait

echo "*********************MATH*********************"
cd ../math/MATH
python Scripts/init_tasks.py
wait
echo "*********************MATH/MetaPrompt_autogen*********************"
echo "Yes" | autogenbench run Tasks/math_MetaPrompt_autogen.jsonl --native -s 1
wait
echo "*********************MATH/TwoAgents*********************"
echo "Yes" | autogenbench run Tasks/math_TwoAgents.jsonl --native -s 1
wait
echo "*********************MATH/AutoBuild*********************"
echo "Yes" | autogenbench run Tasks/math_AutoBuild.jsonl --native -s 1
wait
echo "*********************MATH/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/math_MetaAgent.jsonl --native -s 1
wait
echo "*********************MATH/SingleLLM*********************"
echo "Yes" | autogenbench run Tasks/math_SingleLLM.jsonl --native -s 1
wait

echo "*********************HumanEval*********************"
cd ../programming/HumanEval
python Scripts/init_tasks.py
wait
echo "*********************HumanEval/MetaPrompt_autogen*********************"
echo "Yes" | autogenbench run Tasks/human_eval_MetaPrompt_autogen.jsonl --native -s 1
wait
echo "*********************HumanEval/TwoAgents*********************"
echo "Yes" | autogenbench run Tasks/human_eval_TwoAgents.jsonl --native -s 1
wait
echo "*********************HumanEval/AutoBuild*********************"
echo "Yes" | autogenbench run Tasks/human_eval_AutoBuild.jsonl --native -s 1
wait
echo "*********************HumanEval/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/human_eval_MetaAgent.jsonl --native -s 1
wait
echo "*********************HumanEval/SingleLLM*********************"
echo "Yes" | autogenbench run Tasks/human_eval_SingleLLM.jsonl --native -s 1
wait

echo "*********************SciBench/Chem*********************"
cd ../sci/Chemistry
python Scripts/init_tasks.py
wait
echo "*********************HumanEval/MetaPrompt_autogen*********************"
echo "Yes" | autogenbench run Tasks/sci_chem_MetaPrompt_autogen.jsonl --native -s 1
wait
echo "*********************HumanEval/TwoAgents*********************"
echo "Yes" | autogenbench run Tasks/sci_chem_TwoAgents.jsonl --native -s 1
wait
echo "*********************HumanEval/AutoBuild*********************"
echo "Yes" | autogenbench run Tasks/sci_chem_AutoBuild.jsonl --native -s 1
wait
echo "*********************HumanEval/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/sci_chem_MetaAgent.jsonl --native -s 1
wait
echo "*********************HumanEval/SingleLLM*********************"
echo "Yes" | autogenbench run Tasks/sci_chem_SingleLLM.jsonl --native -s 1
wait

echo "*********************SciBench/Phy*********************"
cd ../sci/Physics
python Scripts/init_tasks.py
wait
echo "*********************HumanEval/MetaPrompt_autogen*********************"
echo "Yes" | autogenbench run Tasks/sci_phy_MetaPrompt_autogen.jsonl --native -s 1
wait
echo "*********************HumanEval/TwoAgents*********************"
echo "Yes" | autogenbench run Tasks/sci_phy_TwoAgents.jsonl --native -s 1
wait
echo "*********************HumanEval/AutoBuild*********************"
echo "Yes" | autogenbench run Tasks/sci_phy_AutoBuild.jsonl --native -s 1
wait
echo "*********************HumanEval/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/sci_phy_MetaAgent.jsonl --native -s 1
wait
echo "*********************HumanEval/SingleLLM*********************"
echo "Yes" | autogenbench run Tasks/sci_phy_SingleLLM.jsonl --native -s 1
wait
