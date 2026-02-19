import json
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd


def read_fasta(file_path) -> list[str]:

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    sequences = []
    seq_lines = []

    with path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if seq_lines:
                    sequences.append("".join(seq_lines))
                    seq_lines = []
            else:
                seq_lines.append(line)

        if seq_lines:
            sequences.append("".join(seq_lines))

    return sequences


def read_json(file_path) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    with path.open("r") as f:
        data = json.load(f)
    return data


def remove_folder(folder_path):

    folder = Path(folder_path)
    if folder.exists() and folder.is_dir():
        shutil.rmtree(folder)
    else:
        raise FileNotFoundError(f"path not exist or not dir: {folder.resolve()}")



def create_time_folder(base_path="./tasks"):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    folder_path = Path(base_path) / timestamp

    folder_path.mkdir(parents=True, exist_ok=False)
    return folder_path


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def create_time_folder_with_timestamp(base_path="./tasks", timestamp=None):
    if timestamp is None:
        timestamp = generate_timestamp()
    folder_path = Path(base_path) / timestamp
    folder_path.mkdir(parents=True, exist_ok=False)
    return folder_path

def build_result_path(base_path, timestamp, filename, suffix):
    folder_path = Path(base_path) / timestamp
    suffix = f".{suffix.lower()}"
    return folder_path / f"{filename}{suffix}"


def format_transfer(json_str: str, workdir: Path, filename: str, format: str = "json"):
    workdir = Path(workdir)
    if not workdir.exists():
        raise FileNotFoundError(f"path not exist: {workdir.resolve()}")

    data = json.loads(json_str)

    out_path = workdir / f"{filename}.{format.lower()}"
    if format.lower() == "json":
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    elif format.lower() == "csv":
        df = pd.json_normalize(data)
        df.to_csv(out_path, sep=",", index=False, encoding="utf-8")


    else:
        raise ValueError(f"unsupported format: {format}")

    return out_path