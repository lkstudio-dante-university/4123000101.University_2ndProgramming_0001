import os
import sys
import math
import random

from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Example.Classes.Global.Manager.CTimeManager import *
from Example.Classes.Global.Manager.CInputManager import *


# Example 13
class CExample_13(QMainWindow, uic.loadUiType("Resources/Example_13/E13MainWindow.ui")[0]):
	# 생성자
	def __init__(self):
		# 멤버 변수를 설정한다
		self.m_fUpdateSkipTime = 0.0
		
		self.m_oPlayer = CE13Player()
		self.m_oBulletList = []
		
		super().__init__()
		self.__init__example_13__()
	
	# 초기화
	def __init__example_13__(self):
		self.show()
		self.setupUi(self)
		self.setWindowTitle("Example 13")
		
		# 영역을 설정한다
		nHeight = self.frameGeometry().height() - self.geometry().height()
		self.setGeometry(10, 10 + nHeight, self.geometry().width(), self.geometry().height())
		
		# 타이머를 설정한다
		self.m_oTimer = QTimer(self)
		self.m_oTimer.timeout.connect(self.OnUpdate)
		
		self.m_oTimer.start(1)
		
		# 메뉴 바를 설정한다
		self.menuBar().setNativeMenuBar(False)
		self.actionAbout.triggered.connect(self.OnClickAboutMenu)
		
		# 플레이어를 설정한다
		self.m_oPlayer.m_fSpeed = 250
		self.m_oPlayer.m_fRadius = 15.0
		
		self.m_oPlayer.m_oPos = QPointF(self.geometry().width() / 2.0, self.geometry().height() / 2.0)
	
	# 상태를 갱신한다
	def OnUpdate(self):
		self.update()
		self.m_fUpdateSkipTime += CTimeManager.GetInst().GetDeltaTime()
		
		# 일정 시간이 지났을 경우
		if self.m_fUpdateSkipTime >= 0.15:
			self.m_fUpdateSkipTime = 0.0
			
			nRandVal01 = random.randint(0, 1)
			nRandVal02 = random.randint(0, 1)
			
			oPos = QPointF(0.0, 0.0)
			oPos.setX(0.0 if nRandVal01 <= 0 else self.geometry().width())
			oPos.setY(0.0 if nRandVal02 <= 0 else self.geometry().height())
			
			oBullet = CE13Bullet()
			oBullet.m_fSpeed = 250.0
			oBullet.m_fRadius = 5.0
			
			oBullet.m_oPos = oPos
			oBullet.m_oDirection = self.m_oPlayer.m_oPos - oBullet.m_oPos
			
			self.m_oBulletList.append(oBullet)
		
		# 플레이어를 갱신한다
		self.m_oPlayer.Update()
		
		# 총알을 갱신한다
		for oBullet in self.m_oBulletList:
			oBullet.Update()
		
		# 관리자를 갱신한다
		CTimeManager.GetInst().Update()
		CInputManager.GetInst().Update()
		
		# 라벨을 갱신한다
		self.labelDeltaTime.setText("Delta Time: {0:0.5f} sec".format(CTimeManager.GetInst().GetDeltaTime()))
		self.labelRunningTime.setText("Running Time: {0:0.5f} sec".format(CTimeManager.GetInst().GetRunningTime()))
	
	# 그리기 이벤트를 수신했을 경우
	def paintEvent(self, a_oEvent: QPaintEvent):
		oPainter = QPainter(self)
		
		try:
			self.m_oPlayer.Draw(oPainter)
			
			for oBullet in self.m_oBulletList:
				oBullet.Draw(oPainter)
		
		finally:
			oPainter.end()
	
	# 닫기 이벤트를 수신했을 경우
	def closeEvent(self, a_oEvent: QCloseEvent):
		nResult = QMessageBox.question(self, "알림", "앱을 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		a_oEvent.accept() if nResult == QMessageBox.Yes else a_oEvent.ignore()
	
	# 키 눌림 이벤트를 수신했을 경우
	def keyPressEvent(self, a_oEvent: QKeyEvent):
		# Esc 키를 눌렀을 경우
		if a_oEvent.key() == Qt.Key_Escape:
			self.close()
		
		CInputManager.GetInst().AddKey(a_oEvent.key())
	
	# 키 눌림 종료 이벤트를 수신했을 경우
	def keyReleaseEvent(self, a_oEvent: QKeyEvent):
		CInputManager.GetInst().RemoveKey(a_oEvent.key())
	
	# 정보 메뉴를 눌렀을 경우
	def OnClickAboutMenu(self):
		QMessageBox.aboutQt(self, "알림")
	
	# 초기화
	@classmethod
	def Start(cls, args):
		oApp = QApplication(args)
		oExample = CExample_13()
		
		sys.exit(oApp.exec())


# 플레이어
class CE13Player:
	# 생성자
	def __init__(self):
		self.m_fSpeed = 0.0
		self.m_fRadius = 0.0
		
		self.m_oPos = QPointF(0.0, 0.0)
	
	# 상태를 갱신한다
	def Update(self):
		oDirection = QPointF(0.0, 0.0)
		
		# 위쪽/아래쪽 방향 키를 눌렀을 경우
		if CInputManager.GetInst().IsKeyDown(Qt.Key_Up) or CInputManager.GetInst().IsKeyDown(Qt.Key_Down):
			oDirection.setY(-1.0 if CInputManager.GetInst().IsKeyDown(Qt.Key_Up) else 1.0)
		
		# 왼쪽/오른쪽 방향 키를 눌렀을 경우
		if CInputManager.GetInst().IsKeyDown(Qt.Key_Left) or CInputManager.GetInst().IsKeyDown(Qt.Key_Right):
			oDirection.setX(-1.0 if CInputManager.GetInst().IsKeyDown(Qt.Key_Left) else 1.0)
		
		try:
			fLength = math.sqrt(math.pow(oDirection.x(), 2.0) + math.pow(oDirection.y(), 2.0))
			oDirection = QPointF(oDirection.x() / fLength, oDirection.y() / fLength)
			
			self.m_oPos += (oDirection * self.m_fSpeed) * CTimeManager.GetInst().GetDeltaTime()
		except Exception as oException:
			pass
	
	# 플레이어를 그린다
	def Draw(self, a_oPainter: QPainter):
		a_oPainter.drawEllipse(self.m_oPos, self.m_fRadius, self.m_fRadius)


# 총알
class CE13Bullet:
	# 생성자
	def __init__(self):
		self.m_fSpeed = 0.0
		self.m_fRadius = 0.0
		
		self.m_oPos = QPointF(0.0, 0.0)
		self.m_oDirection = QPointF(0.0, 0.0)
	
	# 상태를 갱신한다
	def Update(self):
		fLength = math.sqrt(math.pow(self.m_oDirection.x(), 2.0) + math.pow(self.m_oDirection.y(), 2.0))
		oDirection = QPointF(self.m_oDirection.x() / fLength, self.m_oDirection.y() / fLength)
		
		self.m_oPos += (oDirection * self.m_fSpeed) * CTimeManager.GetInst().GetDeltaTime()
	
	# 총알을 그린다
	def Draw(self, a_oPainter: QPainter):
		a_oPainter.setBrush(QBrush(QColor(255, 0, 0, 255)))
		a_oPainter.drawEllipse(self.m_oPos, self.m_fRadius, self.m_fRadius)
