"""
習慣機能の業務ロジックを管理するサービス層。

ViewからDB操作や判定ロジックを分離し、
画面処理をシンプルに保つために使用する。
"""

from habits.models import Habit, HabitLog, HabitSkip

class HabitService:

    @staticmethod
    def is_scheduled_for(habit, target_date):

        if target_date < habit.start_date:
            return False
        
        if habit.end_date and target_date > habit.end_date:
            return False
        
        if HabitSkip.objects.filter(
            habit=habit,
            date=target_date
        ).exists():
            return False
        
        # 毎日
        if habit.frequency == "daily":
            return True
        
        # 〇日おき
        if habit.frequency == "interval":

            if not habit.interval_days:
                return False

            delta_days = (
                target_date - habit.start_date
            ).days

            return delta_days % habit.interval_days == 0
        
        # 曜日指定
        if habit.frequency == "weekday":

            if not habit.weekdays:
                return False

            return (
                target_date.weekday()
                in habit.weekdays
            )
        
        # 回数指定
        if habit.frequency == "count":
            return True
        
        return False
    
    # 実施記録
    @staticmethod
    def complete(habit, target_date):

        HabitLog.objects.get_or_create(
            habit=habit,
            date=target_date
        )

    # 実施記録取消
    @staticmethod
    def uncomplete(habit, target_date):

        HabitLog.objects.filter(
            habit=habit,
            date=target_date
        ).delete()

    # スキップ記録
    @staticmethod
    def skip(habit, target_date):

        HabitSkip.objects.get_or_create(
            habit=habit,
            date=target_date
        )

        HabitLog.objects.filter(
            habit=habit,
            date=target_date
        ).delete()

    # スキップ取消
    @staticmethod
    def unskip(habit, target_date):

        HabitSkip.objects.filter(
            habit=habit,
            date=target_date
        ).delete()

    # 完了済み習慣ID取得
    @staticmethod
    def get_done_habit_ids(target_date):

        return set(
            HabitLog.objects.filter(
                date=target_date
            ).values_list(
                "habit_id",
                flat=True
            )
        )
    
    # スキップ済み習慣ID取得
    @staticmethod
    def get_skipped_habit_ids(target_date):

        return set(
            HabitSkip.objects.filter(
                date=target_date
            ).values_list(
                "habit_id",
                flat=True
            )
        )
    
    # その日に予定されている習慣一覧
    @staticmethod
    def get_scheduled_habits(target_date):

            habits = Habit.objects.filter(
                status="active"
            )

            return [
                habit
                for habit in habits
                if HabitService.is_scheduled_for(
                    habit,
                    target_date
                )
            ]
    
    # 実行状態付き習慣一覧
    @staticmethod
    def get_habit_states(target_date):

        scheduled_habits = (
            HabitService.get_scheduled_habits(
                target_date
            )
        )

        done_ids = (
            HabitService.get_done_habit_ids(
                target_date
            )
        )

        skipped_ids = (
            HabitService.get_skipped_habit_ids(
                target_date
            )
        )

        habit_states = []

        for habit in scheduled_habits:

            if habit.id in done_ids:
                state = "done"

            if habit.id in skipped_ids:
                state = "skipped"

            else:
                state = "todo"

            habit_states.append({
                "habit": habit,
                "state": state,
            })

        return habit_states