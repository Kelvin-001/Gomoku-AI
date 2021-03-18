# -*- coding: utf-8 -*-

"""
    利用利用极大极小搜索实现的五子棋AI —— 评估函数实现
    @author: WangZhanJie
    
"""

import bonus_rules
import re    #导入正则

def cal_score(color, i, j):
	# 初边界处理
	pos_row = '2'
	pos_col = '2'
	bia_right = '2'
	bia_left = '2'
	for ii in range(15):
		if bonus_rules.black[i][ii] == 1:
			if color == 'black':
				pos_row += '1'
			else:
				pos_row += '2'
		elif bonus_rules.white[i][ii] == 1:
			if color == 'black':
				pos_row += '2'
			else:
				pos_row += '1'
		else:
			pos_row += '0'
	pos_row += '2'
	for ii in range(15):
		if bonus_rules.black[ii][j] == 1:
			if color == 'black':
				pos_col += '1'
			else:
				pos_col += '2'
		elif bonus_rules.white[ii][j] == 1:
			if color == 'black':
				pos_col += '2'
			else:
				pos_col += '1'
		else:
			pos_col += '0'
	pos_col += '2'
	# 保存两个斜线上组成的字符串中原下棋点的位置
	bia_left_pos = -1
	bia_right_pos = -1
	bia_left_pos_rev = -1
	bia_right_pos_rev = -1
	# 按列数递增遍历
	for ii in range(max(0, i-j), min(i+(14 - j) + 1, 15)):
		if bia_right_pos == -1 and ii == i:
			bia_right_pos = ii - max(0, i-j) 
			bia_right_pos_rev = min(i+(14 - j), 15) - 1 - bia_right_pos
		if bonus_rules.black[ii][ii + j - i] == 1:
			if color == 'black':
				bia_right += '1'
			else:
				bia_right += '2'
		elif bonus_rules.white[ii][ii + j - i] == 1:
			if color == 'black':
				bia_right += '2'
			else:
				bia_right += '1'
		else:
			bia_right += '0'
	# 末边界处理
	bia_right += '2'
	for ii in range(max(0, i-(14 - j)), min(i + j + 1, 15)): 
		if bia_left_pos == -1 and ii == i:
			bia_left_pos = ii - max(0, i-(14 - j))  
			bia_left_pos_rev = min(i + j + 1, 15) - 1 - bia_left_pos
		if bonus_rules.black[ii][j - (ii - i)] == 1:
			if color == 'black':
				bia_left += '1'
			else:
				bia_left += '2'
		elif bonus_rules.white[ii][j - (ii - i)] == 1:
			if color == 'black':
				bia_left += '2'
			else:
				bia_left += '1'
		else:
			bia_left += '0'
	bia_left += '2'
	search_flag = False
	rev_col = pos_col[::-1]
	rev_row = pos_row[::-1]
	rev_bia_left = bia_left[::-1]
	rev_bia_right = bia_right[::-1]
	score = 0
	# 加末边界处理后,要统一将下标都加1
	i += 1
	j += 1
	bia_left_pos += 1
	bia_right_pos += 1
	bia_left_pos_rev += 1
	bia_right_pos_rev += 1
	for patterns in bonus_rules.all_patterns:
		for p in patterns:
			result = re.search(p, pos_col)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_col)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, pos_row)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_row)
			if result:
				search_range = result.span()
				if (search_range[0] <= i <= search_range[1]) or (search_range[0] <= j <= search_range[1]):

					score = bonus_rules.all_scores[bonus_rules.all_patterns.index(patterns)]
					search_flag = True
					break
			# 处理两种斜线上的情况
			pos = -1
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, bia_left)
				if result: 
					pos = bia_left_pos
			if not result or not result.span()[0] <= pos <= result.span()[1]: 
				result = re.search(p, rev_bia_left)
				if result:
					pos = bia_left_pos_rev
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, bia_right)
				if result:
					pos = bia_right_pos
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, rev_bia_right)
				if result:
					pos = bia_right_pos_rev
			if result:
				search_range = result.span()
				if search_range[0] <= pos <= search_range[1]:
					score = bonus_rules.all_scores[bonus_rules.all_patterns.index(patterns)]
					search_flag = True
					break
		if search_flag:
			break

	return score + bonus_rules.board_scores[i-1][j-1]

