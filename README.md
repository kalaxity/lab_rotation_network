# lab_rotation_network
ラボローテーションに際し作成したプログラムです．量子ネットワーク関連です．

Python用の量子ネットワークシミュレータ，SimQNを用いています．  
あまり用いられておらず（解説どころかサンプルコードも公式以外で見当たらない），プログラム作成に苦労したので，小さなプログラムですが公開します．

```
.
├── 1_operation_valification
│   ├── kansoku.py：観測により量子状態が変化することを確認
│   ├── motsure.py：量子もつれの動作を確認
│   └── quantum_teleportation_test.py：量子テレポーテーションの動作を確認
├── 2_simulation：量子ネットワークのシミュレーション関連
│   └── examine_key_deliver_success_rate.py：ノード間距離による鍵配送成功率の変化を測定
└─── README.md：このファイル 
```

## Ref.
- SimQNのGitHubリポジトリ：https://github.com/ertuil/SimQN
- 公式チュートリアル：https://ertuil.github.io/SimQN/tutorials.html
- 各種モジュールのマニュアルとソースコード：https://ertuil.github.io/SimQN/modules.html
