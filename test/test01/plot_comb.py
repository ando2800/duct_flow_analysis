# plot.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'Times New Roman'

def plot_I(df, outputdir):
    plt.figure()
    plt.plot(df["time_nondim"], df["I"], color='black')
    plt.xlim(0.0, max(df["time_nondim"]))
    plt.ylim(-1.0, 1.0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outputdir, "I_tsd.pdf"), bbox_inches='tight', format='pdf')

def plot_Ssum(df, outputdir):
    plt.figure()
    plt.plot(df["time_nondim"], df["Ssum"], color='black')
    plt.xlim(0.0, max(df["time_nondim"]))
    plt.ylim(0.0, 0.02)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outputdir, "Ssum_tsd.pdf"), bbox_inches='tight', format='pdf')

def plot_Si(df, outputdir):
    plt.figure()
    plt.plot(df["time_nondim"], df["Se"], label="Se", color='blue')
    plt.plot(df["time_nondim"], df["Sn"], label="Sn", color='orange')
    plt.plot(df["time_nondim"], df["Ss"], label="Ss", color='green')
    plt.plot(df["time_nondim"], df["Sw"], label="Sw", color='red')
    plt.xlim(0.0, max(df["time_nondim"]))
    plt.ylim(0.0, max(df["Se"].max(), df["Sn"].max(), df["Ss"].max(), df["Sw"].max()) * 1.01)
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outputdir, "Si_tsd.pdf"), bbox_inches='tight', format='pdf')

def plot_trajectory(df, outputdir):
    plt.figure(figsize=(6, 4))
    plt.plot(df["Ssum"], df["I"], color='black')
    plt.xticks([0.0, 0.005, 0.01, 0.015, 0.02], fontsize=10)
    plt.ylim(-1.0, 1.0)
    plt.xlim(0.0, 0.02)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outputdir, "trajectory_IvsSsum.pdf"), bbox_inches='tight', format='pdf')

def prepare_dataframe(hdf5_dir, episode, start_idx, end_idx):
    ep_tag = f"ep{episode:03d}"
    df_all = pd.DataFrame()
    cumulative_time = 0.0

    for idx in range(start_idx, end_idx + 1):
        filename = f"screanoutput{episode}-{idx}.h5"
        h5path = Path(hdf5_dir) / ep_tag / filename
        if not h5path.exists():
            print(f"[WARNING] Missing: {h5path}")
            continue

        I = pd.read_hdf(h5path, "/new_statistics/Indicator")
        Ssum = pd.read_hdf(h5path, "/new_statistics/Ssum")
        time = pd.read_hdf(h5path, "/time_nondim") + cumulative_time
        Se = pd.read_hdf(h5path, "/statistics/Se")
        Sn = pd.read_hdf(h5path, "/statistics/Sn")
        Ss = pd.read_hdf(h5path, "/statistics/Ss")
        Sw = pd.read_hdf(h5path, "/statistics/Sw")

        cumulative_time = time.iloc[-1]

        temp_df = pd.DataFrame({"I": I, "Ssum": Ssum, 
                                "time_nondim": time,
                                "Se": Se, "Sn": Sn,
                                "Ss": Ss, "Sw": Sw})
        df_all = pd.concat([df_all, temp_df], ignore_index=True)

    return df_all

# ========== Main Execution Block ========== #
if __name__ == "__main__":

    hdf5_dir = "./data/processed"
    episode = 1
    start_idx = 54
    end_idx = 66
    output_dir = f"./results/ep{episode:03d}seg{start_idx}-{end_idx}"

    df = prepare_dataframe(hdf5_dir, episode, start_idx, end_idx)

    if df.empty:
        print("[ERROR] No valid data to plot.")

    os.makedirs(output_dir, exist_ok=True)
    
    plot_I(df, output_dir)   
    plot_Ssum(df, output_dir)
    plot_Si(df, output_dir)
    plot_trajectory(df, output_dir)

    print(f"[MESSAGE] Selected plots have been saved to: {output_dir}")
# ========== End of Main Execution Block ========== #