def cal_score_wise(color, i, j):
	scores = []
	first_pattern = -1
	second_pattern = -1
	p_index = -1
	pos_row = '2'
	pos_col = '2'
	bia_right = '2'
	bia_left = '2'
	for ii in range(15):
		if bonus_rules.black[i][ii] == 1:
			if color == 'black':
				pos_row += '1'
			else:
				pos_row += '2'
		elif bonus_rules.white[i][ii] == 1:
			if color == 'black':
				pos_row += '2'
			else:
				pos_row += '1'
		else:
			pos_row += '0'
	pos_row += '2'
	for ii in range(15):
		if bonus_rules.black[ii][j] == 1:
			if color == 'black':
				pos_col += '1'
			else:
				pos_col += '2'
		elif bonus_rules.white[ii][j] == 1:
			if color == 'black':
				pos_col += '2'
			else:
				pos_col += '1'
		else:
			pos_col += '0'
	pos_col += '2'
	# 保存两个斜线上组成的字符串中原下棋点的位置
	bia_left_pos = -1
	bia_right_pos = -1
	bia_left_pos_rev = -1
	bia_right_pos_rev = -1
	# 按列数递增遍历
	for ii in range(max(0, i-j), min(i+(14 - j) + 1, 15)):
		if bia_right_pos == -1 and ii == i:
			bia_right_pos = ii - max(0, i-j)
			bia_right_pos_rev = min(i+(14 - j), 15) - 1 - bia_right_pos
		if bonus_rules.black[ii][ii + j - i] == 1:
			if color == 'black':
				bia_right += '1'
			else:
				bia_right += '2'
		elif bonus_rules.white[ii][ii + j - i] == 1:
			if color == 'black':
				bia_right += '2'
			else:
				bia_right += '1'
		else:
			bia_right += '0'
	# 加末边界处理
	bia_right += '2'
	for ii in range(max(0, i-(14 - j)), min(i + j + 1, 15)):
		if bia_left_pos == -1 and ii == i:
			bia_left_pos = ii - max(0, i-(14 - j))
			bia_left_pos_rev = min(i + j + 1, 15) - 1 - bia_left_pos
		if bonus_rules.black[ii][j - (ii - i)] == 1:
			if color == 'black':
				bia_left += '1'
			else:
				bia_left += '2'
		elif bonus_rules.white[ii][j - (ii - i)] == 1:
			if color == 'black':
				bia_left += '2'
			else:
				bia_left += '1'
		else:
			bia_left += '0'
	bia_left += '2'
	search_flag = False
	rev_col = pos_col[::-1]
	rev_row = pos_row[::-1]
	rev_bia_left = bia_left[::-1]
	rev_bia_right = bia_right[::-1]
	score = 0
	i += 1
	j += 1
	bia_left_pos += 1
	bia_right_pos += 1
	bia_left_pos_rev += 1
	bia_right_pos_rev += 1
	for patterns in bonus_rules.all_patterns:
		for p in patterns:
			result = re.search(p, pos_col)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_col)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, pos_row)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_row)
			if result:
				search_range = result.span()
				if (search_range[0] <= i <= search_range[1]) or (search_range[0] <= j <= search_range[1]):
					score = bonus_rules.all_scores[bonus_rules.all_patterns.index(patterns)]
					first_pattern = bonus_rules.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					search_flag = True
					break
			# 处理两种斜线上的情况
			pos = -1
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, bia_left)
				if result: 
					pos = bia_left_pos
			if not result or not result.span()[0] <= pos <= result.span()[1]: 
				result = re.search(p, rev_bia_left)
				if result:
					pos = bia_left_pos_rev
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, bia_right)
				if result:
					pos = bia_right_pos
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, rev_bia_right)
				if result:
					pos = bia_right_pos_rev
			if result:
				search_range = result.span()
				if search_range[0] <= pos <= search_range[1]:
					score = bonus_rules.all_scores[bonus_rules.all_patterns.index(patterns)]
					first_pattern = bonus_rules.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					search_flag = True
					break
		if search_flag:
			break

	search_flag = False
	for patterns in bonus_rules.all_patterns[first_pattern:]:
		for p in patterns:
			if patterns == bonus_rules.all_patterns[first_pattern]:
				if patterns.index(p) <= p_index:
					continue
			result = re.search(p, pos_col)
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_col)
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, pos_row)
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_row)
			if result:
				search_range = result.span()
				if (search_range[0] <= i <= search_range[1]) or (search_range[0] <= j <= search_range[1]):

					score = bonus_rules.all_scores[bonus_rules.all_patterns.index(patterns)]
					first_pattern = bonus_rules.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					search_flag = True
					break
			# 处理两种斜线上的情况
			pos = -1
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, bia_left)
				if result:  
					pos = bia_left_pos
			if not result or not result.span()[0] <= pos <= result.span()[1]:  
				result = re.search(p, rev_bia_left)
				if result:
					pos = bia_left_pos_rev
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, bia_right)
				if result:
					pos = bia_right_pos
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, rev_bia_right)
				if result:
					pos = bia_right_pos_rev
			if result:
				search_range = result.span()
				if search_range[0] <= pos <= search_range[1]:
					score = bonus_rules.all_scores[bonus_rules.all_patterns.index(patterns)]
					first_pattern = bonus_rules.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					search_flag = True
					break
		if search_flag:
			break
    
	if len(scores) == 2:
		score = sum(scores)
	elif len(scores) != 0:
		score = max(scores)
        
	return score + bonus_rules.board_scores[i-1][j-1]
