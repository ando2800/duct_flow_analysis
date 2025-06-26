import numpy as np

# datファイルを読み込む（スペース区切りの場合）
data_path = "./data/processed/I4vorts_tsd_all.dat"
data = np.loadtxt(data_path)

I_4vorts = 4
Ssum = 5

# 閾値を超える列のインデックスを取得
columns = np.where((data[:,I_4vorts] < -0.5) & (data[:,Ssum] > 0.013))[0]
nhist = (columns+1) // 141 + 2 # 1始まりで表示するために+1、 さらに商に+1

print("条件を満たすnhist:", nhist)  # 1始まりで表示