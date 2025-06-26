import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rc
import os
import time

filelds_path = "./data/raw/fields/"
output_dir = "./results/vw_uavg/"
file_first_num = int(input("first file No."))
file_last_num = int(input("last file No."))
output_format = input("Output format (eps/pdf/png): ").strip().lower()
latex_env = input("Do you have LaTeX environment installed? (yes/no): ").strip().lower() == 'yes'
add_axis_labels = latex_env
step_size = 200 # 500ステップごとに処理

if add_axis_labels:
    # LaTeXフォント設定
    rc('text', usetex=True)
    rc('font', family='serif')
    rc('font', size=30)

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_len = file_last_num - (file_first_num-1)
mx,my,mz = 128,65,65

y = np.zeros(my)
z = np.zeros(mz)

for j in range (my):
    y[j] = -np.cos((j*np.pi)/(my-1))

for k in range (mz):
    z[k] = -np.cos((k*np.pi)/(mz-1))

Z, Y = np.meshgrid(z, y) 

y_half = np.zeros(1+my//2)
z_half = np.zeros(1+mz//2)

for i in range (1+my//2):
    y_half[i]=y[2*i]
    z_half[i]=z[2*i]
Z_half, Y_half = np.meshgrid(z_half, y_half)

for start in range(file_first_num, file_last_num + 1, step_size):
    end = min(start + step_size - 1, file_last_num)
    current_len = end - start + 1

    vr_all = np.zeros((current_len, mz, my, mx))
    wr_all = np.zeros((current_len, mz, my, mx))
    tr_all = np.zeros((current_len, mz, my, mx))

    print("Data loading ...")
    data_start_time = time.time()
    for i in range(current_len):
        ifile = start + i

        file = h5py.File(f'{filelds_path}fields_{ifile:04}.vr.h5','r')
        vr_all[i] = file['/vr'][...]
        file.close()
        
        file = h5py.File(f'{filelds_path}fields_{ifile:04}.wr.h5','r')
        wr_all[i] = file['/wr'][...]
        file.close()

        file = h5py.File(f'{filelds_path}fields_{ifile:04}.tr.h5','r')
        tr_all[i] = file['/tr'][...]
        file.close()
    data_end_time = time.time()
    print(f"Data loading time for steps {start} to {end}: {data_end_time - data_start_time:.2f} seconds")

    vm = (vr_all.mean(axis=3))
    wm = (wr_all.mean(axis=3))
    tm = (tr_all.mean(axis=3))

    vm_half = np.zeros((current_len, 1+my//2, 1+mz//2))
    wm_half = np.zeros((current_len, 1+my//2, 1+mz//2))

    for j in range (current_len):
        for s in range (0, 1+my//2):
            for t in range (0, 1+mz//2):
                vm_half[j][s][t]=vm[j][2*s][2*t]
                wm_half[j][s][t]=wm[j][2*s][2*t]

    print("Ploting ...")
    # スナップショットの描画
    plot_start_time = time.time()
    for i in range (current_len):
        plot_file_num = start + i
        fig, ax = plt.subplots()
        ax.set_aspect("equal")

        # 軸の設定
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.tick_params(axis='both', which='major', labelsize=20)  # 軸のフォントサイズを設定

        # 軸の数値を小数点第一位でフォーマット
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:.1f}'))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f'{y:.1f}'))
        if add_axis_labels:
            # 軸ラベルを設定
            ax.set_xlabel(r'\textit{z/h}', fontsize=27)
            ax.set_ylabel(r'$\frac{y}{h}$', fontsize=35, rotation=0)

            # 軸ラベルの位置を微調整
            ax.xaxis.set_label_coords(0.5, -0.1)  # X軸ラベルの位置を調整
            ax.yaxis.set_label_coords(-0.18, 0.44)  # Y軸ラベルの位置を調整

        # カラーバーの設定
        ContourTemp = ax.contourf(-Y, Z, tm[i], cmap='bwr')
        cbar = plt.colorbar(ContourTemp)
        cbar.ax.tick_params(labelsize=20)  # カラーバーのフォントサイズを設定
        cbar.set_ticks(np.arange(cbar.vmin, cbar.vmax + 0.5, 0.5))  # 0.5刻みでカラーバーの数値を設定

        if add_axis_labels:
            # カラーバーのラベルを設定
            cbar.set_label(r'\textit{T}', fontsize=27, rotation=0)
            # カラーバーのラベルの位置を微調整
            cbar.ax.yaxis.set_label_coords(4.6, 0.53)

        ax.quiver(-Y_half, Z_half, -wm_half[i], vm_half[i], scale=0.4)

        # ファイルを指定されたディレクトリと形式で保存
        plt.savefig(os.path.join(output_dir, f"msflow_{plot_file_num}.{output_format}"), bbox_inches='tight', format=output_format)
        plt.close()
    plot_end_time = time.time()
    print(f"Plotting time for steps {start} to {end}: {plot_end_time - plot_start_time:.2f} seconds")
