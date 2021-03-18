# -*- coding: utf-8 -*-

"""
    利用利用极大极小搜索实现的五子棋AI —— 加分规则设置及边界处理
    @author: WangZhanJie

"""

import re

black = [[0 for a in range(15)] for b in range(15)]
white = [[0 for a in range(15)] for b in range(15)]
flag = [[0 for a in range(15)] for b in range(15)]

# 连5 - 100000
pattern_5 = [re.compile(r'11111')]
# 活4 - 10000
pattern_alive_4 = [re.compile(r'011110')]
# 冲4 - 8000
pattern_to_4 = [re.compile(r'11011'), re.compile(r'011112'), re.compile(r'10111'), re.compile(r'201111')]
# 双活三 - 5000
pattern_double_alive_3 = [re.compile(r'0011100'), re.compile(r'2011100')]    # 边缘多加了0，避免误判
# 无对方棋在边缘的活3 - 1000
pattern_alive_sleep_3 = [re.compile(r'0011102')]
# 活三 - 200
pattern_alive_3 = [re.compile(r'010110')]
# 双活二 - 100
pattern_double_alive_2 = [re.compile(r'001100'), re.compile(r'001102'), re.compile(r'001012')]
# 眠3 - 50
pattern_sleep_3 = [re.compile(r'001112'), re.compile(r'010112'), re.compile(r'011012'), re.compile(r'10011'), re.compile(r'10101'), re.compile(r'2011102')]
# 无对方棋在边缘的活2 - 10
pattern_alive_sleep_2 = [re.compile(r'0010100'), re.compile(r'00100100')]
# 活2 - 5
pattern_alive_2 = [re.compile(r'201010'), re.compile(r'2010010'),  re.compile(r'20100102'),  re.compile(r'2010102')]
# 眠2 - 3
pattern_sleep_2 = [re.compile(r'000112'), re.compile(r'001012'), re.compile(r'010012'), re.compile(r'10001'), re.compile(r'2010102'), re.compile(r'2011002')]    # 要保证不陷入死4
# 死4 - (-5) 
pattern_dead_4 = [re.compile(r'2\d{3}12'), re.compile(r'2\d{2}1\d{2}2')]
# 死3 - (-5) 
pattern_dead_3 = [re.compile(r'2\d{2}12')]
# 死2 - (-5) 
pattern_dead_2 = [re.compile(r'2\d12')]

all_patterns = [pattern_5, pattern_alive_4, pattern_to_4, pattern_double_alive_3, pattern_alive_sleep_3, pattern_alive_3
                , pattern_double_alive_2, pattern_sleep_3, pattern_alive_sleep_2, pattern_alive_2, pattern_sleep_2, pattern_dead_4,
                pattern_dead_3, pattern_dead_2]

all_scores = [100000, 10000, 8000, 5000, 1000, 200, 100, 50, 10, 5, 3, -5, -5, -5]

board_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
                [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
                [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
                [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

search_range = []