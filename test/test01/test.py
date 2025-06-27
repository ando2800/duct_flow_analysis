# === run_extract.py ===
# ログ抽出実行スクリプト（ベタ書き指定）

from pathlib import Path
from log_extract import convert_log_to_hdf5

# === パラメータ指定 === #
episode = 1  # 対象エピソード番号
input_dir = Path("./data/raw")
output_root = Path("./data/processed")

# === 処理対象ログの検索 === #
ep_str = f"{episode:03d}"
log_files = sorted(input_dir.glob(f"screanoutput{episode}-*"))

if not log_files:
    print(f"[WARNING] No matching logs found for episode {episode}.")
else:
    output_dir = output_root / f"ep{ep_str}"
    for log_path in log_files:
        convert_log_to_hdf5(log_path, output_dir)
