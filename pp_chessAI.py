# -*- coding: utf-8 -*-
"""
    利用利用极大极小搜索实现的五子棋AI —— 单机模式
    @author: WangZhanJie

"""

from graphics import *
import  bonus_rules

w = ''
p = [[0 for a in range(15)] for b in range(15)]
q = [[0 for a in range(15)] for b in range(15)]

def Create_Board():
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

def Click(cnt):
	human_flag = False
	while not human_flag:
		p1 = w.getMouse()
		x1 = p1.getX()
		y1 = p1.getY()
		for i in range(15):
			for j in range(15):
				sqrdis = ((x1 - p[i][j].getX()) ** 2 + (y1 - p[i][j].getY()) ** 2)
				if sqrdis <= 200 and bonus_rules.flag[i][j] == 0:
					if cnt % 2 == 0:
						bonus_rules.black[i][j] = 1
						q[i][j] = Circle(p[i][j], 10)
						q[i][j].draw(w)
						q[i][j].setFill('black')
						human_flag = True
					else:
						bonus_rules.white[i][j] = 1
						q[i][j] = Circle(p[i][j], 10)
						q[i][j].draw(w)
						q[i][j].setFill('white')
						human_flag = True
					cnt += 1
					bonus_rules.flag[i][j] = 1
					break
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


def pp_main(mod, option):
	global w
	w = GraphWin(mod, 480, 600)
	Create_Board()
	cnt = 0
	while 1:
		cnt = Click(cnt)
		Check()
		if Check() == 'black':
			Text(Point(240, 500), 'Black wins').draw(w)
			break
		if Check() == 'white':
			Text(Point(240, 500), 'White wins').draw(w)
			break
	w.getMouse()
