import time
import memory
import register
import ULA
import device
from mvnutils import *
from switchcase import *

'''
This is the class for the MVN, it contains one memory 
(0x0000-0x0FFF), 7 registers (MDR, MAR, IC, IR, OP, OI, AC), 
1 ULA and a list of devices
It also contains methods to fetch, decode and execute instructions
on the memory, return the registers, set and show memory, set, 
remove and show devices
'''

class MVN:

	'''Inicialize MVN contents (memory, registers, ULA and device 
	list) and set the default devices'''
	'''NUM represents the number of steps to be done before 
	executing the Time Interruption (subroutine calling 0x000)'''
	def __init__(self, timeInterrupt=False, time_limit=50, timeout_input=0, line_feed="\n", quiet=False):
		self.mem=memory.memory()
		self.MAR=register.register()
		self.MDR=register.register()
		self.IC=register.register()
		self.IR=register.register()
		self.OP=register.register()
		self.OI=register.register()
		self.AC=register.register()
		self.SP=0x0ffe
		self.end=True
		self.timeInterrupt=timeInterrupt
		self.NUM=time_limit
		self.TIMEOUT=timeout_input
		self.line_feed=line_feed
		self.quiet=quiet
		self.nsteps=0
		self.ula=ULA.ULA()
		self.devs=[]
		self.devs.append(device.device(0,0, self.quiet))
		self.devs.append(device.device(1,0, self.quiet, line_feed=self.line_feed))

		# key:		instruction in code
		# value:	original instruction
		self.instru_translator={0x0: 0x0,
								0x1: 0x1,
								0x2: 0x2,
								0x3: 0x3,
								0x4: 0x4,
								0x5: 0x5,
								0x6: 0x6,
								0x7: 0x7,
								0x8: 0x8,
								0x9: 0x9,
								0xa: 0xa,
								0xb: 0xb,
								0xc: 0xc,
								0xd: 0xd,
								0xe: 0xe,
								0xf: 0xf}

	'''Set current address and get instruction from memory
	MAR:=IC
	MDR:=mem(MAR)'''
	def fetch(self):
		self.MAR.set_value(self.IC.get_value())
		self.get_mem()

	'''Separate instruction in operation+argument
	IR:=MDR
	OP:=first nibble of IR
	OI:=rest of IR'''
	def decode(self):
		if self.nsteps==self.NUM and self.timeInterrupt:
			self.IR.set_value(0xA000)
			self.nsteps=0
		else:
			self.IR.set_value(self.MDR.get_value())
		self.OP.set_value(self.IR.get_value()//0x1000)
		self.OI.set_value(self.IR.get_value()-0x1000*self.OP.get_value())
		self.nsteps+=1

	'''Make different actions dependind on OP and return False if OP is 
	Halt Machine.
	If OP is logic or arithmetic calls ULA to do it'''
	def execute(self):
		switch(self.instru_translator[self.OP.get_value()])
		if case(0):
			return self.jp()
		elif case(1) or case(2):
			if self.ula.execute(self.instru_translator[self.OP.get_value()], 
								self.AC.get_value()):
				self.IC.set_value(self.OI.get_value())
			else:
				self.IC.set_value(self.IC.get_value()+2)
			return True
		elif case(3):
			return self.lv()
		elif case(4) or case(5) or case(6) or case(7):
			self.MAR.set_value(self.OI.get_value())
			self.get_mem()
			self.AC.set_value(self.ula.execute(self.instru_translator[self.OP.get_value()], 
												self.AC.get_value(), 
												self.MDR.get_value()))
			self.IC.set_value(self.IC.get_value()+2)
			return True
		elif case(8):
			return self.ld()
		elif case(9):
			return self.mm()
		elif case(10):
			return self.sc()
		elif case(11):
			return self.rs()
		elif case(12):
			return self.hm()
		elif case(13):
			return self.gd()
		elif case(14):
			return self.pd()
		elif case(15):
			return self.os()

	'''Makes the common cycle: fetch, decode, execute and return weather
	 the code should continue or not'''
	def step(self):
		self.fetch()
		self.decode()
		return self.execute()

	#Return the addr's value
	def get_mem(self):
		self.MDR.set_value(self.mem.get_value(self.MAR.get_value()))

	#Set memory value
	def set_mem(self):
		self.mem.set_value(self.MAR.get_value(), self.MDR.get_value())

	#IC:=OI
	def jp(self):
		self.IC.set_value(self.OI.get_value())
		return True

	'''AC:=OI
	IC:=IC+1'''
	def lv(self):
		self.AC.set_value(self.OI.get_value())
		self.IC.set_value(self.IC.get_value()+2)
		return True

	'''MAR:=OI
	MDR:=mem(MAR)
	AC:=MDR
	IC:=IC+1'''
	def ld(self):
		if self.timeInterrupt and self.IC.get_value()>=0x100 and self.OI.get_value()<0x100:
			raise MVNError("Tentativa de acesso à área reservada por instrução externa")
		self.MAR.set_value(self.OI.get_value())
		self.get_mem()
		self.AC.set_value(self.MDR.get_value())
		self.IC.set_value(self.IC.get_value()+2)
		return True

	'''MAR:=OI
	MDR:=AC
	mem(MAR):=MDR
	IC:=IC+1'''
	def mm(self):
		if self.timeInterrupt and self.IC.get_value()>=0x100 and self.OI.get_value()<0x100:
			raise MVNError("Tentativa de acesso à área reservada por instrução externa")
		self.MAR.set_value(self.OI.get_value())
		self.MDR.set_value(self.AC.get_value())
		self.set_mem()
		self.IC.set_value(self.IC.get_value()+2)
		return True

	'''MAR:=OI
	MDR:=IC+1
	mem(MAR):=MDR
	IC:=OI+1'''
	def sc(self):
		self.MAR.set_value(self.OI.get_value())
		self.MDR.set_value(self.IC.get_value()+2)
		self.set_mem()
		self.IC.set_value(self.OI.get_value()+2)
		return True

	'''MAR:=OI
	MDR:=mem(MAR)
	IC:=MDR'''
	def rs(self):
		self.MAR.set_value(self.OI.get_value())
		self.get_mem()
		self.IC.set_value(self.MDR.get_value())
		return True

	#Only returns False, end of the program
	def hm(self):
		if self.end:return False
		self.end=True
		self.IC.set_value(self.ret)
		return True

	'''AC:=dev
	IC:=IC+1'''
	def gd(self):
		nfound=True
		for dev in self.devs:
			if self.OI.get_value()//0x0100==dev.get_type() and self.OI.get_value()%0x0100==dev.get_UC():
				self.AC.set_value(dev.get_data(self.TIMEOUT))
				nfound=False
		if nfound: raise MVNError("Dispositivo não existe")
		self.IC.set_value(self.IC.get_value()+2)
		return True	

	'''dev:=AC
	IC:=IC+1'''
	def pd(self):
		nfound=0
		for dev in self.devs:
			if self.OI.get_value()//0x0100==dev.get_type() and self.OI.get_value()%0x0100==dev.get_UC():
				dev.put_data(self.AC.get_value())
				nfound+=1
		if nfound==len(self.devs):
			raise MVNError("Dispositivo não existe")
		self.IC.set_value(self.IC.get_value()+2)
		return True

	'''Send OI to the supervisor
	IC:=IC+1'''
	def os(self):
		if self.OI.get_value()%0x100==0xEE:
			switch(self.AC.get_value())
			if case(0):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("OK")
			elif case(1):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("ER:JOB")
			elif case(2):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("ER:CMD")
			elif case(3):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("ER:ARG")
			elif case(4):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("ER:END")
			elif case(5):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("ER:EXE")
			elif case(2319):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("2319! Temos um 2319!")
			elif case(404):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("404! Erro não encontrado.")
			elif case(66):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("Execute o erro 66!")
			elif case(88):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("Cuidado amigo!!! Indo rápido desse jeito você pode acabar viajando no tempo")
			elif case(42):
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("Também fiquei triste com a resposta do Pensador Profundo. Tomara que a Terra já esteja terminando seu trabalho.")
			elif case(2001):
				if self.OI.get_value()!=0: self.os_error(0,self.OI.get_value()//0x100)
				print("Desculpe Dave, estou com medo e não posso fazer isso.")
			elif self.quiet:
				print("Erro desconhecido. Código "+str(self.OI.get_value()//0x100))
		elif self.OI.get_value()%0x100==0xEF:
			self.ret=self.IC.get_value()+2
			self.IC.set_value(self.AC.get_value()-2)
			self.end=False
		elif self.OI.get_value()%0x100==0x57:
			switch(self.AC.get_value())
			if case(0):
				#Get pointer
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				self.MAR.set_value(self.SP)
				self.get_mem()
				self.AC.set_value(self.MDR.get_value())
			elif case(1):
				#Set pointer
				if self.OI.get_value()//0x100!=1: self.os_error(1,self.OI.get_value()//0x100)
				self.MAR.set_value(self.MAR.get_value()-2)
				self.get_mem()
				self.MAR.set_value(self.SP)
				self.set_mem()
			elif case(2):
				#Get stacktop
				if self.OI.get_value()//0x100!=0: self.os_error(0,self.OI.get_value()//0x100)
				self.MAR.set_value(self.SP)
				self.get_mem()
				self.MAR.set_value(self.MDR.get_value())
				self.get_mem()
				self.AC.set_value(self.MDR.get_value())
			elif case(3):
				#Set stacktop
				if self.OI.get_value()//0x100!=1: self.os_error(1,self.OI.get_value()//0x100)
				self.MAR.set_value(self.MAR.get_value()-2)
				self.get_mem()
				self.AC.set_value(self.MDR.get_value())
				self.MAR.set_value(self.SP)
				self.get_mem()
				self.MAR.set_value(self.MDR.get_value())
				self.MDR.set_value(self.AC.get_value())
				self.set_mem()		
			elif self.quiet:
				print("Instrução desconhecida. Código "+str(self.AC.get_value()//0x100))
		elif self.OI.get_value()%0x100==0x01:
			self.MAR.set_value(self.MAR.get_value()-2)
			self.get_mem()
			switch(self.AC.get_value())
			if case(0):
				if self.OI.get_value()//0x100!=1: self.os_error(1, self.OI.get_value()//0x100)
				self.AC.set_value(self.ula.execute(0xA, self.MDR.get_value()))#NOT
			else:
				if self.OI.get_value()//0x100!=2: self.os_error(2, self.OI.get_value()//0x100)
				self.AC.set_value(self.MDR.get_value())
				self.MAR.set_value(self.MAR.get_value()-2)
				self.get_mem()
				if case(1):
					self.AC.set_value(self.ula.execute(0xB , self.AC.get_value(), self.MDR.get_value()))#AND
				elif case(2):
					self.AC.set_value(self.ula.execute(0xC , self.AC.get_value(), self.MDR.get_value()))#OR
				elif case(3):
					self.AC.set_value(self.ula.execute(0xD , self.AC.get_value(), self.MDR.get_value()))#XOR
				elif self.quiet:
					print("Operador desconhecido. Código "+str(self.AC.get_value()))
		elif self.OI.get_value()%0x100==0x0D:
			if self.OI.get_value()//0x100!=1: self.os_error(1, self.get_value()//0x100)
			self.MAR.set_value(self.MAR.get_value()-2)
			self.get_mem()
			nfound=True
			for dev in self.devs:
				if self.MDR.get_value()//0x0100==dev.get_type() and self.MDR.get_value()%0x0100==dev.get_UC():
					nfound=False
					break
			if nfound: raise MVNError("Dispositivo não existe")
			switch(self.AC.get_value())
			if case(0):
				dev.clean_buffer()
			elif case(1):
				dev.append_buffer()
			elif self.quiet:
				print("Operador desconhecido. Código "+str(self.AC.get_value()))
		elif self.OI.get_value()%0x100==0x71:
			if self.OI.get_value()//0x100!=0: self.os_error(0, self.get_value()//0x100)
			time.sleep(self.AC.get_value()/1000)
		elif self.quiet:
			print("Operação desconhecida. Código "+str(self.OI.get_value()%0x100))
		self.IC.set_value(self.IC.get_value()+2)
		return True

	def os_error(self, expected, passed):
		raise MVNError(str(expected)+" arguments expecteds, "+str(passed)+" passed.")

	def print_state(self):
		return hex(self.MAR.get_value())[2:].zfill(4)+" "+hex(self.MDR.get_value())[2:].zfill(4)+" "+hex(self.IC.get_value())[2:].zfill(4)+" "+hex(self.IR.get_value())[2:].zfill(4)+" "+hex(self.OP.get_value())[2:].zfill(4)+" "+hex(self.OI.get_value())[2:].zfill(4)+" "+hex(self.AC.get_value())[2:].zfill(4)

	'''Receives an list of lists containing pairs of addr-value and put 
	this to memory'''
	def set_memory(self, guide):
		for data in guide:
			self.mem.set_value(int(data[0], 16), int(data[1], 16))
	def dump_memory(self, start, stop, arq=None):
		self.mem.show(start, stop, arq)

	#Routine to add new device to device list
	def create_disp(self):
		file=open("disp.lst", "r")
		lines=file.read().split("\n")
		cont=0
		while cont < len(lines):
			if lines[cont]=="":
				lines.pop(cont)
				cont-=1
			cont+=1
		for line in lines:
			line=clean(line)
			switch(int(line[0]))
			if case(0):
				if len(line)!=2:
					raise MVNError("'disp.lst' file badly formulated")
				self.devs.append(device.device(0, int(line[1]), quiet=self.quiet))
			elif case(1):
				if len(line)!=2:
					raise MVNError("'disp.lst' file badly formulated")
				self.devs.append(device.device(1, int(line[1]), quiet=self.quiet, line_feed=self.line_feed))
			elif case(2):
				if len(line)!=3:
					raise MVNError("'disp.lst' file badly formulated")
				self.devs.append(device.device(2, int(line[1]), printer=line[2], quiet=self.quiet))
			elif case(3):
				if len(line)!=4:
					raise MVNError("'disp.lst' file badly formulated")
				self.devs.append(device.device(3, int(line[1]), line[2], line[3], quiet=self.quiet))

	#Print the devices on device list
	def print_devs(self):
		translate={"0":"Teclado", "1":"Monitor", "2":"Impressora", "3":"Disco"}
		for dev in self.devs:
			print("  "+str(dev.get_type())+"    "+str(dev.get_UC()).zfill(2)+"   "+translate[str(dev.get_type())])

	#Print options of device
	def show_available_devs(self):
		self.devs[0].show_available()

	#Add a new device with specified parameters
	def new_dev(self, dtype, UC, file=None, rwb=None, printer=None):
		for dev in self.devs:
			if dev.get_type()==dtype and dev.get_UC()==UC:
				raise MVNError("Device ja existe")
		self.devs.append(device.device(dtype, UC, file, rwb, printer, self.quiet))

	#Remove specified device
	def rm_dev(self, dtype, UC):
		for dev in range(len(self.devs)):
			if self.devs[dev].get_type()==dtype and self.devs[dev].get_UC()==UC:
				self.devs[dev].terminate()
				self.devs.pop(dev)
				return
