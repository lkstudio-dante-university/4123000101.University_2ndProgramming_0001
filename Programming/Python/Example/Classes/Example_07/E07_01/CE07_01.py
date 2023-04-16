import os
import sys

# Example 7 - 1
class CE07_01:
    # 실행한다
	@classmethod
	def Run(cls):
		CE07UserInfoStorage.GetInst().m_nNumGolds = 10
		CE07UserInfoStorage.GetInst().m_nNumEquipments = 20

		CE07UserInfoStorage.GetInst().SaveUserInfo()
		CE07UserInfoStorage.GetInst().LoadUserInfo()

		print("=====> 유저 정보 <=====")
		print("{0}, {1}".format(CE07UserInfoStorage.GetInst().m_nNumGolds, CE07UserInfoStorage.GetInst().m_nNumEquipments))
	

# 유저 정보 저장소
class CE07UserInfoStorage:
	m_oInst = None

	# 초기화
	def __init__(self):
		self.m_nNumGolds = 0
		self.m_nNumEquipments = 0

	# 유저 정보를 로드한다
	def LoadUserInfo(self):
		"""
		스트림이란?
		- 데이터를 입/출력 할 수 있는 통로를 의미한다. (즉, 스트림을 활용하면 파일을 대상으로 데이터를 입/출력하는 것이 가능하다.)

		스트림은 컴퓨터에서 동작하는 모든 프로그램이 사용하는 공통 자원이기 때문에 스트림이 더이상 필요 없을 경우에는 반드시 해당 스트림을
		제거해 줄 필요가 있다. (즉, 사용이 완료 된 스트림을 제거하지 않을 경우 불필요한 스트림이 생성된다는 것을 의미하며 이는 곧 컴퓨터 자원이
		고갈 되어 정작 필요 할 때 스트림을 생성 할 수 없는 문제가 발생 할 수 있다.)
		"""
		# 파일이 존재 할 경우
		if os.path.isfile("Example/Resources/Example_07/E07_01.txt"):
			"""
			open 메서드란?
			- 파일을 대상으로 데이터를 입/출력 할 수 있게 스트림을 생성해주는 역할을 수행하는 메서드이다. 따라서, 해당 메서드는 반환 값으로
			스트림을 반환해주며 해당 스트림을 통해 원하는 데이터를 파일로부터 입력 받거나 출력하는 것이 가능하다.

			또한, 스트림은 close 메서드를 제공하며 해당 메서드는 스트림을 제거하는 역할을 수행한다. (즉, 스트림이 더이상 필요 없을 경우에는
			반드시 close 메서드를 통해 해당 스트림을 제거해줘야한다.)

			with 키워드란?
			- Python 에서 스트림을 좀 더 안전하게 사용 할 수 있도록 제공하는 키워드로서 해당 키워드를 활용하면 특정 스트림을 제거하기 위해서
			명시적으로 close 메서드를 호출 할 필요가 없다. (즉, with 키워드 영역을 벗어나면 Python 인터프리터가 자동으로 close 메서드를
			호출해준다는 것을 알 수 있다.)

			따라서, 해당 키워드를 활용하면 사용이 완료 된 스크림에 close 메서드를 호출하지 않는 실수를 최소화하는 것이 가능하다.
			"""
			with open("Example/Resources/Example_07/E07_01.txt", "r") as oRStream:
				oTokenList = oRStream.readline().split(",")

				self.m_nNumGolds = int(oTokenList[0])
				self.m_nNumEquipments = int(oTokenList[1])

	# 유저 정보를 저장한다
	def SaveUserInfo(self):
		"""
		open 메서드는 출력용으로 스트림을 생성 할 경우 파일을 같이 생성해주는 역할도 수행한다. (즉, 입력용으로 스트림을 생성 할 경우 파일이
		없으면 예외가 발생한다.)

		단, open 메서드는 디렉토리는 생성해주지 않기 때문에 명시 된 파일 경로에 존재하지 않는 디렉토리가 명시되어 있을 경우 스트림 생성에
		실패한다. (즉, 반환 값으로 None 데이터가 반환된다는 것을 알 수 있다.)

		따라서, 스트림 생성을 시도하기 전에 디렉토리 존재 여부를 검사 후 디렉토리 존재 여부에 따라 해당 디렉토리를 생성해주는 명령문을
		작성해줘야한다. (즉, os.makedirs 메서드를 통해 디렉토리를 생성할 수 있다.)
		"""
		# 디렉토리가 없을 경우
		if not os.path.isdir("Example/Resources/Example_07"):
			os.makedirs("Example/Resources/Example_07")

		with open("Example/Resources/Example_07/E07_01.txt", "w") as oWStream:
			oWStream.write("{0},{1}".format(self.m_nNumGolds, self.m_nNumEquipments))

	# 인스턴스를 반환한다
	@classmethod
	def GetInst(cls):
		# 인스턴스가 없을 경우
		if cls.m_oInst == None:
			cls.m_oInst = CE07UserInfoStorage()
			
		return cls.m_oInst
	