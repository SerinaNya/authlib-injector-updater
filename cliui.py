# 许可: GNU General Public License v3

from colorama import init, Fore, Back, Style

__author__ = 'SkEy'
__all__ = ['Fore', 'Back', 'Style', 'UIPrinter']

class _InternalColors:
	'''
	内部颜色组
	'''
	CAPTION = Style.RESET_ALL + Fore.LIGHTBLACK_EX
	PRINT = Style.NORMAL
	NOTE = Fore.LIGHTBLUE_EX
	WAIT = Fore.LIGHTBLACK_EX
	SUCC = Fore.LIGHTGREEN_EX
	WARN = Fore.BLACK + Back.YELLOW
	FAIL = Fore.LIGHTWHITE_EX + Back.RED
	ASK = Fore.WHITE + Back.BLUE
	CONFIRM = Fore.LIGHTRED_EX + Back.YELLOW
	NO = Fore.LIGHTWHITE_EX + Back.LIGHTBLACK_EX
	END = Style.RESET_ALL

COLORAMA_INITED = False

class UIPrinter(_InternalColors):
	'''
	基础用户交互接口
	'''
	def __init__(self, name):
		global COLORAMA_INITED
		if not COLORAMA_INITED:
			init()
			COLORAMA_INITED = True
		self.cprint = lambda prompt, msg, no_new_line = False: print(prompt + f'{self.CAPTION} {name}{self.END}:' , msg, end = '' if no_new_line else None)
	def print(self, msg):
		'''一般消息'''
		self.cprint(f'{self.PRINT}[ ]', msg)
	def note(self, msg):
		'''提示'''
		self.cprint(f'{self.NOTE}[*]', msg)
	def wait(self, msg):
		'''请稍候'''
		self.cprint(f'{self.WAIT}[.]', msg)
	def succ(self, msg):
		'''成功'''
		self.cprint(f'{self.SUCC}[+]', msg)
	def warn(self, msg):
		'''警告'''
		self.cprint(f'{self.WARN}[!]', msg)
	def fail(self, msg):
		'''错误'''
		self.cprint(f'{self.FAIL}[-]', msg)
	def ask(self, msg):
		'''一般询问'''
		self.cprint(f'{self.ASK}[?]', msg, no_new_line=True)
	def no(self, msg):
		'''操作未完成'''
		self.cprint(f'{self.NO}[=]', msg)
	def confirm(self, msg):
		'''确认询问'''
		self.cprint(f'{self.CONFIRM}[?]', msg, no_new_line=True)