import mysql.connector
from typing import Optional

def criarConexao(db: Optional[str] = None):
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='!=Four8987',
        database=db
    )

def criarDB():
    conexao = criarConexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS dbjokenpo")
        cursor.execute("USE dbjokenpo")
        criarTabelas(cursor)
    except mysql.connector.Error as err:
        print(f"Erro ao criar o banco de dados: {err}")
    

def criarTabelas(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `dbjokenpo`.`partidas` (
                `id_partida` INT NOT NULL AUTO_INCREMENT,
                `vencedor` VARCHAR(45) NOT NULL,
                `rodadas` INT NOT NULL,
                PRIMARY KEY (`id_partida`));
            """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `dbjokenpo`.`rodadas` (
                `cod_rodada` INT ZEROFILL NOT NULL AUTO_INCREMENT,
                `id_partida` INT NULL NOT NULL,
                `rodada` INT NOT NULL,
                `move_player_1` VARCHAR(20) NOT NULL,
                `move_player_2` VARCHAR(20) NOT NULL,
                `resultado` VARCHAR(50) NOT NULL,
                PRIMARY KEY (`cod_rodada`),
                INDEX `id_partida_idx` (`id_partida` ASC) VISIBLE,
                CONSTRAINT `id_partida`
                FOREIGN KEY (`id_partida`)
                REFERENCES `dbjokenpo`.`partidas` (`id_partida`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION);
            """
        )
    except mysql.connector.Error as err:
        print(f"Erro ao criar o banco de dados: {err}")

criarDB()