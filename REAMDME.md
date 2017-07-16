# Multi Agent Learning for Keras

## Kerasでマルチエージェントラーニング
マルチエージェントラーニングは、相互に影響を与え合うモデルが強調ないし、敵対して、目的となる報酬を最大化するシチュエーションのディープラーニングです[1][2]

強化学習の特殊系と捉えることができそです　　

Deep Mind社が提案したモデルの一部では非常に面白く、報酬の設定しだいでは協力したり敵対したりします。　　

この敵対的に学習を行うというのがGANだと考えているのですが、解析的なアプローチはアカデミアのみなさんが頑張っていることかと思います  

Kerasで敵対的な簡単なマルチエージェントラーニングを21言っちゃダメゲームで構築しました  

21言っちゃダメゲームを行います  
（これはQiitaのはむこさんの記事を参考にさせていただきました、ありがとうございます[3]）

## 強化学習の理論
強化学習は、人間が特に正しい悪いなどを指定せずとも、なんらかの報酬系から報酬を得ることで報酬を最大化します  
このとき、ある系列の状態をSとし、その時の行動をaとし、この組み合わせで得られる報酬関数をQとすると、報酬箱のようになります。  
<p align="center">
  <img width="200px" src="https://user-images.githubusercontent.com/4949982/28245373-e7ef3be6-6a3f-11e7-8440-7307f7814321.png">
</p>

また報酬の割引率というものがあるらしく、行動が連続する系では、最終的に得られる特典が各選択に対してどの程度影響を及ぼしているのかわかりません  

（わからないので、今回は具体的に求めるということをしていません）  

今回の例では、Q関数を具体的にDeepLearningによる関数としています  

## ルール（問題設定）
1先手、後手に別れて0から最小１、最大の３つ増やした数字を言い合います  
数字を累積していって、21以上のになるように言った時点で負けです。相手に21以上を踏ませれば勝ちです  

## 

## 参考文献
[1] [Understanding Agent Cooperation](https://deepmind.com/blog/understanding-agent-cooperation/)
[2] [Multi-agent Reinforcement Learning in Sequential Social Dilemmas](https://storage.googleapis.com/deepmind-media/papers/multi-agent-rl-in-ssd.pdf)
[3] [深層強化学習：「20言っちゃダメゲーム」の最適解を30分程度で自動的に編み出す（chainerRL）](http://qiita.com/hamko/items/119750780dc430760d78#_reference-4664ea066f5790a8570e)
