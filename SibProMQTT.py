#!/usr/bin/env python
from datetime import datetime
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
#from Crypto.Random import random
from base64 import b64decode
from base64 import b64encode

class SibProMQTT:
    # key = AES key in the form of string 
    # iv = AES iv (initial vector) in the form of string 
	# htype = hash type ("SHA1", "SHA256", "SHA384", "SHA512", "MD5"
    # enctype = AES encryption mode "MODE_ECB" / "MODE_CBC"
	def __init__(self, key, iv, htype, enctype):
		self.skey = key
		self.iv = iv
		self.shtype = htype
		self.date = str(datetime.now().timestamp())
		#self.nonce = random.getrandbits(64)
		self.xA = key # by default, unless it is defined below
		self.sep = "|.-"
		self.deltaT = 3.00
	
#	def genNonce(self):
#		self.nonce = random.getrandbits(64)

	def genDate(self):
		self.date = datetime.now().timestamp()	

	def hash_xa(self, msg_str):
		hv = ""
		if self.shtype == "SHA1":
			mh = hashlib.sha1(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "SHA256":
			mh = hashlib.sha256(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "SHA384":
			mh = hashlib.sha384(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "SHA512":
			mh = hashlib.sha512(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "MD5":
			mh = hashlib.md5(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		# only taking the first 16 bytes as the key
		hv = hv[:16]
		return hv

	def hash(self, msg_str):
		hv = ""
		if self.shtype == "SHA1":
			mh = hashlib.sha1(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "SHA256":
			mh = hashlib.sha256(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "SHA384":
			mh = hashlib.sha384(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "SHA512":
			mh = hashlib.sha512(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		elif self.shtype == "MD5":
			mh = hashlib.md5(msg_str.encode()).digest()
			hv = b64encode(mh).decode('utf-8')
		return hv
    
    
	def calc_xA_pub(self):
		dt = self.date
		hdt = str(dt)
		self.xA = self.hash_xa(hdt+self.skey)
        
    
	def calc_xA_subs(self, time):
		self.xA = self.hash_xa(time+self.skey)

	def encrypt_c1(self,msg_str):
		cipher = AES.new(self.xA.encode(), AES.MODE_CBC, self.iv.encode())
		ct_bytes = cipher.encrypt(pad(msg_str.encode(), AES.block_size))
		ct = b64encode(ct_bytes).decode('utf-8')
		return ct
    
	def encrypt_c2(self,msg_str):
		cipher = AES.new(self.skey.encode(), AES.MODE_CBC, self.iv.encode())
		ct_bytes = cipher.encrypt(pad(msg_str.encode(), AES.block_size))
		ct = b64encode(ct_bytes).decode('utf-8')
		return ct

	def decrypt_c1(self, xA, ciphertext):
		mess = ""
		ct = b64decode(ciphertext)
		cipher = AES.new(xA.encode(), AES.MODE_CBC, self.iv.encode())
		pt = unpad(cipher.decrypt(ct), AES.block_size)
		return pt

	def decrypt_c2(self, ciphertext):
		xA_st = ""
		ct = b64decode(ciphertext)
		cipher = AES.new(self.skey.encode(), AES.MODE_CBC, self.iv.encode())
		pt = unpad(cipher.decrypt(ct), AES.block_size)
		xA_st = pt.decode()
		return xA_st
        
	def execute_publish(self, msg_str):
		# Gen TS1 --> done in init
		# calculate XA
		self.calc_xA_pub()
		#calculate C1
		c1 = self.encrypt_c1(msg_str)
		#calculate C2
		c2 = self.encrypt_c2(self.xA)
		out = c1 + self.sep + c2 + self.sep + self.date
		return out
        
	def execute_subscribe(self, msg_str):
		out = ""
		xA_st = ""
		# Gen TS2 --> done in init
		# Check if deltaT > TS2 - TS1
		inp = msg_str.split(self.sep)
		if self.deltaT > (float(self.date) - float(inp[2])):
			xA_st = self.decrypt_c2(inp[1])
			#print("xA_st = ", xA_st)
			self.calc_xA_subs(inp[2])
			#print("self.xA = ", self.xA)
			if xA_st == self.xA :
				out = self.decrypt_c1(xA_st, inp[0])
				#print("out = ", out)
			else :
				print("xAs are not same")
		else :
			print("delay is bigger than ", self.deltaT)
		if out == "":
			return out
		else:
			return out.decode()
    
    

		


		