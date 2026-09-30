import subprocess
import sys
import tempfile

TIME_LIMIT = 20


def run_code(code):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name

    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=TIME_LIMIT,
        )
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": f"Stopped: took longer than {TIME_LIMIT} seconds"}

    return {
        "success": result.returncode == 0,
        "output": result.stdout.strip(),
        "error": result.stderr.strip(),
    }


if __name__ == "__main__":
    good = run_code("import pandas as pd\nprint(pd.Series([1, 2, 3]).sum())")
    print("GOOD CODE:", good)

    bad = run_code("print(undefined_name)")
    print("BAD CODE:", bad["success"], "-", bad["error"].splitlines()[-1])
