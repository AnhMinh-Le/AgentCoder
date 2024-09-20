from libs.codegeex.benchmark.execution import check_correctness
from agent.programmer import fetch_completion as programmer
from agent.test_designer import fetch_completion as test_designer
from agent.test_executor import test_executor
import logging


def gencode(
    data_entry: dict,
    epoch: int = 2,
    programmer_times: int = 3,
    test_designer_times: int = 3,
) -> dict:
    for i in range(epoch):
        data_entry = programmer(data_entry, programmer_times)
        data_entry = test_designer(data_entry, test_designer_times)
        data_entry = test_executor(data_entry)
    return data_entry


def is_correct(data_entry: dict, lan: str = "python"):
    # test_setup = "\n".join(IMPORT_HELPER["python"]) + "\n"
    test_setup = ""
    func_name = data_entry["entry_point"]
    data_entry["test_code"] = (
        test_setup
        + "\n"
        + data_entry["completion"]
        + "\n"
        + data_entry["test"]
        + "\n"
        + f"check({func_name})"
    )
    # logging.info("-----Full code------")
    # logging.info(data_entry["test_code"])
    # logging.info("-----------------")
    result = check_correctness(data_entry["task_id"], data_entry, lan, 3)

    return result["passed"]


if __name__ == "__main__":
    data_entry = {
        "task_id": "HumanEval/6",
        "prompt": """from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    \"\"\" Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    \"\"\"
""",
        "entry_point": "parse_nested_parens",
        "canonical_solution": """    def parse_paren_group(s):
        depth = 0
        max_depth = 0
        for c in s:
            if c == '(':
                depth += 1
                max_depth = max(depth, max_depth)
            else:
                depth -= 1

        return max_depth

    return [parse_paren_group(x) for x in paren_string.split(' ') if x]
""",
        "test": """

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('(()()) ((())) () ((())()())') == [2, 3, 1, 3]
    assert candidate('() (()) ((())) (((())))') == [1, 2, 3, 4]
    assert candidate('(()(())((())))') == [4]
""",
    }
    data_entry = gencode(data_entry)
    logging.info(is_correct(data_entry))
