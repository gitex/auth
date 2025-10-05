# import pytest
# import time_machine
#
# from src.utils import now_ts
#
#
# timestamps = (
#     1672531000,
#     1735675200,
# )
#
#
# @pytest.mark.parametrize("ts", timestamps)
# def test_now_ts_returns_correct_ts(ts: int) -> None:
#     with time_machine.travel(ts, tick=False):
#         assert now_ts() == ts
