# -*- coding: utf-8 -*-
"""
    利用利用极大极小搜索实现的五子棋AI —— 人机/机器对战模式
    @author: WangZhanJie

"""

from graphics import *
import bonus_rules
import alpha_beta_pruning
import evaluation_function

p = [[0 for a in range(15)] for b in range(15)]
q = [[0 for a in range(15)] for b in range(15)]
w = ''
def Create_Board():
	global w
	for i in range(15):
		for j in range(15):
			p[i][j] = Point(i*30+30, j*30+30)
			p[i][j].draw(w)
	for r in range(15):
		Line(p[r][0], p[r][14]).draw(w)
		Line(p[0][r], p[14][r]).draw(w)
	center = Circle(p[7][7], 3)
	center.draw(w)
	center.setFill('black')

def human_vs_machine(cnt, mod):
	global w
	if cnt is None:  # 异常判断
		return
	if cnt % 2 == 0:
		human_flag = False
		while not human_flag:  # 异常处理
			try:
				p1 = w.getMouse()
				x1 = p1.getX()
				y1 = p1.getY()
			except:
				return
			for i in range(15):
				for j in range(15):
					sqrdis = ((x1 - p[i][j].getX()) ** 2 + (y1 - p[i][j].getY()) ** 2)
					if sqrdis <= 200 and bonus_rules.flag[i][j] == 0:
						bonus_rules.black[i][j] = 1
						q[i][j] = Circle(p[i][j], 10)
						q[i][j].draw(w)
						q[i][j].setFill('black')
						human_flag = True
						break
				if human_flag:
					break
	else:
		machine_pos = alpha_beta_pruning.alpha_beta_process(mod)
		if not machine_pos:
			Text(Point(240, 500), '机器对战已结束!').draw(w)
			return -1
		i = machine_pos[0]
		j = machine_pos[1]
		bonus_rules.white[i][j] = 1
		q[i][j] = Circle(p[i][j], 10)
		q[i][j].draw(w)
		q[i][j].setFill('white')
	cnt += 1
	bonus_rules.flag[i][j] = 1
	return cnt

def machine_vs_machine(cnt, mod):
	global w
	if cnt % 2 == 0:
		machine_pos = alpha_beta_pruning.alpha_beta_process(mod)
		if not machine_pos:
			Text(Point(240, 500), '机器对战已结束!').draw(w)
			return -1
		i = machine_pos[0]
		j = machine_pos[1]
		bonus_rules.black[i][j] = 1
		# cal_score('white', i, j)
		q[i][j] = Circle(p[i][j], 10)
		q[i][j].draw(w)
		q[i][j].setFill('black')
	else:
		machine_pos = alpha_beta_pruning.alpha_beta_process(mod)
		if not machine_pos:
			Text(Point(240, 500), '机器对战已结束!').draw(w)
			return -1
		i = machine_pos[0]
		j = machine_pos[1]
		bonus_rules.white[i][j] = 1
		q[i][j] = Circle(p[i][j], 10)
		q[i][j].draw(w)
		q[i][j].setFill('white')
	cnt += 1
	bonus_rules.flag[i][j] = 1
	return cnt

def human_with_machine_vs_machine(cnt, mod):
	global w
	if cnt % 2 == 0:
		human_flag = False
		machine_pos = alpha_beta_pruning.alpha_beta_process(mod)
		ii = machine_pos[0]
		jj = machine_pos[1]
		q[ii][jj] = Circle(p[ii][jj], 3)
		q[ii][jj].draw(w)
		q[ii][jj].setFill('black')
		Text(Point(240, 550), 'The black point is the current suggestion of the system.').draw(w)
		Text(Point(240, 570), 'The white point is the previous suggestion of the system.').draw(w)
		if not machine_pos:
			Text(Point(240, 500), '对战已结束!').draw(w)
			return -1
		while not human_flag:
			p1 = w.getMouse()
			x1 = p1.getX()
			y1 = p1.getY()
			for i in range(15):
				for j in range(15):
					sqrdis = ((x1 - p[i][j].getX()) ** 2 + (y1 - p[i][j].getY()) ** 2)
					if sqrdis <= 200 and bonus_rules.flag[i][j] == 0:
						q[ii][jj].setFill('white')
						bonus_rules.black[i][j] = 1
						q[i][j] = Circle(p[i][j], 10)
						q[i][j].draw(w)
						q[i][j].setFill('black')
						human_flag = True
						break
				if human_flag:
					break
	else:
		machine_pos = alpha_beta_pruning.alpha_beta_process(mod)
		if not machine_pos:
			Text(Point(240, 500), '对战已结束!').draw(w)
			return -1
		i = machine_pos[0]
		j = machine_pos[1]
		bonus_rules.white[i][j] = 1
		q[i][j] = Circle(p[i][j], 10)
		q[i][j].draw(w)
		q[i][j].setFill('white')
	cnt += 1
	bonus_rules.flag[i][j] = 1
	return cnt

def Check():
	for i in range(15):
		for j in range(11):
			if bonus_rules.black[i][j:j+5] == [1, 1, 1, 1, 1]:
				return 'black'
			elif bonus_rules.white[i][j:j+5] == [1, 1, 1, 1, 1]:
				return 'white'
	for i in range(15):
		for j in range(11):
			if bonus_rules.black[j][i] and bonus_rules.black[j+1][i] and bonus_rules.black[j+2][i] and bonus_rules.black[j+3][i] and bonus_rules.black[j+4][i]:
				return 'black'
			elif bonus_rules.white[j][i] and bonus_rules.white[j+1][i] and bonus_rules.white[j+2][i] and bonus_rules.white[j+3][i] and bonus_rules.white[j+4][i]:
				return 'white'
	for i in range(11):
		for j in range(11):
			if bonus_rules.black[i][j] and bonus_rules.black[i+1][j+1] and bonus_rules.black[i+2][j+2] and bonus_rules.black[i+3][j+3] and bonus_rules.black[i+4][j+4]:
				return 'black'
			elif bonus_rules.white[i][j] and bonus_rules.white[i+1][j+1] and bonus_rules.white[i+2][j+2] and bonus_rules.white[i+3][j+3] and bonus_rules.white[i+4][j+4]:
				return 'white'
	for i in range(11):
		for j in range(14):
			if bonus_rules.black[i][j] and bonus_rules.black[i+1][j-1] and bonus_rules.black[i+2][j-2] and bonus_rules.black[i+3][j-3] and bonus_rules.black[i+4][j-4]:
				return 'black'
			elif bonus_rules.white[i][j] and bonus_rules.white[i+1][j-1] and bonus_rules.white[i+2][j-2] and bonus_rules.white[i+3][j-3] and bonus_rules.white[i+4][j-4]:
				return 'white'

def Run_chess(mod, option):
	global w
	w = GraphWin(mod + option, 480, 600)
	Create_Board()
	cnt = 0
	bonus_rules.white[7][7] = 1
	q[7][7] = Circle(p[7][7], 10)
	q[7][7].draw(w)
	q[7][7].setFill('white')
	bonus_rules.flag[7][7] = 1
	while 1:
		if option == 'MM':
			cnt = machine_vs_machine(cnt, mod)
		elif option == 'HM':
			cnt = human_vs_machine(cnt, mod)
		elif option == 'HMM':
			cnt = human_with_machine_vs_machine(cnt, mod)
		Check()
		if cnt == -1:
			break
		if Check() == 'black':
			Text(Point(240, 500), 'Black wins').draw(w)
			break
		if Check() == 'white':
			Text(Point(240, 500), 'White wins').draw(w)
			break
	# 异常处理
	try:
		w.getMouse()
	except:
		pass