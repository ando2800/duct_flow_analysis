# ダクト流れログ抽出パイプライン（Duct Flow Log Extraction Pipeline）

このドキュメントは、ダクト流れシミュレーションから生成されたログファイルを解析し、HDF5形式で統計量を保存するためのコードに関する実装内容・想定・将来的な改善点についてまとめたものです。

---

## 概要

このパイプラインは、ダクト流れの数値計算によって出力されるログファイル（例：`screanoutput1-1`, `screanoutput1-2`）から重要な定数や統計量（`I`, `Ssum`など）を抽出し、各エピソード（例：ep001）ごとに HDF5 ファイルに保存します。

---

## 主な構成

### 1. `log_extract.py`

* 含まれる関数：

  * `extract_constants_from_log`: `CMASSFLOW`, `h`, `nstep`, `nhist`, `dt`, `Re` などの物理定数を抽出
  * `extract_statistics_from_log`: `ENER` 行から `Sn`, `Sw`, `Ss`, `Se` を抽出
  * `convert_log_to_hdf5`: 定数と統計量を組み合わせてHDF5へ保存するエントリ関数

### 2. `run_extract.py`

* 実行用スクリプト

  * 対象のエピソード番号やログファイルのパスを指定
  * 対応するログファイル（例：`screanoutput1-*`）を自動的に検出
  * 出力先 `data/processed/epXXX/` を自動生成
  * 各ログファイルを `.h5` に変換し保存

---

## 出力仕様

* HDF5構造：

  * `/statistics/Sn`, `/Sw`, `/Ss`, `/Se`
  * `/new_statistics/Indicator`, `/new_statistics/Ssum`
  * `/time_nondim`
  * `/config/CMASSFLOW`, `/dt`, `/Re` など定数

---

## 動作要件

* Python バージョン：3.8以上
* 必須ライブラリ：

  * `pandas >= 1.1`
  * `numpy >= 1.19`
* 注意：

  * `grep` および `awk` を `subprocess` 経由で呼び出すため、**Unix系シェル環境（macOS, Linux）専用**。Windows では非対応（WSL推奨）

---

## 想定・前提

* 入力ログファイル名は `screanoutput{episode}-{index}` の形式であること
* ディレクトリ構成は `data/raw/`（入力）、`data/processed/epXXX/`（出力）
* ログ形式は一定である（定数や`ENER`行の書式が変わらない）
* 各定数（例：CMASSFLOW, dt）はログ内に1回だけ登場する

---

## 今後の改良候補

* [ ] 複数エピソードを一括処理できるようにする
* [ ] `ENER` 行が欠損していた場合のエラーハンドリング強化
* [ ] HDF5保存時の圧縮オプション（例：`zlib`）対応
* [ ] 他の物理量（例：DIVERGENCE, SLIP-VELOCITY）への拡張
* [ ] コマンドラインツール化（`argparse`導入）
* [ ] ログ解析のロバスト性強化（正規表現での柔軟抽出など）

---

## ライセンス・利用について

このコードは研究用途および内部解析を目的として設計されています。再利用・論文等での利用時には出典を明記してください。
