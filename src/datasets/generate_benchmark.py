import json
from agent.pipeline import gencode

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
    result = gencode(data_entry)
    result_lst.append(result)
    result["failed_test_cases"] = result.get("test", [])
    #print(data_entry['test'])

with open('output.json', 'w') as json_file:
    json.dump(result_lst, json_file, indent=4)

'''
true_count = sum(1 for res in result_lst if res.get("need_reproduce") is True)
false_count = sum(1 for res in result_lst if res.get("need_reproduce") is False)

print('True: ', true_count)
print('False: ', false_count)

'''
