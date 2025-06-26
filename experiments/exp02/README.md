<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js">
</script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [['$', '$'] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>

# 一定加熱($Ri=0.02$)のダクトシミュレーション

## 前提（logファイル参照）
$$Re_b=1200, Ri=0.02, Pr=0.7$$
$$[Lx,Ly,Lz]/H=[4\pi,1,1]$$

## 目的
1. 強化学習で観測された高エネルギーの左右壁面4つ渦パターンが制御を行っていないときでも観測されるのかという問い
2. 臨界Re数において、$Ri=0.02$の時に2次流れは左右壁面４つ渦パターンとなるといことは既知のことであるので、一定加熱ではどれくらい4つ渦の指標が左右壁面4つ渦パターンをの域の状態を通過しているか？

## 方法
1. IとSsumの時系列プロット + state spaceの軌道図

## 結果・考察
1. tragectoryから一定加熱ではエネルギーの高い左右壁面４つ渦パターンは観測されない
2. 思っていたよりも4つ渦の指標が高い値で変動していた（と言っても0よりは小さな域で）、しかし０より大きくなることは比較的少なかったので、時間平均すると、統計的には左右壁面4つ渦パターンに偏っているのだろう