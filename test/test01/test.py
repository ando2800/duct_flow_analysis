# main.py

import sys
from pathlib import Path

# === Set path to import duct_log_extract.py === #
LIB_UTIL_PATH = Path(__file__).resolve().parent.parent.parent / "lib"
sys.path.insert(0, str(LIB_UTIL_PATH))

from ductlogRL2hdf5 import convert_log_to_hdf5

# === Configuration === #
input_root = Path("./data/raw")
output_root = Path("./data/processed")

# === Ask user which episode to extract === #
episode_input = input("Enter episode number (e.g. 1): ").strip()
if not episode_input.isdigit():
    print("[ERROR] Invalid episode number.")
    sys.exit(1)

episode_num = int(episode_input)
ep_dir = output_root / f"ep{episode_num:03d}"
ep_dir.mkdir(parents=True, exist_ok=True)

# === Process all log files for the episode === #
pattern = f"screanoutput{episode_num}-*"
log_files = sorted(input_root.glob(pattern))

if not log_files:
    print(f"[WARNING] No log files found for episode {episode_num}.")
    sys.exit(0)

for log_file in log_files:
    print(f"[INFO] Processing {log_file.name}...")
    convert_log_to_hdf5(log_path=log_file, output_dir=ep_dir)

