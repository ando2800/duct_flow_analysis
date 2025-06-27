import sys
from pathlib import Path
#from .ductlogRL2hdf5 import convert_log_to_hdf5 #テスト用コード（ライブラリにおいていない。改良するならまずこれを改良して）

# === Set path for library === # 
LIB_UTIL_PATH = Path(__file__).resolve().parent.parent.parent / "lib"
sys.path.insert(0, str(LIB_UTIL_PATH))

from log2hdf5 import convert_log_to_hdf5

# === Note: The following section is for several log files( with RL) processing === #

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
# ================ #

"""
# === Note: The following section is for single log file processing === #
# === 対象ログファイル（直接指定）=== #
log_path = Path("./data/raw/output.txt")  # ← ここを書き換えて使う
output_dir = Path("./data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# === 出力ファイル名 === #
output_file_name = f"output.h5"  # ← ここも適宜変更可
output_path = output_dir / output_file_name

# === 実行 === #
print(f"[INFO] Processing single log file: {log_path.name}")
convert_log_to_hdf5(log_path=log_path, output_dir=output_dir, filename=output_file_name)
# ================ #
"""