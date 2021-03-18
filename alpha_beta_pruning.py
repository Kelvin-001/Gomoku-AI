# -*- coding: utf-8 -*-
"""
    利用利用极大极小搜索实现的五子棋AI —— 极大极小值alpha-beta剪枝搜索
    @author: WangZhanJie

"""

import evaluation_function
import bonus_rules
import copy

test = [[0 for i in range(15)] for j in range(15)]
a = [[0 for i in range(15)] for j in range(15)]
b = [[0 for i in range(15)] for j in range(15)]
best_b_sums = -1
best_w_sums = -1
best_b = []
best_w = []
black_used_pos = []
white_used_pos = []
max_b_score = -1000
max_w_score = -1000
best_b_pos = []
best_w_pos = []
best_pos = []
search_range = []
origin_color = ''
test_pos = []
def alpha_beta_process(mod):
	global search_range, best_pos
	search_range = shrink_range()
	best_pos = machine_thinking(mod)
	return best_pos

def alpha_beta(color, depth, alpha, beta):
	global test_pos, origin_color, rblack_used_pos, white_used_pos, max_score, best_pos, black_used_pos, white_used_pos, search_range, max_b_score, max_w_score, best_b_pos, best_w_pos
	if origin_color == '':
		origin_color = color
	if depth <= 0:
		if color == 'black':
			i0 = black_used_pos[-1][0]
			j0 = black_used_pos[-1][1]
			score = evaluation_function.cal_score('black', i0, j0)
			
		else:
			i0 = white_used_pos[-1][0]
			j0 = white_used_pos[-1][1]
			score = evaluation_function.cal_score('white', i0, j0)
			
	for i in range(15):
		for j in range(15):
			
			if bonus_rules.flag[i][j] == 0 and search_range[i][j] == 1:
				bonus_rules.flag[i][j] = 1
				search_range[i][j] = 0
				if color == 'black':
					bonus_rules.black[i][j] = 1
					black_used_pos.append((i, j))
				else:
					bonus_rules.white[i][j] = 1
					white_used_pos.append((i, j))
				if color == 'black':
					new_color = 'white'
				else:
					new_color = 'black'
				val = - alpha_beta(new_color, depth-1, -beta, - alpha)
				bonus_rules.flag[i][j] = 0
				search_range[i][j] = 1
				if color == 'black':
					black_used_pos.remove((i, j))
					bonus_rules.black[i][j] = 0
				else:
					white_used_pos.remove((i, j))
					bonus_rules.white[i][j] = 0
				if val >= beta:
					return beta
				if val > alpha:
					if color == origin_color and depth == 4:
						best_pos = (i, j)
					alpha = val
	return alpha

# 测试
def alpha_beta_test(color, depth, alpha, beta):
	global a, b, test, best, best_b_sums, best_w_sums, best_b, best_w
	if depth <= 0:
		sums = 0
		for i in range(15):
			for j in range(15):
				if color == 'black':
					if a[i][j] == 1:
						sums += bonus_rules.board_scores[i][j]
				else:
					if b[i][j] == 1:
						sums += bonus_rules.board_scores[i][j]
		if color == 'black':
			if sums > best_b_sums:
				best_b_sums = sums
				best_b = copy.deepcopy(a)
		else:
			if sums > best_w_sums:
				best_w_sums = sums
				best_w = copy.deepcopy(b)
		return sums
    
	for i in range(15):
		for j in range(15):
			if test[i][j] == 0:
				test[i][j] = 1
				if color == 'black' and not a[i][j] == 1:
					a[i][j] = 1
				else:
					b[i][j] = 1
				if color == 'white' and not b[i][j] == 1:
					new_color = 'black'
				else:
					new_color = 'white'
				val = - alpha_beta_test(new_color, depth-1, -beta, - alpha)
				test[i][j] = 0
				if color == 'black':
					a[i][j] = 0
				else:
					b[i][j] = 0
				if val >= beta:
					return beta
				if val > alpha:
					alpha = val
	return alpha


# 替代alpha-beta的剪枝操作，直接找'半径'为1的闭包
def shrink_range():
	cover_range = [[0 for i in range(15)] for j in range(15)]
	for i in range(15):
		for j in range(15):
			if bonus_rules.flag[i][j] == 1:
				for k in range(3):
					cover_range[max(0, i - 1)][min(14, j - 1 + k)] = 1
					cover_range[max(0, i)][min(14, j - 1 + k)] = 1
					cover_range[min(14, i + 1)][min(14, j - 1 + k)] = 1
	cnt = 0
	for i in range(15):
		for j in range(15):
			if bonus_rules.flag[i][j] == 1:
				cover_range[i][j] = 0
			if cover_range[i][j] == 1:
				cnt += 1
	return cover_range



