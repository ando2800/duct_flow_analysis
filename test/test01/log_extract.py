# === log_extract.py ===
# ライブラリ的な位置づけ（データ抽出・変換ロジック）

import os
import re
import pandas as pd
import numpy as np
from pathlib import Path

def extract_constants(log_text):
    constants = {}
    match = re.search(r"MASSFLOW:\s+([0-9.Ee+-]+)", log_text)
    if match:
        constants["CMASSFLOW"] = float(match.group(1))

    match = re.search(r"dt\s*=\s*([0-9.Ee+-]+)", log_text)
    if match:
        constants["dt"] = float(match.group(1))

    match = re.search(r"nstep\s*=\s*([0-9]+)", log_text)
    if match:
        constants["nstep"] = int(match.group(1))

    match = re.search(r"nhist\s*=\s*([0-9]+)", log_text)
    if match:
        constants["nhist"] = int(match.group(1))

    constants["h"] = 1.0  # duct height is assumed fixed
    return constants

def extract_energy_blocks(log_text):
    ener_lines = [line for line in log_text.splitlines() if line.strip().startswith("ENER")]
    data = []
    for line in ener_lines:
        parts = line.strip().split()
        try:
            Sn, Sw, Ss, Se = map(float, parts[13:17])
            data.append([Sn, Sw, Ss, Se])
        except (IndexError, ValueError):
            continue
    return data

def calc_I(sectors):
    Sn, Sw, Ss, Se = sectors
    total = Sn + Sw + Ss + Se
    return 0.0 if total == 0 else (Sn + Ss - Sw - Se) / total

def calc_S(sectors, ub, h):
    Sn, Sw, Ss, Se = sectors
    return (Sn + Sw + Ss + Se) * ub / h

def convert_log_to_hdf5(log_path: Path, output_dir: Path):
    with open(log_path, "r") as f:
        log_text = f.read()

    constants = extract_constants(log_text)
    energy_data = extract_energy_blocks(log_text)

    if len(constants) < 4 or not energy_data:
        print(f"[WARNING] Skipping {log_path.name} due to missing data.")
        return

    CMASSFLOW = constants["CMASSFLOW"]
    h = constants["h"]
    ub = CMASSFLOW / 4.0
    dt = constants["dt"]
    dt_nondim = dt * ub / h
    nstep = constants["nstep"]
    nhist = constants["nhist"]

    df = pd.DataFrame(energy_data, columns=["Sn", "Sw", "Ss", "Se"])
    df["time_nondim"] = dt_nondim + 10 * dt_nondim * np.arange(len(df))
    df["I"] = df[["Sn", "Sw", "Ss", "Se"]].apply(lambda row: calc_I(row), axis=1)
    df["Ssum"] = df[["Sn", "Sw", "Ss", "Se"]].apply(lambda row: calc_S(row, ub, h), axis=1)

    os.makedirs(output_dir, exist_ok=True)
    h5file = output_dir / f"{log_path.stem}.h5"
    with pd.HDFStore(h5file, mode="w") as store:
        store.put("/statistics/Sn", df["Sn"])
        store.put("/statistics/Sw", df["Sw"])
        store.put("/statistics/Ss", df["Ss"])
        store.put("/statistics/Se", df["Se"])
        store.put("/new_statistics/Indicator", df["I"])
        store.put("/new_statistics/Ssum", df["Ssum"])
        store.put("/time_nondim", df["time_nondim"])

    print(f"[MESSAGE] Saved: {h5file}")
