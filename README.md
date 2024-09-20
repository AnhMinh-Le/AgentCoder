# AgentCoder
Recode for the paper https://arxiv.org/abs/2312.13010

## Installation
If you want to install locally, run command below
```bash
pip install -r requirements-dev.txt
pre-commit install
```
Create a copy of file `.env.example`, then rename it to `.env`, and fill the neccessary fields.
## Inference
```bash
python scripts/infer_example.py
```

## Acknowledgments
This code is based on the [AgentCoder paper](https://arxiv.org/abs/2312.13010), and 2 repos: [AgentCoder](https://github.com/huangd1999/AgentCoder), [CodeGeeX](https://github.com/THUDM/CodeGeeX)
