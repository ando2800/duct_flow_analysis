# Duct Flow Log Data Processing and Visualization

本プロジェクトは、流体計算コードから得られる `screanoutput*-*` ログファイルを解析・可視化するツール群です。以下の3つのスクリプトに分かれています。

## ファイル構成

- `run.py`  
  各エピソード（例: ep001）に対応した複数の `screanoutputX-Y` ログを処理して、HDF5 ファイルに変換します。

- `ductlogRL2hdf5.py`  
  上記 `run.py` から呼び出されるライブラリスクリプトで、ログ解析とHDF5保存を担当します。

- テスト用である。実際に使うときには`./lib/`の中にある`log2hdf5.py`をインポートしてください。

- `plot.py`  
  `run.py` で出力された HDF5 データを時系列的に結合して、必要な可視化を行います。プロット対象は選択可能。

## 実行方法

### 1. HDF5ファイルの生成（ログ解析）

```bash
python run.py
```

- `run.py` の中でエピソード番号や処理対象ディレクトリを手動指定できます。
- `./log/screanoutputX-Y` に対応し、`./data/processed/epXXX/` 以下にHDF5が出力されます。
- 出力ファイル名は `screanoutputX-Y.h5` に対応します。

### 2. プロットの実行

```bash
python plot.py
```

- 対象エピソード・データ範囲は `plot.py` 内の `main()` で指定。
- プロット対象は以下から選択可能：
  - Indicator (I)
  - Ssum
  - Trajectory (I vs Ssum)

- 出力先は `./results/combined_plots_epXXX/`

## 注意点

- 各 `screanoutputX-Y` に含まれる `time_nondim` は **0始まりではなく、dt始まり** です。
- 各ファイルの時系列は連続しているため、結合時には末尾の時間ステップを前のファイルの末尾に加算することで連続時間を再構成しています。
- `time_nondim` の補正には **時間ステップ幅 dt の使用は不要** です。

## 開発・動作要件

- Python 3.8 以降推奨
- 依存ライブラリ：
  - pandas
  - matplotlib
  - pathlib（標準ライブラリ）
  - os（標準ライブラリ）

## 今後の改良点（例）

- 引数によるエピソード・範囲指定（`argparse` 対応）
- ログファイルの自動検出と検証
- プロットの自動レイアウト調整
- HDF5へのメタデータ記録（dtやReなど）

## 出力例

```
data/
  processed/
    ep001/
      screanoutput1-1.h5
      screanoutput1-2.h5
results/
  ep1seg1-2/
    I_tsd.pdf
    Ssum_tsd.pdf
    trajectory_IvsSsum.pdf
```

## 補足

- 処理対象のログはすべて `./log/` 以下に格納しておく必要があります。
- 1つのエピソード内のファイルは `screanoutputX-Y` 形式で連番としてください。
