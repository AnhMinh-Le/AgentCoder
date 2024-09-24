import json
from agent.pipeline import gencode, is_correct
import logging

logging.basicConfig(filename='execution_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_dataset_from_jsonl(file_path: str) -> list[dict]:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data_entry = json.loads(line)
            data.append(data_entry)
    return data


def load_data_entry(dataset: list[dict], index: int) -> dict:
    data_entry = {
        "task_id": dataset[index]['task_id'],
        "prompt": dataset[index]['text'],
        "completion": dataset[index]['code'],
        "test": dataset[index]['test_list'],
        "test_setup": dataset[index]['test_setup_code'],
        "challenge_tests": dataset[index]['challenge_test_list'],
        "need_reproduce": True,
    }
    return data_entry


file_path = r'C:\Users\IDEAPAD\AgentCoder\src\datasets\mbpp.jsonl'
dataset = load_dataset_from_jsonl(file_path)
result_lst = []

for i in range(len(dataset)):
    data_entry = load_data_entry(dataset, i)
    logging.info(f'Processing task {data_entry["task_id"]}')

    result = gencode(data_entry)
    result["is_correct"] = is_correct(result)

    logging.info(f'Generated code for task {data_entry["task_id"]}: {result["completion"]}')
    logging.info(f'Test result for task {data_entry["task_id"]}: {result["is_correct"]}')

    result_lst.append(result)

with open('output.json', 'w') as json_file:
    json.dump(result_lst, json_file, indent=4)

true_count = sum(1 for res in result_lst if res.get("is_correct") is True)
false_count = sum(1 for res in result_lst if res.get("is_correct") is False)

logging.info(f'Total True: {true_count}, Total False: {false_count}')
