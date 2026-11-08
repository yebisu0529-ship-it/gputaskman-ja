# gputaskman 日本語版（非公式）

[shanselman/gputaskman](https://github.com/shanselman/gputaskman)（v0.3.3）の画面表示を日本語にした、非公式のローカライズです。
ライセンスは元のプロジェクトと同じMITで、著作権表示（Copyright (c) 2026 Scott Hanselman）は[LICENSE](LICENSE)にそのまま残しています。
変えたのは表示する文言だけで、収集の仕組みと数値の扱いは元のままです。機能や仕組みの説明は、元の[README.md](README.md)（英語）を参照してください。

## インストール

[uv](https://docs.astral.sh/uv/)が必要です。PyPIの`gputaskman`は元の英語版なので、日本語版はこのリポジトリから入れます。

```powershell
uv tool install git+https://github.com/yebisu0529-ship-it/gputaskman-ja@i18n-ja
```

英語版と日本語版はパッケージ名が同じ`gputaskman`なので、同時には入れられません。英語版を入れている場合は、先に`uv tool uninstall gputaskman`を実行します。
インストールせずに1回だけ試すときは、`uvx --from git+https://github.com/yebisu0529-ship-it/gputaskman-ja@i18n-ja gputaskman`を実行します。

## 使い方

```powershell
gputaskman                  # TUI
gputaskman --once           # テキストで1回だけ出力
gputaskman --json           # JSON を1回だけ出力（常に英語）
gputaskman diff before.json after.json   # 2つの --json を比較
gputaskman --lang en        # 英語で表示
```

ソースから動かすときは、リポジトリを取得して`uv run`を使います。Python 3.11以上が必要です。

```powershell
git clone https://github.com/yebisu0529-ship-it/gputaskman-ja.git
cd gputaskman-ja
uv sync --locked
uv run --locked gputaskman
```

TUIのキーは元のままです。`↑/↓`で選択、`s`で並べ替え、`c`でグラフ、`a`ですべて/上位、`p`で一時停止、`?`で説明、`q`で終了します。

## 表示言語

`--lang {auto,en,ja}`で表示言語を選びます。既定は`auto`で、次の順に決めます。

1. 環境変数`GPUTASKMAN_LANG`（`auto`、`en`、`ja`）。`en`か`ja`なら、それに従います。
2. `LC_ALL`、`LC_MESSAGES`、`LANG`のうち、最初に空でないもの。`ja`で始まれば日本語、それ以外は英語です。
3. Windowsの表示言語。日本語なら日本語です。
4. どれにも当てはまらなければ英語です。

`--lang`を指定すると、環境変数より優先されます。ずっと日本語にしたいときは、環境変数を設定します。

```powershell
setx GPUTASKMAN_LANG ja
```

`--json`と`diff --json`は、`--lang`や`GPUTASKMAN_LANG`にかかわらず英語で出力します。スクリプトや他のツールが読む形式を変えないためです。
`--once`と`diff`のテキストは日本語になります。

## 既知の制限

- 1文字のショートカット（`q`、`s`、`c`、`a`、`p`、`?`）は、IMEをオフ（半角英数）にしないと効きません。
- `--help`の説明、argparseの`usage:`や`options:`、Textual組み込みのコマンドパレット（Ctrl+P）の中身は、英語のままです。
- 曖昧幅の文字（バーの`█` `░`や`■`など）を全角で描く端末では、バーの位置がずれます。元のプロジェクトと同じ制限です。
- `--once`をファイルやパイプに出すと、日本語Windowsではcp932で書き出されます。訳文はcp932で表せる文字だけを使っています。UTF-8で受け取るときは、`PYTHONUTF8=1`を設定します。
- ヘルプ画面（`?`）の表は、120桁より狭い端末では、セルの末尾が「…」で切れることがあります。全文はセルにマウスを置くと表示されます。
- インスペクターの長い説明文は空白の位置でしか折り返されないため、「5.73 GB」の数値と単位の間など、区切りの悪い位置で改行されることがあります。表示に使っているRichの折り返しの仕様です。
- プロセス名、ランタイム名、エンジン名（3d、compute、copy、videoなど）、OllamaやLM Studioが返すモデル名、ログの内容は、そのまま表示します。

## 用語

この表示では、数値や分類がどの根拠から来たかを、次の言葉で区別します。日本語にしても、確かさは元の英語より強くしていません。

| 英語 | 日本語 | 意味 |
|---|---|---|
| measured | 実測 | OSやドライバーのカウンターが返した値 |
| inferred | 推測 | 実測値と状況から導いた値。`*`は成り立つ説明が1つだけの場合、`?`は順序などによる推測 |
| estimated, est. | 推定 | モデルのヘッダーや起動引数などから計算した値 |
| runtime-reported | ランタイム報告 | llama.cppなどのログやAPIが報告した値 |
| heuristic | ヒューリスティック | ファイル名やフォルダー名からの手がかり。実際の種類や常駐は確認していない |
| confirmed | 確認済み | `api`か`mapped`を含む2つ以上の根拠がそろった状態 |
| unproven | 未確認 | 候補はあるが、ロードされているかは確認していない |
| evidence | 根拠 | モデルをどう特定したか（`api`、`mapped`、`cmdline`、`installed`） |
| unattributed | 未帰属 | どのプロセスにも割り当てられていない分 |
| unknown | 不明 | 取得できなかった値。0ではない |
| Spill | 共有RAM | GPUからアクセスできるシステムRAM。あふれた分とは限らない |
| Paged | 非常駐 | `max(Total Committed - Local Usage - Non Local Usage, 0)`による推定。退避の実測ではない |

## 開発メモ

- 訳文は`src/gputaskman/locale_ja.py`にあります。キーは、ソースにある英語の文字列そのものです。
- `tests/test_i18n.py`が、訳文の不足、古くなったキー、プレースホルダーの不一致、cp932で表せない文字を検出します。元の英語を編集すると、このテストが該当する文字列を示します。
- テストは`uv run --locked python -m unittest discover -s tests -q`で実行します。日本語のWindowsでもそのまま通ります。英語の出力を確かめるテストは、自分で`GPUTASKMAN_LANG=en`を指定しています。
