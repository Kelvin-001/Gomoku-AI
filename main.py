# -*- coding: utf-8 -*-
"""
    利用利用极大极小搜索实现的五子棋AI —— 主界面
    Created on Thu Jun 2 11:25:10 2020
    @author: WangZhanJie

"""

import multiprocessing
from tkinter import messagebox
from tkinter import *
from chessAI import *
from pp_chessAI import *
win_times = 0

if __name__ == '__main__':
	top = Tk()
	top.title("五子棋游戏")
	top.iconbitmap('logo.ico')
	def play(mod, option):
		global win_times
		confirm = messagebox.askokcancel('确认窗口', '确认开始' + mod + '模式 ' + option +' 是否开始对战？')
		if confirm:
			if mod == '单机':
				p = multiprocessing.Process(target=pp_main, args=(mod, option))
				p.start()
			else:
				p = multiprocessing.Process(target=Run_chess, args=(mod, option))
				p.start()
		else:
			return
    
    #绘制按钮和按钮上的文字
	Button(top, text="玩家对战 [单机]", fg="black", width=28, command=lambda: play('单机', '')).pack()
	Button(top, text="人机 [困难]", fg="black",  width=28, command=lambda: play('困难', 'HM')).pack()
	Button(top, text="机器 [困难]", fg="black", width=28, command=lambda: play('困难', 'MM')).pack()
	Button(top, text="辅助 [困难]", fg="black", width=28, command=lambda: play('困难', 'HMM')).pack()
	Button(top, text="人机 [简单]", fg="black",  width=28, command=lambda: play('简单', 'HM')).pack()
	Button(top, text="机器 [简单]", fg="black", width=28, command=lambda: play('简单', 'MM')).pack()
	Button(top, text="辅助 [简单]", fg="black", width=28, command=lambda: play('简单', 'HMM')).pack()
	Button(top, text="人机 [突破防线]", fg="black", width=28, command=lambda: play('突破防线', 'HM')).pack()
	Button(top, text="机器 [突破防线]", fg="black", width=28, command=lambda: play('突破防线', 'MM')).pack()

	top.mainloop()
