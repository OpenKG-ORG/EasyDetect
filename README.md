<div align="center">

<img src="figs/logo.png" width="300px">

**An Easy-to-use Hallucination Detection Framework for LLMs**

---

<p align="center">
  <a href="https://huggingface.co/spaces/zjunlp/MHaluBench">Datasets</a> •
  <a href="#overview">Overview</a> •
  <a href="#quickstart">Quickstart</a> •
\  <a href="#citation">Citation</a> •
  <a href="#contributors">Contributors</a>
</p>

![](https://img.shields.io/badge/version-v0.1.1-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![](https://img.shields.io/github/last-commit/zjunlp/EasyInstruct?color=green) 
![](https://img.shields.io/badge/PRs-Welcome-red) 

</div>

## Table of Contents

- <a href="#news">What's New</a>
- <a href="#overview">Overview</a>
- <a href="#quickstart">Quickstart</a>
  - <a href="#shell-script">Shell Script</a>
  - <a href="#gradio-app">Gradio App</a>
- <a href="#citation">Citation</a>
- <a href="#contributors">Contributors</a>

<!-- ## 🔔News

- **2023-12-9 The paper "[When Do Program-of-Thoughts Work for Reasoning?](https://arxiv.org/abs/2308.15452)" (supported by EasyInstruct), is accepted by AAAI 2024!**
- **2023-10-28 We release version 0.1.1, supporting for new features of instruction generation and instruction selection.**
- **2023-8-9 We release version 0.0.6, supporting Cohere API calls.**
- **2023-7-12 We release [EasyEdit](https://github.com/zjunlp/EasyEdit), an easy-to-use framework to edit Large Language Models.**
<details>
<summary><b>Previous news</b></summary>

- **2023-5-23 We release version 0.0.5, removing requirement of llama-cpp-python.**
- **2023-5-16 We release version 0.0.4, fixing some problems.**
- **2023-4-21 We release version 0.0.3, check out our [documentations](https://zjunlp.gitbook.io/easyinstruct/documentations) for more details.**
- **2023-3-25 We release version 0.0.2, suporting IndexPrompt, MMPrompt, IEPrompt and more LLMs**
- **2023-3-13 We release version 0.0.1, supporting in-context learning, chain-of-thought with ChatGPT.**
  
</details> -->

---



## 🌟Overview

EasyInstruct is a Python package which is proposed as an easy-to-use instruction processing framework for Large Language Models(LLMs) like GPT-3, Llama, ChatGLM in your research experiments. EasyInstruct modularizes instruction generation, selection, and prompting, while also considering their combination and interaction. 

<img src="figs/overview.png">

- The current supported instruction generation techniques are as follows:

  | **Methods** | **Description** |
  | --- | --- |
  | [Self-Instruct](https://arxiv.org/abs/2212.10560) | The method that randomly samples a few instructions from a human-annotated seed tasks pool as demonstrations and prompts an LLM to generate more instructions and corresponding input-output pairs. |
  | [Evol-Instruct](https://arxiv.org/abs/2304.12244) | The method that incrementally upgrades an initial set of instructions into more complex instructions by prompting an LLM with specific prompts. |
  | [Backtranslation](https://arxiv.org/abs/2308.06259) | The method that creates an instruction following training instance by predicting an instruction that would be correctly answered by a portion of a document of the corpus.  |
  | [KG2Instruct](https://arxiv.org/abs/2305.11527) | The method that creates an instruction following training instance by predicting an instruction that would be correctly answered by a portion of a document of the corpus. |




---

## ⏩Quickstart

We provide two ways for users to quickly get started with EasyInstruct. You can either use the shell script or the Gradio app based on your specific needs.

### Shell Script

#### Step1: Write a configuration file in yaml format

Users can easily configure the parameters of EasyInstruct in a yaml file or just quickly use the default parameters in the configuration file we provide. Following is an example of the configuration file for Self-Instruct.

```yaml
generator:
  SelfInstructGenerator:
    target_dir: data/generations/
    data_format: alpaca
    seed_tasks_path: data/seed_tasks.jsonl
    generated_instructions_path: generated_instructions.jsonl
    generated_instances_path: generated_instances.jsonl
    num_instructions_to_generate: 100
    engine: gpt-3.5-turbo
    num_prompt_instructions: 8
```

More example configuration files can be found at [configs](https://github.com/zjunlp/EasyInstruct/tree/main/configs).

#### Step2: Run the shell script

Users should first specify the configuration file and provide their own OpenAI API key. Then, run the follwing shell script to launch the instruction generation or selection process.

```shell
config_file=""
openai_api_key=""

python demo/run.py \
    --config  $config_file\
    --openai_api_key $openai_api_key \
```



---
### 🚩Citation

Please cite our repository if you use EasyInstruct in your work.

```bibtex
@misc{easyinstruct,
  author = {Yixin Ou and Ningyu Zhang and Honghao Gui and Zhen Bi and Yida Xue and Runnan Fang and Kangwei Liu and Lei Li and Shuofei Qiao and Huajun Chen},
  title = {EasyInstruct: An Easy-to-use Instruction Processing Framework for Large Language Models},
  year = {2023},
  url = {https://github.com/zjunlp/EasyInstruct},
}

@misc{knowlm,
  author = {Ningyu Zhang and Jintian Zhang and Xiaohan Wang and Honghao Gui and Kangwei Liu and Yinuo Jiang and Xiang Chen and Shengyu Mao and Shuofei Qiao and Yuqi Zhu and Zhen Bi and Jing Chen and Xiaozhuan Liang and Yixin Ou and Runnan Fang and Zekun Xi and Xin Xu and Lei Li and Peng Wang and Mengru Wang and Yunzhi Yao and Bozhong Tian and Yin Fang and Guozhou Zheng and Huajun Chen},
  title = {KnowLM: An Open-sourced Knowledgeable Large Langugae Model Framework},
  year = {2023},
 url = {http://knowlm.zjukg.cn/},
}

@misc{bi2023programofthoughts,
      author={Zhen Bi and Ningyu Zhang and Yinuo Jiang and Shumin Deng and Guozhou Zheng and Huajun Chen},
      title={When Do Program-of-Thoughts Work for Reasoning?}, 
      year={2023},
      eprint={2308.15452},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

---

## 🎉Contributors

<a href="https://github.com/zjunlp/EasyInstruct/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=zjunlp/EasyInstruct" />
</a>

We will offer long-term maintenance to fix bugs, solve issues and meet new requests. So if you have any problems, please put issues to us.
