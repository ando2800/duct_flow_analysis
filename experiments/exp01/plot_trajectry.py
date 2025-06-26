import numpy as np
import matplotlib.pyplot as plt

# データファイルのパス
data_path = "./data/processed/I4vorts_tsd_59-67.dat"

# データ読み込み
data = np.loadtxt(data_path)

# 4列目（インデックス3）と5列目（インデックス4）を抽出
x = data[:, 5]
y = data[:, 4]

plt.figure(figsize=(8, 6))
plt.plot(x, y, linestyle='-',markersize=1, linewidth=1, color='black', alpha=0.7)
plt.plot(x[0], y[0], marker='o',markersize=3, color='red', label='start')
plt.plot(x[-1], y[-1], marker='o',markersize=3, color='blue', label='end')
plt.text(x[0], y[0], 'start', color='red', fontsize=12, va='bottom', ha='right')
plt.text(x[-1], y[-1], 'end', color='blue', fontsize=12, va='bottom', ha='left')
plt.xlim(0.0, 0.016)
plt.ylim(-1, 1)
plt.xlabel('Ssum')
plt.ylabel('I')
plt.grid(True)
plt.tight_layout()

plt.savefig('./results/trajectory_59-67_plot.pdf', dpi=300)