import ibm_db

connection = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dhq06480;PWD=RU3oAevR87GjcL1s",'','')

print(connection)
print("Connection Successfull !\n\n")

sql = "SELECT EMAIL,PASSWORD FROM logins"
stmt = ibm_db.exec_immediate(connection, sql)
dictionary = ibm_db.fetch_assoc(stmt)
while dictionary != False:
    # printing
    print("Full Row : ", dictionary)
    dictionary = ibm_db.fetch_assoc(stmt)