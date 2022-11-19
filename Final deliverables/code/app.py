from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify

from werkzeug.security import generate_password_hash, check_password_hash

import ibm_db,bcrypt,requests,io,json
import json
import pprint
import ibm_boto3
from ibm_botocore.client import Config, ClientError

connection = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=xrl27444;PWD=TR5CfVrO2n3Q92s4",'','')

COS_ENDPOINT="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID="Rn7yT8V81grCqj7fP1R33bi9ENOza2XF0wqjoV3XOZQH"
COS_INSTANCE_CRN="crn:v1:bluemix:public:cloud-object-storage:global:a/640be09080b0456c8f013b1b42ceb249:5818c20b-0847-4f5c-b78e-08c75250ff51::"

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=['GET'])
def home():
    if 'email' not in session:
      return redirect(url_for('login'))
    return render_template('index.html')


@app.route("/result",methods=['GET','POST'])
def reg():
    return render_template('result.html')

@app.route("/upload",methods=['GET','POST'])
def upload():
    return render_template('upload.html')

@app.route("/login", methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
      email = request.form['usermail']
      password = request.form['password']

      if not email or not password:
        return render_template('login.html',error='Please fill all fields')
      query = "SELECT * FROM users WHERE EMAIL=? AND PASSWORD=?"
      stmt = ibm_db.prepare(connection, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.bind_param(stmt,2,password)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(email,password)
      print(isUser)

      if not isUser:
        return render_template('login.html',error='Invalid Credentials = '+email, flash_message="True")
      session['email'] = isUser['EMAIL']
      flash("You are successfully logged in");
      return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/register')
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    name = request.form['username']

    if not email or not password or not name:
      return render_template('register.html',error='Please fill all fields')
    

    query = "SELECT * FROM users WHERE EMAIL=?"
    stmt = ibm_db.prepare(connection, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO USERS (EMAIL,PASSWORD,NAME,CREATED_ON) VALUES (?,?,?,CURRENT_TIMESTAMP)"
      prep_stmt = ibm_db.prepare(connection, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, email)
      ibm_db.bind_param(prep_stmt, 2, password)
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.execute(prep_stmt)
      return redirect(url_for('login'))
    else:
      return render_template('register.html', msg='Mail is already in use')

  return render_template('register.html')

@app.route('/uploader',methods=['POST'])
def uploader():
  name_file=request.form['imageURL']
  print("working fine")
  f = request.files['file']
  try:
      part_size = 1024 * 1024 * 5

      file_threshold = 1024 * 1024 * 15

      transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

      content = f.read()
      cos.Object('foodbucket', name_file).upload_fileobj(
                Fileobj=io.BytesIO(content),
                Config=transfer_config
            )
      return redirect(url_for('index'))
      

  except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
        return redirect(url_for('index'))

  except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))
        return redirect(url_for('index'))

@app.route('/profile')
def profile():
  
  if 'email' not in session:
    return redirect(url_for('login'))
  return render_template('profile.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("You are successfully logged out");
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)