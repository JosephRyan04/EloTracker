from typing import List
from application.Models.Stat import Stat
from application.Models.Transaction import Transaction
from application.Models.User import User


def format_cc(connect_code):
    return str(connect_code).replace('-', '#').upper()

def calculate_stats(transactions: List[Transaction], user: User) -> Stat:
    loss = 0
    last_loss = 0
    cur_streak = 0
    max_streak = 0
    for rank in transactions:

        if rank.LossCount > loss:
            loss = rank.LossCount
            last_loss = rank.UpdateCount
            cur_streak = 0

        elif rank.LossCount == loss:
            cur_streak = rank.UpdateCount - last_loss
            max_streak = max(max_streak, cur_streak)

    return Stat(user_id=transactions[0].user_id,
                MaxStreak=max_streak,
                CurrentStreak=cur_streak
                )