import os
import subprocess
import numpy as np

def calc_I_4vorts(sectors):
    sector1, sector2, sector3, sector4 = sectors
    total = sector1 + sector2 + sector3 + sector4
    if total == 0:
        return 0
    return (sector1 + sector3 - sector2 - sector4) / total

def calc_Ssum(sectors):
    CMASSFLOW = 1.92783340171785
    ub = CMASSFLOW / 4
    h = 1.0
    sector1, sector2, sector3, sector4 = sectors 
    return (sector1 + sector2 + sector3 + sector4) * ub / h

print('[MESSAGE] Create tsd of Indicator for 4 voticity .')
seg_start = 59
seg_end = 67
input_files = [f"./data/raw/log/screanoutput1-{i}" for i in range(seg_start, seg_end)]
output_file_path = "./data/processed/I4vorts_tsd_59-67.dat"
open(output_file_path, "w").close()  # 空ファイル作成

temp_files = []

for input_file in input_files:
    temp_output_file_path = f"./data/processed/temp_{os.path.basename(input_file)}.dat"
    temp_files.append(temp_output_file_path)
    open(temp_output_file_path, "w").close()

    # 必要なデータ抽出
    with open(temp_output_file_path, "a") as f:
        grep_process = subprocess.Popen(["grep", "ENER", input_file], stdout=subprocess.PIPE)
        awk_process = subprocess.Popen(["awk", "{print $14, $15, $16, $17}"],
                                stdin=grep_process.stdout, stdout=f, text=True)
        awk_process.communicate()

    try:
        data = np.loadtxt(temp_output_file_path)
        if data.ndim == 1:
            data = data.reshape(1, -1)
        # 新しい値を計算
        I_4vorts = np.apply_along_axis(calc_I_4vorts, 1, data)
        Ssum = np.apply_along_axis(calc_Ssum, 1, data)
        data_with_new_columns = np.column_stack((data, I_4vorts, Ssum))
        # 計算済みデータで一時ファイルを上書き
        np.savetxt(temp_output_file_path, data_with_new_columns)
    except Exception as e:
        open(temp_output_file_path, "w").close()
        print(f"[ERROR] Failed to process {input_file}: {e}")

# すべての一時ファイルをまとめて最終ファイルに追記
with open(output_file_path, "a") as output_file:
    for temp_path in temp_files:
        with open(temp_path, "r") as temp_file:
            output_file.write(temp_file.read())
        os.remove(temp_path)
