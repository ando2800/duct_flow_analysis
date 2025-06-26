import yaml
import os
import sys

# === プロジェクトルートの src を PYTHONPATH に追加 ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from flowlib.ductlog2hdf5 import ductlog2hdf5

# === YAMLの読み込み（このファイルと同じディレクトリから）===
with open("config.yaml") as f:
    config = yaml.safe_load(f)
    print("[DEBUG] config =", config)

ductlog2hdf5(
    inputfile="./data/raw/output.txt",
    outputfile="./data/processed/statistics_tsd.h5",
    config=config
)
