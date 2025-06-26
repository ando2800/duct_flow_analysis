# exp01 データ解析・可視化

- 4つ渦の指標と渦度の総和の時系列データの奇跡図を作成
- 卒論で得られた軌跡図の右下にある部分を取り出して正しいかその部分を拡大した軌跡図を作る

## 手順
1. 学習済み強化学習モデルのDDPG_s400_v1.2_evalのductのlogデータをgoyaからとってくる
2. logデータからENERデータを取り出してI(5行目)とSsum(6行目)を計算して時系列データとして作る
3. 条件指定して特定の時間帯の時系列データだけ取り出す
4. 軌跡図をplot

## ディレクトリ構成

- `plot_trajectry.py`  
  軌跡データを読み込み、SsumとIの関係をプロットします。開始点・終了点を強調表示し、PDF形式で保存します

- `fetch_raw.py`  
  データファイルから条件を満たす行を抽出

- `gen_tsd.py`
  ダクトのlogデータからI, S_sumの時系列データを作成

- `data/raw`
  生データ, ductのlogデータを格納 
  pathはgoyaの中にあるDDPG_s400_v1.2_evalにあるactor

- `data/processed/`  
  時系列データを格納

- `results/`  
  解析結果の図やファイルを保存


> **Note** 
> - logデータのファイル名 screanoutput1-** **の部分はセグメントに対応

## memo
- nhist data は1つのscreanoutput(1セグメント)につき141個
- fields data は1つのセグメントあたり7個 -> nimg=380~500はおよそ55~72セグメントに対応(7x55=385, 7x72=504)

## 3D流れデータの可視化方法
1. `$ cd ./data/raw/fields/paraview`
2. `$ paraview` でparaviewを起動
3. paraviewを開いて左上のファイルをクリックしてxdmfファイルを選択
