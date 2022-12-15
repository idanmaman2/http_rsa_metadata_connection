from flask import Flask, request
import rsa 
import json 
import pickle
import base64
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def hello_world():
    public_key = pickle.loads(base64.b64decode(request.args.get("public_key")))
    if not public_key : 
        return "<p> you must enter public key <\p> "
    print(public_key,type(public_key))
    respone = rsa.encrypt(json.dumps({"size":"800x800", "sindex": "100x10" ,"0":+3 , "1":-3 }).encode(),pub_key=public_key)
    print(respone)
    return respone
if __name__ == "__main__":
    app.run()