# タスクサンプルデータ自動生成プログラム
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
# あなたのアプリ名が「tasks」ではない場合は、下の「tasks」を書き換えてください
from tasks.models import Task 

class Command(BaseCommand):
    help = "無限スクロールのテスト用に、サンプルタスクを35件一括生成します"

    def handle(self, *args, **options):
        # 1. サンプルのタイトルと詳細のパーツ
        titles = [
            "プログラミングの学習", "部屋の掃除と片付け", "食材の買い出し", 
            "ジムで筋トレ", "読書（技術書）", "未返信メールの処理", 
            "ブログ記事の下書き", "散歩とリフレッシュ", "新しいレシピに挑戦", 
            "Djangoアプリのバグ修正", "家計簿の入力", "サプリメントの注文",
            "英語のリスニング", "ポートフォリオの作成", "定例ミーティングの準備"
        ]
        
        descriptions = [
            "公式ドキュメントを読みながら進める。", "15分タイマーをかけて集中してやる。",
            "今週の晩御飯の分をまとめて買う。", "スクワットとベンチプレスを中心に。",
            "気になった章を重点的にメモを取りながら読む。", "保留にしていた案件のレスポンス。",
            "アイディア出しから構成まで終わらせる。", "外の空気を吸ってリフレッシュする。",
            "YouTubeで見つけた美味しそうなパスタを作る。", "エラーログを解析して修正する。"
        ]

        statuses = ["todo", "doing", "done", "draft"]

        self.stdout.write("タスクを生成中...")

        # 2. ループを回して35件のデータをランダムに生成
        for i in range(1, 36):
            base_title = random.choice(titles)
            desc = random.choice(descriptions)
            status = random.choice(statuses)
            
            # 期限（今日から前後10日の間でランダムに設定）
            random_days = random.randint(-10, 10)
            due_date = date.today() + timedelta(days=random_days)

            # 完全にランダムだとつまらないので、完了済みのものは期限を過去にしやすいように調整
            if status == "done":
                due_date = date.today() - timedelta(days=random.randint(1, 5))

            # データベースに保存
            Task.objects.create(
                title=f"【テスト】{base_title} No.{i}",
                description=f"これは自動生成された{i}番目のテストタスクです。\n{desc}",
                status=status,
                due_date=due_date,
                link="https://google.com" if random.choice([True, False]) else ""
            )

        self.stdout.write(self.style.SUCCESS("成功！35件のサンプルタスクがデータベースに注入されました！"))