# 用贪心思想再权衡各参数,比alpha-beta效果好
def machine_thinking(mod):
	global search_range
	black_max_score = -5
	white_max_score = -5
	w_best_pos = ''
	b_best_pos = ''
	for i in range(15):
		for j in range(15):
			if bonus_rules.flag[i][j] == 0 and search_range[i][j] == 1:
				bonus_rules.flag[i][j] = 1
				search_range[i][j] = 0
				bonus_rules.white[i][j] = 1
				if mod == '困难':
					white_score = evaluation_function.cal_score_wise('white', i, j)
				elif mod == '简单' or mod == '突破防线':
					white_score = evaluation_function.cal_score('white', i, j)
					pass
				bonus_rules.white[i][j] = 0
				bonus_rules.black[i][j] = 1
				if mod == '困难':
					black_score = evaluation_function.cal_score_wise('black', i, j)
				elif mod == '简单' or mod == '突破防线':
					black_score = evaluation_function.cal_score('black', i, j)
				else:
					pass
				bonus_rules.black[i][j] = 0
				bonus_rules.flag[i][j] = 0
				if black_score > black_max_score:
					black_max_score = black_score
					b_best_pos = (i, j)
                    
				if white_score > white_max_score:
					white_max_score = white_score
					w_best_pos = (i, j)

	# 防守
	if mod == '突破防线' and white_max_score >= 10000 and black_max_score <= white_max_score:
		return w_best_pos
	if mod == '突破防线' and black_max_score >= 1000:
		return b_best_pos
	if white_max_score > black_max_score or white_max_score >= 100000:
		return w_best_pos
	else:
		return b_best_pos


# 进攻
def machine_thinking_twice(mod):
	global search_range
	black_max_score = -5
	white_max_score = -5
	w_best_pos = ''
	b_best_pos = ''
	for i in range(15):
		for j in range(15):
			if bonus_rules.flag[i][j] == 0 and search_range[i][j] == 1:
				bonus_rules.flag[i][j] = 1
				search_range[i][j] = 0
				bonus_rules.white[i][j] = 1
				if mod == '困难':
					white_score = evaluation_function.cal_score_wise('white', i, j)
				elif mod == '简单':
					white_score = evaluation_function.cal_score('white', i, j)
				else:
					pass
				bonus_rules.white[i][j] = 0
				bonus_rules.black[i][j] = 1
				if mod == '困难':
					black_score = evaluation_function.cal_score_wise('black', i, j)
				elif mod == '简单':
					black_score = evaluation_function.cal_score('black', i, j)
				else:
					pass
				bonus_rules.black[i][j] = 0
				bonus_rules.flag[i][j] = 0
				if black_score > black_max_score:
					black_max_score = black_score
					b_best_pos = (i, j)

				if white_score > white_max_score:
					white_max_score = white_score
					w_best_pos = (i, j)

	if white_max_score >= 100000:
		return w_best_pos
	if black_max_score >= 8000:
		return b_best_pos
	if white_max_score > black_max_score:
		first_best = w_best_pos
		second_best = b_best_pos
	else:
		first_best = b_best_pos
		second_best = w_best_pos
	first_sums, first_best = twice_search(first_best, second_best, mod)
	second_sums, second_best = twice_search(second_best, first_best, mod)
	if first_sums < second_sums:
		first_best = second_best
	print(first_sums, second_sums)
	return first_best

def twice_search(first_best, second_best, mod):
	global search_range
	(w_11, w_12) = first_best
	one_score = evaluation_function.cal_score_wise('white', w_11, w_12)
	bonus_rules.white[w_11][w_12] = 1
	bonus_rules.flag[w_11][w_12] = 1

	search_range = shrink_range()
	(b_11, b_12) = machine_thinking(mod)
	one_b_score = evaluation_function.cal_score_wise('black', b_11, b_12)
	bonus_rules.black[b_11][b_12] = 1
	bonus_rules.flag[b_11][b_12] = 1

	search_range = shrink_range()
	(w_21, w_22) = machine_thinking(mod)
	two_score = evaluation_function.cal_score_wise('white', w_21, w_22)
	bonus_rules.white[w_21][w_22] = 1
	bonus_rules.flag[w_21][w_22] = 1

	search_range = shrink_range()
	(b_21, b_22) = machine_thinking(mod)
	two_b_score = evaluation_function.cal_score_wise('black', b_21, b_22)

	bonus_rules.white[w_11][w_12] = bonus_rules.white[w_21][w_22] = 0
	bonus_rules.flag[w_11][w_12] = bonus_rules.flag[w_21][w_22] = 0
	bonus_rules.black[b_11][b_12] = 0
	bonus_rules.flag[b_11][b_12] = 0

	w_sums = one_score + two_score
	b_sums = one_b_score + two_b_score
	if w_sums >= b_sums:
		return w_sums, first_best
	else:
		return b_sums, second_best