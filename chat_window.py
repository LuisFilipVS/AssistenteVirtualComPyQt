from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from interfaces.widgets.input_widget import Ui_Form as Input_Form
from interfaces.widgets.output_widget import Ui_Form as Out_Form

#Classes de configuração das interfaces

#Classe do Widget de mensagem enviada pelo usuario
class InputWidget(QWidget):
    def __init__(self, parent=None, chat_obj=None):
        super().__init__(parent)
        self.input_ui = Input_Form()
        self.input_ui.setupUi(self)

        self.chat_obj = chat_obj

        self.input_label = self.input_ui.label_2

    def set_input_text(self, input_str):
        self.input_label.setText(input_str)

    def set_edit_text(self):
        text = self.input_label.text()
        self.chat_obj.setPlainText()

#Classe do Widget de mensagem de retorno do assistente
class OutputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.out_ui = Out_Form()
        self.out_ui.setupUi(self)

        self.out_label = self.out_ui.label_2

    def set_output_text(self, out_str):
        self.out_label.setText(out_str)


#Classe principal do Widget que coordena os chat entre usuario e IA
class ChatWindow(QWidget):
    def __init__(self, parent=None, chat_obj=None, chat_data=None):
        super().__init__(parent)

        self.chat_object = chat_obj
        self.chat_data = chat_data
        self.main_verticalLayout = QVBoxLayout(self)
        self.main_verticalLayout.setContentsMargins(0,0,0,0)
        self.main_verticalLayout.setSpacing(0)
        self.main_verticalLayout.setObjectName("main_verticalLayout")

        self.style_str = '''
            QLabel {
                border: None;
                padding: 1px;
                border-radius: 5px;
                margin: 0px
            }

            QWidget {
                background: #AAB7B8;
            }

            '''
        self.setStyleSheet(self.style_str)
        self.chats_data = {
            "title" : "",
            "chat_list": []
        }

        if self.chat_data:
            self.chat_data["title"] = self.chat_data["title"]
            self.chats_data["chat_list"] += self.chat_data["chat_list"]

        self.show_chats() 

    def show_chats(self):
        print(self.chat_data.get("chat_list"))
        chat_list = self.chat_data.get("chat_list")
        for chat in chat_list:
            input_str = chat.get("input_str")
            input_widget = InputWidget(chat_obj=self.chat_object)
            input_widget.set_input_text(input_str)
            self.main_verticalLayout.addWidget(input_widget)

            out_str = chat.get("out_str")
            out_widget = OutputWidget()
            out_widget.set_output_text(out_str)
            self.main_verticalLayout.addWidget(out_widget)

        spacerItem = QSpacerItem(20,700,QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_verticalLayout.addItem(spacerItem)
        self.setLayout(self.main_verticalLayout)









