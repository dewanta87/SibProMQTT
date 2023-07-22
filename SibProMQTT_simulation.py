from SibProMQTT import SibProMQTT as spmqtt
import time
from datetime import datetime
#import machine

#uart = machine.UART(2,115200)

mess50 = "abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|"
mess100 = "abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|"
mess150 = "abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|"
mess200 = "abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|abcdefghijklmnopqrstuvwx|"


key1 = "abc12@mymail.com"
key2 = "abc12@mymail-longadd.com"
key3 = "abcdefg123456@mymail-longadd.com"
hash_type = "SHA1"
REP = 1000
HASH = 3 #SHA1, SHA256, SHA384
avg_acc = 0

# Simulation parameters
key = key1
aes_iv = "bWRHdzkzVDFJbWNB"
MESS = mess100

print("Length of message = ", len(MESS))
for k in range (HASH) :
	if k==0:
		hash_type = "MD5"
	elif k==1:
		hash_type = "SHA256"
	elif k==2:
		hash_type = "SHA1"
	acc = 0
	avg_acc = 0
	for i in range (REP) :
		# publish
		start = datetime.now().timestamp()
		trans = spmqtt(key, aes_iv, hash_type, "AES-CBC")
		msg = trans.execute_publish(MESS)

		# delay to to check timestamp is working or not
		#time.sleep(4)

		# subscribe
		recv = spmqtt(key, aes_iv, hash_type, "AES-CBC")
		mess_rec = recv.execute_subscribe(msg)
		#print("mess = ", MESS)
		#print("mess_rec = ", mess_rec)
		end = datetime.now().timestamp() - start
		acc = acc + end
		start = 0.00
		end = 0.00
        
	avg_acc = acc/REP
	ustring = "average computation cost " + hash_type + " = " + str(avg_acc)
    #print("average computation cost ", hash_type, " = ", avg_acc)
	#uart.write(ustring)
	print(ustring)