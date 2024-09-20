from common.chatter import Chatter
from libs.prompts import Prompts
from libs.typing import Dataset, Role
import logging

prompts = Prompts(role=Role.TEST_DESIGNER)


def fetch_completion(data_entry, times: int = 1):
    if "need_reproduce" in data_entry.keys() and data_entry["need_reproduce"] is False:
        return data_entry

    chatter = Chatter(system_message="You are a code developer assistant.")
    global prompts
    if prompts.DATASET == Dataset.HUMAN_EVAL:
        few_shot_prompt = prompts.few_shot_prompt
        prompts.template_prompt = {
            "few_shot_prompt": few_shot_prompt,
            "prompt": data_entry["prompt"],
        }
    test_case_list = []
    for i in range(times):
        # NOTE: The below while loop is a dangerous code block. ==> chê
        while True:
            completion = chatter.chat(prompts.template_prompt)
            if completion != "":
                break
            break
        completion = chatter.postprocess_code_completion(completion)
        test_case_list.append(completion)
    data_entry["test_case_list"] = test_case_list
    return data_entry


if __name__ == "__main__":
    data_entry = {
        "prompt": """
from typing import List
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    \"\"\"
"""
    }
    data_entry = fetch_completion(data_entry)
    logging.info(data_entry["test_case_list"])
