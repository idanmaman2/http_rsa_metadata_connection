from flask import Flask, request
import rsa 
import json 
import base64
import random 
import datetime
from Crypto.Cipher import AES
from  Crypto.Hash import MD5 
app = Flask(__name__)
cons = [] 
convs = { }
public_keys = { }
@app.route("/", methods = ["GET"])
def main():
    return "main page "
    

@app.route("/create/<con>", methods = ["GET"])
def create(con):
        if con in convs : 
            return "already exsits "
        password_hash_md5= request.args.get("password")
        convs[con] ={"key":  base64.b64encode(random.randbytes(16)).decode(encoding="ascii"), "password":  password_hash_md5} 
        return "created"
@app.route("/join/publickeyserver/<con>", methods = ["GET"])
def join_first(con):
    id = None 
    while not id : 
        tmp =  base64.b64encode(random.randbytes(32)).decode(encoding="ascii")
        if tmp  not in public_keys : 
            id = tmp 
    public_keys[id] = {"keys" : rsa.newkeys(1024)    , "max-time": datetime.datetime.now()+datetime.timedelta(minutes=10) }
    return  {"id" : id , "pk": base64.b64encode(public_keys[id]["keys"][0].save_pkcs1()).decode(encoding="ascii"),"max-time":public_keys[id]["max-time"] } 
    
@app.route("/join/final/<con>", methods = ["POST"])
def join_final(con):
    name = request.form.get("name")
    id = request.form.get("id")
    arg = request.form.get("public_key")
    password = request.form.get("password")
    if not arg or not name or not password or not id : 
        return f"<p> you must enter public key and name and password and id  {con}</p> "
    public_key = rsa.PublicKey.load_pkcs1(base64.b64decode(arg))
    if id not in public_keys : 
        return "<p>you must put valid id session</p>"
    piv = public_keys[id]["keys"][1]
    
    
    
    password = rsa.decrypt(base64.b64decode(password) ,priv_key=piv).decode(encoding="ascii")
    name = rsa.decrypt(base64.b64decode(name),priv_key=piv).decode(encoding="ascii")
    md5 = MD5.new()
    md5.update(bytes(password,encoding="ascii"))
    hashedpass = md5.hexdigest() 
    if hashedpass != convs[con]["password"]: 
        return "<p>password is not valid  </p>"
    respone = {
        "con_id":con  , 
        "name" : name , 
        "key" : convs[con]["key"]
    } 
    
    respone = rsa.encrypt(json.dumps(respone).encode(),pub_key=public_key)
   
    print(respone)
    return respone
if __name__ == "__main__":
    app.run()