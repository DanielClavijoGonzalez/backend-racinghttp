import jwt
import mysql.connector
from config import KEY_TOKEN_AUTH
from config import SECRET_KEY, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_DB
from config import MYSQL_PASSWORD
import datetime
import bcrypt

def fixStringClient(string):
    fixed = str(string).replace("'", "").replace("*", "").replace('"', "").replace("+", "").replace("|", "").replace("%", "").replace("$", "").replace("&", "").replace("=", "").replace("?", "").replace('¡', "").replace("\a", "").replace("<", "").replace(">", "").replace("/", "").replace("[", "").replace("]", "").replace("(", "").replace("]", "").replace("´", "").replace(",", "").replace("!", "").replace("\n", "")
    return fixed

def checkJwt(token):
    try:
        data = jwt.decode(token[1], KEY_TOKEN_AUTH , algorithms=['HS256'])
        return True
    except:
        return False

def dataTableMysql(query, rtn="datatable"):
    try:
        mydb = mysql.connector.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB)
        mycursor = mydb.cursor()
        mycursor.execute(query)
        data = mycursor.fetchall()
        mydb.commit()
        
        if rtn == "datatable":
            mycursor.close()
            return data
        elif rtn == "rowcount":
            if mycursor.rowcount >= 1:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False
        else:
            mycursor.close()
            return data
    except:
        return False
    

def encoded_jwt(email):
    return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30), 'email': email}, KEY_TOKEN_AUTH , algorithm='HS256')

def cryptStringBcrypt(string, rtn="string", slt=10):
    salt = bcrypt.gensalt(slt)
    hashed = bcrypt.hashpw(bytes(str(string), encoding= 'utf-8'), salt)
    if rtn == "string":
        return hashed.decode("utf-8")
    elif rtn == "byte":
        return hashed
    else:
        return hashed.decode("utf-8")

def decryptStringBcrypt(EncValidate, EncCompare):
    return bcrypt.checkpw(bytes(str(EncValidate), encoding= 'utf-8'), EncCompare)