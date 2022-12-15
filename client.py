
import requests
import rsa 
import pickle
import base64
import json 
public_key,private_key = rsa.newkeys(1024)
print(private_key,public_key,sep="\n"*3)

server = "http://127.0.0.1:5000"

respone = (requests.get(server+"/",params={"public_key":base64.b64encode(pickle.dumps(public_key))}).content)
data_block= json.loads(rsa.decrypt(respone,priv_key=private_key).decode(encoding="ascii"))
print(data_block)
print(data_block["size"])