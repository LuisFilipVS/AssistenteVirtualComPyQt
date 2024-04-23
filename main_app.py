import json
from threading import Thread
from time import sleep
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget,QHBoxLayout, QLineEdit,QPushButton, QLabel, QGridLayout, QFrame
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from interfaces.widgets.MainWindow import Ui_MainWindow
from chat_window import ChatWindow

try:
    from assistente import assistente
    from capturaAudio import capturaAudio
except:
    from assistente import assistente
    from assistente import capturaAudio


#Classe que configura o menu da interface
class CustomWidget(QWidget):

    def __init__(self, text, show_btn_flag, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5,0,0,0)
        chat_icon = QIcon("interfaces/...")
        chat_icon_btn = QPushButton(self)
        chat_icon_btn.setIcon(chat_icon)
        chat_title = QLineEdit(self)
        chat_title.setText(text)
        chat_title.setReadOnly(True)
        delete_btn = QPushButton(self)
        delete_btn.setIcon(QIcon("interfaces/..."))
        edit_btn = QPushButton(self)
        edit_btn.setIcon("interfaces/...")

        style_str = """
        QPushButton {
            border: None;
            max_Width: 20px;
            max_height: 20px;
            background: transparent

        }

        """
        chat_title_style_str = """
        QLineEdit{
            background: transparent;
            border:None;
            color: #fff;
            font-size: 15px;
            padding-left:2px;
        }

        """
        chat_title.setStyleSheet(chat_title_style_str)
        chat_icon_btn.setStyleSheet(style_str)
        delete_btn.setStyleSheet(style_str)
        edit_btn.setStyleSheet(style_str)

        if not show_btn_flag:
            delete_btn.hide()
            edit_btn.hide()

        layout.addWidget(chat_icon_btn)
        layout.addWidget(chat_title)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

#Classe configura a Thread que irá executar a escuta da assistente em paralelo
class WorkerThread(QObject):
    iniciar_fala = pyqtSignal(bool)
    retorno = pyqtSignal(str,str)

    def __init__(self,janela):
        super().__init__()
        self.ui = janela

    #Inicializador da Thread
    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.Api_Assistente)
        self.timer.start(10000)

    #Chamada da Assistente
    def Api_Assistente(self):
        entrada, saida = None, None

        executor = assistente.assistente(interface=self.ui, iniciar_fala=self.iniciar_fala, retorno=self.retorno)
        entrada, saida = executor.iniciar()
        pass


#Classe que obtem a interface do chat onde está configurada todas as funções de
#operação com interfaces do projeto
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.chat_data = None

        self.message_input = self.ui.input_textEdit
        self.input_frame = self.ui.input_frame
        self.new_chat_btn = self.ui.Button_iniciar
        self.send_message_btn = self.ui.Button_enviar
        self.main_scrollArea = self.ui.scrollArea
        self.logout_btn = self.ui.Button_sair
        self.frame_confirma_escuta = self.ui.escuta_frame

        self.main_scrollArea.setVerticalScrollBarPolicy(1)
        self.message_input.setFixedHeight(24)
        self.input_frame.setFixedHeight(42)
        self.ui.input_frame.setVisible(False)

        # Set data for main window when start app
        self.show_chat_list()
        self.show_home_window()

        #Esconder Frame Confirma escuta de audio
        self.frame_confirma_escuta.setVisible(False)

        #Atribuindo gatilhos aoo botões
        self.send_message_btn.clicked.connect(self.get_response)
        self.new_chat_btn.clicked.connect(self.Api_Assistente)
        self.logout_btn.clicked.connect(self.logout)

    #Função que irá criar o chat de comunicação e iniciará o loop de escuta em outra Thread
    def create_new_chat(self):
        self.frame_confirma_escuta.setVisible(True)
        self.ui.Habilitar_voz.setVisible(False)

        self.paralelo = WorkerThread(self)
        self.paralelo.run()

    #Função de configuração da Thread
    def Api_Assistente(self):
        self.frame_confirma_escuta.setVisible(True)
        self.ui.Habilitar_voz.setVisible(False)
        
        self.thread = QThread()
        self.paralelo = WorkerThread(self)
        self.paralelo.moveToThread(self.thread)

        self.thread.started.connect(self.paralelo.run)
        self.paralelo.iniciar_fala.connect(self.alterar_status)
        self.paralelo.retorno.connect(self.get_response)
        self.thread.start()

    #Função que irá definir na interface quando o usuário poderá falar
    def alterar_status(self,chave):
        self.ui.Habilitar_voz.setVisible(chave)
    
    #Função que irá operar a execução da assistente
    def obter_retorno_assistente(self):
        entrada, saida = None, None
        executor = assistente.assistente()
        entrada, saida = executor.iniciar()
        print(entrada, saida)
    
    #Função que irá imprimir no chat cada mensagem trocada entre usuário e assistente
    def get_response(self, msg_entrada, msg_saida):
        # Recebe o texto formatado para a assistente

        #message_input = self.message_input.toPlainText().strip()
        message_input = msg_entrada
        message_output = msg_saida
        

        print(self.chat_data)
        if self.chat_data is None:
            if message_input:
                self.chat_data = {
                "title": message_input,
                "chat_list": [
                    {
                        "input_str" : message_input,
                        "out_str": message_output
                    }
                ]
            }
                
        else:
            if message_input:
                self.chat_data["chat_list"].append(
                    {
                        "input_str" : message_input,
                        "out_str": message_output
                    }
                )

        self.show_chat_window(self.chat_data)
        pass
    
    
    def show_chat_list(self,selected_index=None):
        pass

    def show_home_window(self):
        grid_layout = self.clear_main_scroll_area()

    #Função que fecha a aplicação  
    def logout(self):
        self.close()

    #Função auxiliar para adicionar a tela de chat na tela principal
    def show_chat_window(self, chat_data):
        grid_layout = self.clear_main_scroll_area()
        print(chat_data)
        chat_window = ChatWindow(chat_obj=self.message_input, chat_data=chat_data)
        grid_layout.addWidget(chat_window)

    #Função auxiliar que limpa o widget com as mensagens trocadas no chat
    def clear_main_scroll_area(self):
        grid_layout = self.main_scrollArea.findChild(QGridLayout)
        grid_layout.setContentsMargins(0,0,0,0)

        children_list = grid_layout.children()
        remove_widget_list = [QLabel, QPushButton, QFrame]

        for remove_widget in remove_widget_list:
            children_list += self.main_scrollArea.findChildren(remove_widget)

        for child in children_list:
            child.deleteLater()

        # Remover os espaçamentos
        for row in range(grid_layout.rowCount()):
            for column in range(grid_layout.columnCount()):
                item = grid_layout.itemAtPosition(row, column)
                if item:
                    grid_layout.removeItem(item)

        return grid_layout
        






            









