import mysql.connector

conexao = mysql.connector(
    host='localhost',
    user='root',
    password='!=Four8987',
    database='dbjokenpo',
)

cursor = conexao.cursor()