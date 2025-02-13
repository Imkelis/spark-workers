from flask import Flask
from flask import request
from flask import jsonify
import requests
import os
import json
app = Flask(__name__)

def get_api_key() -> str:
    secret = os.environ.get("COMPUTE_API_KEY")
    if secret:
        return secret
    else:
        #local testing
        with open('.key') as f:
            return f.read()
      
@app.route("/")
def hello():
    return "Test Final Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/identify")
def identify():
    hostname = os.uname()[1]
    internal_ip = requests.get('http://whatismyip.akamai.com/').text
    return f"Hostname: {hostname}, Internal IP: {internal_ip}"


@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
    return "Test Final Use post to add" # replace with form template
  else:
    token=get_api_key()
    ret = addWorker(token,request.form['num'])
    return ret
  
  

@app.route("/addmultiple", methods=['POST'])
def add_multiple():
    if request.method == 'POST':
        token = get_api_key()
        vm_ids = request.form['nums'].split(',')
        responses = []
        for num in vm_ids:
            response = addWorker(token, num.strip())
            responses.append({"vm_id": num, "response": response})
        return jsonify(responses)
    else:
       return "Test Final Use post to add"
       



def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/fabled-sorter-399614/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+token}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
