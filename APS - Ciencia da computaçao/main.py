from PyQt5 import  uic,QtWidgets
import sqlite3
import hashlib

def chama_segunda_tela():
    nome_usuario = primeira_tela.lineEdit.text()
    senha = primeira_tela.lineEdit_2.text()

    if nome_usuario != "" and senha != "":
        nome_usuario_cript = hashlib.md5(nome_usuario.encode()).hexdigest()
        senha_user_cript = hashlib.md5(senha.encode()).hexdigest()
        banco = sqlite3.connect('Banco de Dados/bancoCadastro.db')
        cursor = banco.cursor()
        try:
            cursor.execute("SELECT senha text FROM cadastro WHERE login ='{}'".format(nome_usuario_cript))
            senha_BD = cursor.fetchall()    

            if senha_user_cript == senha_BD[0][0]:
                cursor.execute("SELECT nome text FROM cadastro WHERE login ='{}'".format(nome_usuario_cript))
                login = cursor.fetchall()
                
                print(login[0][0])

                if nome_usuario_cript == "b09c600fddc573f117449b3723f23d64":
                    segunda_tela.label_9.setText(login[0][0])
                    primeira_tela.close()
                    segunda_tela.show()
                    segunda_tela.pushButton_2.clicked.connect(abre_tela_cadastro)  
                else:
                    segundaCasu_tela.label_9.setText(login[0][0])
                    primeira_tela.close()
                    segundaCasu_tela.show()
            else:
                primeira_tela.label_5.setText("Senha incorreta") 
            banco.close()
        except:
            primeira_tela.label_6.setText("Login não cadastrado!")
    else:
        primeira_tela.label_5.setText("Preencha os campos")

def Fechar():
    tela_Excluir.close()
    tela_Alterar.close()
    segunda_tela.close()
    primeira_tela.close()
    tela_cadastro.close()
    segundaCasu_tela.close()
 
def carregadados():
    banco = sqlite3.connect('Banco de Dados/bancoCadastro.db') 
    cursor = banco.cursor()
    cursor.execute("SELECT nome text FROM cadastro ")
    lista = cursor.fetchall()
    #Sewgunda tela
    segunda_tela.tableWidget.setRowCount(len(lista))
    segunda_tela.tableWidget.setRowCount(len(lista))
    segunda_tela.tableWidget.setColumnCount(1)
    #tela excluir
    tela_Excluir.tableWidget.setRowCount(len(lista))
    tela_Excluir.tableWidget.setRowCount(len(lista))
    tela_Excluir.tableWidget.setColumnCount(1)
    
    for i in range(0, len(lista)):
        for j in range(0, 1):
           segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(lista[i][j])))
           tela_Excluir.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(lista[i][j])))
 
    banco.close()

def Voltar():
    tela_Excluir.close()
    tela_cadastro.close()
    segunda_tela.show()

def abre_tela_cadastro():
    tela_cadastro.show()
    segunda_tela.close()

    nome = segunda_tela.label_9.text()
    tela_cadastro.label_10.setText(nome)
    

def cadastrar():
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()
    if nome != "" and login != "" and senha != "":
        if (senha == c_senha ):
            try:               
                login_cript = hashlib.md5(login.encode()).hexdigest()
                senha_cript = hashlib.md5(senha.encode()).hexdigest()
                banco = sqlite3.connect('Banco de Dados/bancoCadastro.db') 
                cursor = banco.cursor()

                cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text NOT NULL UNIQUE, login text NOT NULL UNIQUE, senha text NOT NULL UNIQUE)")
                cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"','"+login_cript+"','"+senha_cript+"')")

                banco.commit() 
                banco.close()
                tela_cadastro.label_5.setText("Usuario cadastrado")

            except sqlite3.Error as erro:
                print("Erro ao inserir os dados: ",erro)
                tela_cadastro.label_5.setText("Erro. Usuario ja cadastrado")
        else:
            tela_cadastro.label_5.setText("As senhas estão diferentes")
    else:
        tela_cadastro.label_5.setText("Preencha os campos")

def TelaExcluir():
    tela_Excluir.show()
    segunda_tela.close()
    
    nome = segunda_tela.label_9.text()
    tela_Excluir.label_12.setText(nome)

    banco = sqlite3.connect('Banco de Dados/bancoCadastro.db') 
    cursor = banco.cursor()
    cursor.execute("SELECT nome text FROM cadastro ")
    lista = cursor.fetchall()
    tela_Excluir.tableWidget.setRowCount(len(lista))
    tela_Excluir.tableWidget.setRowCount(len(lista))
    tela_Excluir.tableWidget.setColumnCount(1)
    for i in range(0, len(lista)):
        for j in range(0, 1):
           tela_Excluir.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(lista[i][j])))
    banco.close()

def Excluir():
    segunda_tela.close()
    Nome_excluir = tela_Excluir.lineEdit.text()
    banco = sqlite3.connect('Banco de Dados/bancoCadastro.db') 
    cursor = banco.cursor()
    cursor.execute("DELETE FROM cadastro WHERE nome ='{}'".format(Nome_excluir))
    carregadados()

    banco.commit()
    banco.close()
    tela_Excluir.label_3.setText("Usuario excluido!")
    tela_Excluir.lineEdit.setText("")


def Alterar():
    print("Teste")

app=QtWidgets.QApplication([])
#Declarando as telas
primeira_tela=uic.loadUi("interface/TelaLogin.ui")
segunda_tela = uic.loadUi("interface/TelaLogadoAdm.ui")
segundaCasu_tela = uic.loadUi("interface/TelaLogadoNormal.ui")
tela_cadastro = uic.loadUi("interface/TelaCadastro.ui")
tela_Excluir = uic.loadUi("interface/TelaExcluir.ui")
tela_Alterar = uic.loadUi("interface/TelaAlterar.ui")

#Tela Login
primeira_tela.pushButton.clicked.connect(chama_segunda_tela)
primeira_tela.pushButton.clicked.connect(carregadados)
primeira_tela.pushButton_2.clicked.connect(Fechar)


#Tela Usuario Administrador
segunda_tela.pushButton_3.clicked.connect(Fechar)
segunda_tela.pushButton_6.clicked.connect(Fechar)
segunda_tela.pushButton_5.clicked.connect(TelaExcluir)
segunda_tela.pushButton_4.clicked.connect(Alterar)

#Tela de Usuario Normal
segundaCasu_tela.pushButton.clicked.connect(Fechar)
segundaCasu_tela.pushButton_3.clicked.connect(Fechar)

#Tela Cadastrar
tela_cadastro.pushButton.clicked.connect(carregadados)
tela_cadastro.pushButton.clicked.connect(cadastrar) 
tela_cadastro.pushButton_2.clicked.connect(Voltar)
tela_cadastro.pushButton_3.clicked.connect(Fechar)
tela_cadastro.pushButton_2.clicked.connect(carregadados)

#Tela Excluir
tela_Excluir.pushButton.clicked.connect(Excluir)
tela_Excluir.pushButton.clicked.connect(carregadados)
tela_Excluir.pushButton_2.clicked.connect(Fechar)
tela_Excluir.pushButton_3.clicked.connect(Voltar)
tela_Excluir.pushButton_3.clicked.connect(carregadados)

primeira_tela.show()
app.exec()