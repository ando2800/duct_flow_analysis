import numpy as np
import pandas as pd
from io import StringIO
import subprocess

def calc_I(sectors):
    Sn, Sw, Ss, Se = sectors
    total = Sn + Sw + Ss + Se
    if total == 0:
        return 0
    return (Sn + Ss - Sw - Se) / total

def calc_S(sectors, ub, h):
    Sn, Sw, Ss, Se = sectors
    return (Sn + Sw + Ss + Se) * ub / h

def ductlog2hdf5(inputfile, outputfile, config):
    print('[MESSAGE] Create time series data from historical log.')

    # 定数読み込み
    CMASSFLOW = config['CMASSFLOW']
    h = config['h']
    ub = CMASSFLOW / 4.0
    nstep = config['nstep']
    nhist = config['nhist']
    dt = config['dt']
    dt_nondim = dt * ub / h

    # 出力からENER行を抽出し、14-17列を読む
    grep = subprocess.Popen(["grep", "ENER", inputfile], stdout=subprocess.PIPE, text=True)
    awk = subprocess.Popen(["awk", "{print $14, $15, $16, $17}"],
                           stdin=grep.stdout, stdout=subprocess.PIPE, text=True)
    output, _ = awk.communicate()

    df = pd.read_csv(StringIO(output), sep=r'\s+', header=None)
    df.columns = ['Sn', 'Sw', 'Ss', 'Se']

    # 時間ベクトル作成
    df['time_nondim'] = dt_nondim + 10 * dt_nondim * np.arange(1 + (nstep - 1) // nhist)

    # 統計量計算
    df['I'] = df[['Sn', 'Sw', 'Ss', 'Se']].apply(lambda row: calc_I(row), axis=1)
    df['Ssum'] = df[['Sn', 'Sw', 'Ss', 'Se']].apply(lambda row: calc_S(row, ub, h), axis=1)

    # HDF5で保存
    with pd.HDFStore(outputfile, mode='w') as store:
        store.put('/statistics/Sn', df['Sn'])
        store.put('/statistics/Sw', df['Sw'])
        store.put('/statistics/Ss', df['Ss'])
        store.put('/statistics/Se', df['Se'])
        store.put('/new_statistics/Indicator', df['I'])
        store.put('/new_statistics/Ssum', df['Ssum'])
        store.put('/time_nondim', df['time_nondim'])

    print("[MESSAGE] Time series data saved to HDF5 format successfully!")
