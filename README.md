# ![ヘッダー画像](/docs/img/header.svg)

本リポジトリは、ウェブサイト「週7英単語」の開発プロジェクトを管理するものです。

週7英単語のURL：https://shu7-eitango.com

# 背景

このプロジェクトおよびウェブサイトは、ウェブ開発技術（特にインフラ関連の技術）の学習の成果物として紹介することを意図しています。

実は、本プロダクトに先行して、高度な日本語語彙を身につけるための[週7日本語](https://javocabflushcards.com)というウェブサイトを開発していました。ただ、そのサイトは個人的な学習ニーズに特化しており、紹介には適していないと感じました。

そこで、よりたくさんの人々の需要にかなう英単語学習サイトとして、本プロダクトを改めて立ち上げました。このウェブサイトでは、目にすることが少ない英単語を毎日ピックアップしていて、英単語カードのように学習できるようになっています。これまで知らなかった英単語に出会い、新たな学びを得ることができる、発見型学習ウェブサイトとしてより多くのニーズに応えられるよう、本プロジェクトを開発しています。

# プレビュー

- トップ画面

    | PC |　モバイル |
    |:-----:|:-----:|
    | ![トップ画面（PC）](/docs/img/capture_index.pc.png) | ![トップ画面（モバイル）](/docs/img/capture_index.mobile.png) |

- 束（bunch）の画面

    | PC |　モバイル |
    |:-----:|:-----:|
    | ![束の画面（PC）](/docs/img/capture_bunch.pc.png) | ![束の画面（モバイル）](/docs/img/capture_bunch.mobile.png) |

- Grafanaのダッシュボード

    | PC |　モバイル |
    |:-----:|:-----:|
    | ![Grafanaダッシュボード（PC）](/docs/img/capture_gfdashboard.pc.png) | ![Grafanaのダッシュボード（モバイル）](/docs/img/capture_gfdashboard.mobile.png) |

# 使用技術

| Category          | Technology Stack               |
| ----------------- | ------------------------------ |
| Frontend          | Bootstrap                      |
| Backend           | Nginx, uWSGI, Flask, Python    |
| Infrastructure    | Amazon EC2, Cloudflare         |
| Database          | MySQL, Redis, Grafana Loki     |
| Monitoring        | Grafana                        |
| Environment setup | Docker Compose                 |
| CI/CD             | GitHub Actions                 |
| Design            | PowerPoint                     |
| etc.              | Promtail, Certbot, geoipupdate |

# システム構成図

![システム構成図](/docs/img/sysconf.svg)

# 今後の展望

インフラ、サーバサイドの改善を積極的に行おうと考えており、以下のことを目論んでいます。

- RDS、DynamoDBをVPCに追加し、Composeプロジェクトからデータベース部分を切り出すことで、システムの信頼性を高めてコストを抑える。

- CI/CDツールとしてCircleCIを導入し、テスト、デプロイを効率的に行う。

- インフラ技術の学習を兼ね、Kubernetesによるコンテナオーケストレーションを導入し、デプロイ、スケーリングをより効率的に行う。（金銭面を考慮して短期間のみ運用の予定）

- 今のデータベース設計は簡潔さに欠けており、オブジェクト指向に則っていないため、次のようなER図にしたがってデータベースを再構築する。
    <details>
    <summary>計画中のER図</summary>

    ![計画中のER図](/docs/img/erdiagram.svg)
    
    ※`category`は現在`pos`と呼んでいるものに対応。
    </details>

また、優先度は上記より低いものの、フロントエンドについても以下の改善を行うつもりです。
- 単語カードの表示について、現状のリスト形式ではなく、実際の暗記カードをイメージした、1枚1枚めくるような見た目にする。
