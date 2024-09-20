from tqdm import tqdm
import logging

# from libs.codegeex.benchmark.utils import IMPORT_HELPER
from libs.codegeex.benchmark.execution import check_correctness, swallow_io, time_limit


def test_executor(data_entry: dict, lan: str = "python", thresh: int = 3):
    # test_setup = "\n".join(IMPORT_HELPER["python"]) + "\n"
    test_setup = ""

    if "need_reproduce" in data_entry.keys() and data_entry["need_reproduce"] is False:
        return data_entry

    completion_list = data_entry["completion_list"]
    test_case_list = data_entry["test_case_list"]
    correct_list = []

    for j in range(len(completion_list)):
        correct = 0
        if f"def {data_entry['entry_point']}" not in completion_list[j]:
            correct_list.append(correct)
            continue
        for k in range(len(test_case_list)):
            if f"assert {data_entry['entry_point']}(" not in test_case_list[k]:
                continue
            data_entry["test_code"] = (
                test_setup + "\n" + completion_list[j] + "\n" + test_case_list[k]
            )
            result = check_correctness(data_entry["task_id"], data_entry, lan, 3)
            if result["passed"]:
                correct += 1
        correct_list.append(correct)

    max_correct = max(correct_list)
    idx = correct_list.index(max_correct)

    data_entry["completion"] = data_entry["completion_list"][idx]
    data_entry["idx"] = idx
    data_entry["max_correct"] = max_correct
    # make decision about need to reproduce or not
    if max_correct >= thresh:
        data_entry["need_reproduce"] = False

    return data_entry


def test_report(dataset, lan):
    correct = 0
    # test_setup = '\n'.join(IMPORT_HELPER["python"]) + "\n"
    test_setup = ""
    for i in tqdm(range(len(dataset))):
        data_entry = dataset[i]
        try:
            with swallow_io():
                with time_limit(2.0):
                    exec(
                        test_setup
                        + "\n"
                        + data_entry["completion"]
                        + "\n"
                        + data_entry["test"]
                        + "\n"
                        + f"check({data_entry['entry_point']})"
                    )
                # No error util hear, that means passing all the test cases.
                correct += 1
        except Exception:
            pass
    logging.info("==============Start Report Testing==============")
    logging.info(f"test_report: {(correct/len(dataset)*100):.1f}")


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
""",
        "task_id": "HumanEval/0",
        "entry_point": "has_close_elements",
        "canonical_solution": """for idx, elem in enumerate(numbers):
        for idx2, elem2 in enumerate(numbers):
            if idx != idx2:
                distance = abs(elem - elem2)
                if distance < threshold:
                    return True

    return False
""",
        "test": """
METADATA = {
    'author': 'jt',
    'dataset': 'test'
}
def check(candidate):
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False
""",
    }
    from agent.programmer import fetch_completion as programmer
    from agent.test_designer import fetch_completion as test_designer

    data_entry = programmer(data_entry)
    data_entry = test_designer(data_entry, times=3)
    data_entry = test_executor(data_entry)

    logging.info(data_entry)
