# Multi Agent Learning for Keras

## Kerasでマルチエージェントラーニング
マルチエージェントラーニングは、相互に影響を与え合うモデルが強調ないし、敵対して、目的となる報酬を最大化するシチュエーションのディープラーニングです[1][2]

強化学習の特殊系と捉えることができそです　　

Deep Mind社が提案したモデルの一部では非常に面白く、報酬の設定しだいでは協力したり敵対したりします。　　

この敵対的に学習を行うというのがGANだと考えているのですが、解析的なアプローチはアカデミアのみなさんが頑張っていることかと思います  

Kerasで敵対的な簡単なマルチエージェントラーニングを21言っちゃダメゲームで構築しました  

21言っちゃダメゲームを行います  
（これはQiitaのはむこさんの記事を参考にさせていただきました、ありがとうございます[3]）


## 参考文献
[1] [Understanding Agent Cooperation](https://deepmind.com/blog/understanding-agent-cooperation/)
[2] [Multi-agent Reinforcement Learning in Sequential Social Dilemmas](https://storage.googleapis.com/deepmind-media/papers/multi-agent-rl-in-ssd.pdf)
[3] [深層強化学習：「20言っちゃダメゲーム」の最適解を30分程度で自動的に編み出す（chainerRL）](http://qiita.com/hamko/items/119750780dc430760d78#_reference-4664ea066f5790a8570e)
