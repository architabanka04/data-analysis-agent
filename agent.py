import re

import pandas as pd

from client import send_request
from executor import run_code

DATA_PATH = "datasets/sample_sales.csv"
OUTPUT_PATH = "outputs/cleaned_sales.csv"


def describe_data(path):
    df = pd.read_csv(path)
    return (
        f"Rows: {len(df)}\n"
        f"Columns and types:\n{df.dtypes.to_string()}\n\n"
        f"First 10 rows:\n{df.head(10).to_string()}"
    )


def extract_code(reply):
    match = re.search(r"```(?:python)?\n(.*?)```", reply, re.DOTALL)
    return match.group(1).strip() if match else reply.strip()


def run_task(instruction):
    prompt = f"""You are a data analyst. Write Python code using pandas.

Task: {instruction}

The data is in the file: {DATA_PATH}
Here is what it looks like:
{describe_data(DATA_PATH)}

Rules:
- Read the file from {DATA_PATH}
- Save the result to {OUTPUT_PATH} (create the outputs folder if needed)
- Print a short summary of what you changed
- Reply with ONLY the code, inside one python code block"""

    reply = send_request(prompt)
    code = extract_code(reply)
    result = run_code(code)
    return code, result


if __name__ == "__main__":
    code, result = run_task("Clean this dataset")
    print("=== CODE THE AI WROTE ===")
    print(code)
    print()
    print("=== WHAT HAPPENED ===")
    print("Success:", result["success"])
    print(result["output"] if result["success"] else result["error"][-800:])
