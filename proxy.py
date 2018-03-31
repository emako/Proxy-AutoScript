import sys
import subprocess
import win32event, pywintypes, win32api
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from icon import *

class Ui_Proxy(QWidget):
	def setupUi(self, Proxy):
		app.aboutToQuit.connect(self.exit)
		global mainWindow
		self.mainWindow = mainWindow
		Proxy.setObjectName("Proxy")
		Proxy.setWindowModality(QtCore.Qt.WindowModal)
		Proxy.resize(266, 279)
		Proxy.setMinimumSize(QSize(266, 279))
		Proxy.setMaximumSize(QSize(266, 279))
		self.proxylabel = QLabel(Proxy)
		self.proxylabel.setGeometry(QtCore.QRect(20, 30, 221, 16))
		self.proxylabel.setAlignment(QtCore.Qt.AlignCenter)
		self.proxylabel.setObjectName("proxylabel")
		self.copyBt = QPushButton(Proxy)
		self.copyBt.setGeometry(QtCore.QRect(80, 120, 100, 30))
		self.copyBt.setObjectName("copyBt")
		self.copyBt.setEnabled(False)
		self.exitBt = QPushButton(Proxy)
		self.exitBt.setGeometry(QtCore.QRect(80, 170, 100, 30))
		self.exitBt.setObjectName("exitBt")
		self.minimizeBt = QPushButton(Proxy)
		self.minimizeBt.setGeometry(QtCore.QRect(80, 220, 100, 30))
		self.minimizeBt.setObjectName("minimizeBt")
		self.startBt = QPushButton(Proxy)
		self.startBt.setGeometry(QtCore.QRect(80, 70, 100, 30))
		self.startBt.setObjectName("startBt")
		self.retranslateUi(Proxy)
		QtCore.QMetaObject.connectSlotsByName(Proxy)
		self.tray = QSystemTrayIcon()
		self.minimizeBt.clicked.connect(self.resume)
		self.exitBt.clicked.connect(qApp.quit)
		self.startBt.clicked.connect(self.start)
		self.copyBt.clicked.connect(self.copy)
		self.crateTray()
		self.thread_flag = False
		self.tray_flag = True
		self.tray_timer = QTimer(self)
		self.tray_timer.timeout.connect(self.trayOperate)
		self.start()

	def exit(self):
		self.tray.hide()
		del self.tray
		qApp.quit()

	def crateTray(self):
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icona48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.tray.setIcon(icon)
		self.tray.activated.connect(self.iconClied)
		self.tray_menu = QMenu(QApplication.desktop())
		self.StartAction = QAction('Start', self, triggered=self.start)
		self.CopyAction = QAction('Copy', self, triggered=self.copy)
		self.RestoreAction = QAction('Resume', self, triggered=self.resume)
		self.QuitAction = QAction('Exit ', self, triggered=qApp.quit)
		self.tray_menu.addAction(self.StartAction)
		self.tray_menu.addAction(self.CopyAction)
		self.tray_menu.addAction(self.RestoreAction)
		self.tray_menu.addAction(self.QuitAction)
		self.tray.setContextMenu(self.tray_menu)
		self.tray.show()

	def resume(self):
		if self.mainWindow.isVisible():
			self.mainWindow.hide()
			self.RestoreAction.setText('Resume')
		else:
			self.mainWindow.show()
			self.RestoreAction.setText('Hide')

	def iconClied(self, reason):
		print('Tray icon clicked mode is {reason}.'.format(reason=str(reason)))
		if self.tray_flag != True:
			return
		if reason == 1:#singleClicked(right)
			pass
		elif reason == 2:#doubleClicked(left)
			if self.mainWindow.isVisible():
				self.mainWindow.hide()
				self.RestoreAction.setText('Resume')
			else:
				self.mainWindow.show()
				self.RestoreAction.setText('Hide')
			self.tray_flag = False
			self.tray_timer.start(500)
		elif reason == 3:#singleClicked(left)
			if self.mainWindow.isVisible():
				self.mainWindow.hide()
				self.RestoreAction.setText('Resume')
		elif reason == 4:#singleClicked(center)
			self.copy()

	def trayOperate(self):
		self.tray_flag = True
		self.tray_timer.stop()

	def start(self):
		if self.thread_flag == True:
			self.thread_flag = False
			self.startBt.setText('Start')
			self.StartAction.setText('Start')
			self.proxylabel.setText('Trun Off')
			self.copyBt.setEnabled(False)
			self.CopyAction.setEnabled(False)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(":/iconb48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.tray.setIcon(icon)
			self.abort()
		else:
			self.thread_flag = True
			self.startBt.setText('Abort')
			self.StartAction.setText('Abort')
			self.copyBt.setEnabled(True)
			self.CopyAction.setEnabled(True)
			self.icon = QtGui.QIcon()
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(":/icona48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.tray.setIcon(icon)
			self.proxylabel.setText('http://127.0.0.1')
			self.thread = StartThread()
			self.thread.start()

	def abort(self):
		print('Abort Server.')
		self.thread.kill()
		self.thread.exit()

	def retranslateUi(self, Proxy):
		_translate = QtCore.QCoreApplication.translate
		Proxy.setWindowTitle(_translate("Proxy", "Proxy"))
		self.proxylabel.setText(_translate("Proxy", "Trun Off"))
		self.copyBt.setText(_translate("Proxy", "Copy"))
		self.exitBt.setText(_translate("Proxy", "Exit"))
		self.minimizeBt.setText(_translate("Proxy", "Hide"))
		self.startBt.setText(_translate("Proxy", "Start"))

	def copy(self):
		self.clipboard = QApplication.clipboard()
		self.clipboard.setText('http://127.0.0.1')

class StartThread(QtCore.QThread):
	def __init__(self, parent=None):
		super(StartThread, self).__init__(parent)
		self.child = None

	def run(self):
		st = subprocess.STARTUPINFO
		st.dwFlags = subprocess.STARTF_USESHOWWINDOW
		st.wShowWindow = subprocess.SW_HIDE
		self.child = subprocess.Popen('node proxy.js', stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=st)
		while True:
			line = self.child.stdout.readline().decode('u8').strip('\n')
			if subprocess.Popen.poll(self.child) == 0:
				break
			if line == '':
				break
			print(line)

	def kill(self):
		self.child.kill()

def maxLen(keys):
	return (len(keys) - 1)

if __name__ == '__main__':
	ERROR_ALREADY_EXISTS = 183
	hmutex = win32event.CreateMutex(None, pywintypes.FALSE, 'ema_proxy_mutex') 
	if(win32api.GetLastError() == ERROR_ALREADY_EXISTS):
		exit()
	qApp.setStyle(QStyleFactory.keys()[maxLen(QStyleFactory.keys())])
	app = QApplication(sys.argv)
	global mainWindow
	mainWindow = QMainWindow()
	ui = Ui_Proxy()
	ui.setupUi(mainWindow)
	icon = QtGui.QIcon()
	icon.addPixmap(QtGui.QPixmap(":/icona48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	mainWindow.setWindowIcon(icon)
	#mainWindow.show()
	sys.exit(app.exec_())
	ui.exit()