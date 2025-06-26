# Project Title 

## Purpose

強化学習を使ったductシミュレーションのlogデータから統計量を取り出してhdf5形式で保存する関数の作成

### Input
- `data/raw/output.log`　ダクトのlogテキストファイル

### Output
- `data/processed/statistics_tsd.h5`: HDF5 file containing time-series statistics
- `results/*.pdf`: Plots of I(t), S(t), and trajectory in phase space

### Key Parameters
- `CMASSFLOW`: 1.9278 (used to normalize velocity)
- `dt`: 0.02 (simulation time step)
- `nhist`: 10 (sampling interval)

### Execution Steps
1. Edit `config.yaml` as needed
2. Run `python run.py` to generate HDF5 data
3. Run `python plot.py` to generate plots

### Dependencies
- Python packages: numpy, pandas, matplotlib, PyYAML
- System tools: `grep`, `awk`

## Project Structure
```
$ sudo apt install tree
$ tree
```
```
test01
├── data/
│ ├── raw/ 
│ └── processed/ 
├── results/ 
└── README.md
```

## Requirements

## How to Run

1. Edit `config.yaml` to match your simulation parameters.
2. Run the main script:
3. Generate plots:

Output will be saved in the `results/` directory.

## Notes

## References

## Created on: __DATE__