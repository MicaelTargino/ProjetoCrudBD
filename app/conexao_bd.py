import mysql.connector
from mysql.connector import Error
import os
from typing import Optional, List, Tuple
import time

class ConexaoBD:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.usuario = os.getenv('DB_USER', 'usuario')
        self.senha = os.getenv('DB_PASSWORD', 'senha123')
        self.banco = os.getenv('DB_NAME', 'supermercado_db')
        self.conexao = None
        self.cursor = None
        self.tentar_conectar()
    
    def tentar_conectar(self, tentativas_max: int = 5):
        tentativa = 0
        while tentativa < tentativas_max:
            try:
                self.conectar()
                if self.conexao and self.conexao.is_connected():
                    print(f"Conectado ao banco de dados MySQL")
                    break
            except Error as e:
                tentativa += 1
                print(f"Tentativa {tentativa} de {tentativas_max} falhou: {e}")
                if tentativa < tentativas_max:
                    time.sleep(5)
                else:
                    raise e
    
    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                use_unicode=True
            )
            self.cursor = self.conexao.cursor(dictionary=True)
            self.cursor.execute("SET NAMES utf8mb4")
            self.cursor.execute("SET CHARACTER SET utf8mb4")
            self.cursor.execute("SET character_set_connection=utf8mb4")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise e
    
    def desconectar(self):
        if self.conexao and self.conexao.is_connected():
            if self.cursor:
                self.cursor.close()
            self.conexao.close()
    
    def executar_query(self, query: str, parametros: Optional[Tuple] = None) -> Optional[List]:
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
            
            self.cursor.execute(query, parametros or ())
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conexao.commit()
                return None
        except Error as e:
            print(f"Erro ao executar query: {e}")
            if self.conexao:
                self.conexao.rollback()
            raise e
    
    def executar_insert(self, query: str, parametros: Tuple) -> Optional[int]:
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
            
            self.cursor.execute(query, parametros)
            self.conexao.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Erro ao inserir dados: {e}")
            if self.conexao:
                self.conexao.rollback()
            raise e
    
    def executar_update(self, query: str, parametros: Tuple) -> int:
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
            
            self.cursor.execute(query, parametros)
            self.conexao.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Erro ao atualizar dados: {e}")
            if self.conexao:
                self.conexao.rollback()
            raise e
    
    def executar_delete(self, query: str, parametros: Tuple) -> int:
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
            
            self.cursor.execute(query, parametros)
            self.conexao.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Erro ao deletar dados: {e}")
            if self.conexao:
                self.conexao.rollback()
            raise e
    
    def verificar_conexao(self) -> bool:
        return self.conexao and self.conexao.is_connected()
    
    def iniciar_transacao(self):
        if self.verificar_conexao():
            self.conexao.start_transaction()
    
    def confirmar_transacao(self):
        if self.verificar_conexao():
            self.conexao.commit()
    
    def reverter_transacao(self):
        if self.verificar_conexao():
            self.conexao.rollback()