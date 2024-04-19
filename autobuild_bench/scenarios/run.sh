echo "*********************DA-Bench*********************"
cd DA/DA-bench
python Scripts/init_tasks.py
wait
# echo "*********************DA-Bench/MetaPrompt_autogen*********************"
# echo "Yes" | autogenbench run Tasks/da_MetaPrompt_autogen.jsonl --native
# wait
# echo "*********************DA-Bench/AutoBuild*********************"
# echo "Yes" | autogenbench run Tasks/da_AutoBuild.jsonl --native
# wait
# echo "*********************DA-Bench/TwoAgents*********************"
# echo "Yes" | autogenbench run Tasks/da_TwoAgents.jsonl --native
# wait
# echo "*********************DA-Bench/SingleLLM*********************"
# echo "Yes" | autogenbench run Tasks/da_SingleLLM.jsonl --native
# wait
echo "*********************DA-Bench/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/da_MetaAgent.jsonl --native
wait

echo "*********************MATH*********************"
cd ../../math/MATH
python Scripts/init_tasks.py
wait
# echo "*********************MATH/MetaPrompt_autogen*********************"
# echo "Yes" | autogenbench run Tasks/math_MetaPrompt_autogen.jsonl --native
# wait
# echo "*********************MATH/TwoAgents*********************"
# echo "Yes" | autogenbench run Tasks/math_TwoAgents.jsonl --native
# wait
# echo "*********************MATH/AutoBuild*********************"
# echo "Yes" | autogenbench run Tasks/math_AutoBuild.jsonl --native
# wait
# echo "*********************MATH/SingleLLM*********************"
# echo "Yes" | autogenbench run Tasks/math_SingleLLM.jsonl --native
# wait
echo "*********************MATH/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/math_MetaAgent.jsonl --native
wait

echo "*********************HumanEval*********************"
cd ../../programming/HumanEval
python Scripts/init_tasks.py
wait
# echo "*********************HumanEval/MetaPrompt_autogen*********************"
# echo "Yes" | autogenbench run Tasks/human_eval_MetaPrompt_autogen.jsonl --native
# wait
# echo "*********************HumanEval/TwoAgents*********************"
# echo "Yes" | autogenbench run Tasks/human_eval_TwoAgents.jsonl --native
# wait
# echo "*********************HumanEval/AutoBuild*********************"
# echo "Yes" | autogenbench run Tasks/human_eval_AutoBuild.jsonl --native
# wait
# echo "*********************HumanEval/SingleLLM*********************"
# echo "Yes" | autogenbench run Tasks/human_eval_SingleLLM.jsonl --native
# wait
echo "*********************HumanEval/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/r_human_eval_MetaAgent.jsonl --native
wait

echo "*********************SciBench/Chem*********************"
cd ../../sci/Chemistry
python Scripts/init_tasks.py
wait
# echo "*********************SciBench/Chem/MetaPrompt_autogen*********************"
# echo "Yes" | autogenbench run Tasks/sci_chem_MetaPrompt_autogen.jsonl --native
# wait
# echo "*********************SciBench/Chem/TwoAgents*********************"
# echo "Yes" | autogenbench run Tasks/sci_chem_TwoAgents.jsonl --native
# wait
# echo "*********************SciBench/Chem/AutoBuild*********************"
# echo "Yes" | autogenbench run Tasks/sci_chem_AutoBuild.jsonl --native
# wait
# echo "*********************SciBench/Chem/SingleLLM*********************"
# echo "Yes" | autogenbench run Tasks/sci_chem_SingleLLM.jsonl --native
# wait
echo "*********************SciBench/Chem/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/sci_chem_MetaAgent.jsonl --native
wait

echo "*********************SciBench/Phy*********************"
cd ../../sci/Physics
python Scripts/init_tasks.py
wait
# echo "*********************SciBench/Phy/MetaPrompt_autogen*********************"
# echo "Yes" | autogenbench run Tasks/sci_phy_MetaPrompt_autogen.jsonl --native
# wait
# echo "*********************SciBench/Phy/TwoAgents*********************"
# echo "Yes" | autogenbench run Tasks/sci_phy_TwoAgents.jsonl --native
# wait
# echo "*********************SciBench/Phy/AutoBuild*********************"
# echo "Yes" | autogenbench run Tasks/sci_phy_AutoBuild.jsonl --native
# wait
# echo "*********************SciBench/Phy/SingleLLM*********************"
# echo "Yes" | autogenbench run Tasks/sci_phy_SingleLLM.jsonl --native
# wait
echo "*********************SciBench/Phy/MetaAgent*********************"
echo "Yes" | autogenbench run Tasks/sci_phy_MetaAgent.jsonl --native
wait


echo "*********************GAIA*********************"
cd ../../retrieval/GAIA
python Scripts/init_tasks.py
wait
echo "*********************GAIA/MetaAgent 1*********************"
echo "Yes" | autogenbench run Tasks/gaia_validation_level1__MetaAgent.jsonl --native
wait
echo "*********************GAIA/MetaAgent 2*********************"
echo "Yes" | autogenbench run Tasks/gaia_validation_level2__MetaAgent.jsonl --native
wait
echo "*********************GAIA/MetaAgent 3*********************"
echo "Yes" | autogenbench run Tasks/gaia_validation_level3__MetaAgent.jsonl --native
wait
