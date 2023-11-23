# 1. 概要

## 2. 目次

1. jsonの作り方

### 3.1 前提

- rootユーザーで"IAM ユーザーおよびロールによる請求情報へのアクセス"を有効化をしてから1日以上たっている。

- 3.4 "任意"を行う際は pythonが入っていて、vscodeでpython実行環境できる

### 3.2 LINE通知チャネル開設

LINE developerで通知用のチャネルAPIを作ること
ログイン　<https://developers.line.biz/ja/services/line-login/>
※Slackで送りたい人はSlackで実装変更も可

まずプロバイダを作成して、さらにチャネルを作成する

- プロバイダ作成 > プロバイダ詳細に入る
- チャネル設定 > 新規チャネル作成 > Messaging API > チャネル作成

### 3.3 "任意" .envファイル作成設定

チャネルの詳細に入ったら以下を取得して.example.envから
XXXの部分を埋めた状態のenv/local/.envを作成することが目標。

1. env/localフォルダを作成して　.envファイルを作成する
   1. フォルダ作って.example.envをコピーしてリネーム
2. LINE_USER_ID
   1. Messaging API設定よりQRコードを読み取り自分の携帯アカウントに友達追加
   2. 「チャネル基本設定」の下部に「あなたのユーザーID」から取得
3. LINE_CHANNEL_ACCESS_TOKEN
   1. 「Messaging API設定」の下部にチャネルアクセストークンを発行を押す

### 3.4 "任意" ローカルで疎通確認　python実行

仮想環境作成するか直接やるかはおまかせします
仮想環境バージョン

コマンドプロンプト

```cmd
cd C:\path\to\training_iac\notify_cost\source
code .
```

sourceファイルがワーキングディレクトリになるようにした後

```cmd
python -m venv venv
.\venv\Scripts\activate

python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
```

app/main.pyを開きF5で実行する。
