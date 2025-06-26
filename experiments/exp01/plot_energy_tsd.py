import numpy as np
import matplotlib.pyplot as plt

# データファイルのパス
data_path = "./data/processed/I4vorts_tsd_59-67.dat"

# データ読み込み
data = np.loadtxt(data_path)

#sumをdatから抽出
y = data[:, 5]
x = range(len(y))

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.ylim(0.0, 0.017)
plt.tight_layout()
plt.savefig('./results/ener_tsd_seg59-67.pdf', dpi=300, format='pdf')