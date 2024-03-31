# GAIA Benchmark

This scenario implements the [GAIA](https://arxiv.org/abs/2311.12983) agent benchmark.

## Running Tasks

Setting the environment variable "BING_API_key". You can write the following command in .bashrc:
```sh
export BING_API_key='[Your Key]'
```

Level 1 tasks:
```sh
autogenbench run Tasks/gaia_test_level_1__two_agents.jsonl
autogenbench tabulate Results/gaia_test_level_1__two_agents
```

## References
**GAIA: a benchmark for General AI Assistants**<br/>
Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, Thomas Scialom<br/>
[https://arxiv.org/abs/2311.12983](https://arxiv.org/abs/2311.12983)
