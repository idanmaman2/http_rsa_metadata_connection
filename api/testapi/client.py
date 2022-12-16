
import requests
import rsa 
import base64
import json 
from  Crypto.Hash import MD5 
server = "http://127.0.0.1:5000"
password ="mypass"
con = "123"


md5 = MD5.new()
md5.update(bytes(password,encoding="ascii"))
hashedpass = md5.hexdigest() 
responecreate = requests.get(server+f"/create/{con}",params={"password":hashedpass} ).text
print(responecreate)



respone = requests.get(server+f"/join/publickeyserver/{con}",params={} ).json() 
print(respone)






public_key,private_key = rsa.newkeys(1024)

name = "idan"
public_key_str = base64.b64encode(public_key.save_pkcs1())
#password
id = respone["id"]
public_key_server = rsa.PublicKey.load_pkcs1(base64.b64decode(respone['pk']))

encr= {
    "public_key": public_key_str, 
    "name":base64.b64encode(rsa.encrypt(bytes(name,encoding="ascii"),pub_key=public_key_server)).decode(encoding="ascii"), 
    "id" : id , 
    "password" :base64.b64encode(rsa.encrypt(bytes(password,encoding="ascii"),pub_key=public_key_server)).decode(encoding="ascii") 
} 



respone = (requests.post(server+f"/join/final/{con}",data=encr).content)

print("*"*30)
print(respone)
data_block= json.loads(rsa.decrypt(respone,priv_key=private_key).decode(encoding="ascii"))
print(data_block)
print(data_block["con_id"])
print(data_block["name"])