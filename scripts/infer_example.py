import sys

sys.path.append("src")

from agent.pipeline import gencode, is_correct

import logging

logging.basicConfig(level=logging.INFO)

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
    data_entry = gencode(data_entry, epoch=1, test_designer_times=1, programmer_times=1)
    # Generate code is stored in data_entry["completion"]
    logging.info("Generated code:")
    logging.info(data_entry["completion"])

    # To check the generated code whether pass all the test cases, call function is_correct
    logging.info("Is the generated code passed all the test cases")
    logging.info(is_correct(data_entry))
