'''
Classe criada para conter funçoes de captura de audio por meio da biblioteca
speech_recognition '''

import speech_recognition as sr

class capturaAudio():
    def __init__(self,interface, iniciar_fala):
        self.iniciar_fala = iniciar_fala
        self.interface = interface
        self.TEMPO_DE_ESCUTA = 4
        self.reconhecedor_voz = sr.Recognizer()
        pass

    #Função que recebe o reconhecedor e habilita a escuta de voz, retornando a fala em audio
    def escutaVoz(self, interface=None, reconhecedor=sr.Recognizer()):
        self.reconhecedor_voz = reconhecedor
        self.fala_reconhecida = False
        self.fala = None
        with sr.Microphone() as fonte_audio:
            try:
                self.reconhecedor_voz.adjust_for_ambient_noise(fonte_audio)

                print("Fale alguma coisa...")
                if interface is not None:
                    #interface.ui.ui.Habilitar_voz.setVisible(True)
                    self.iniciar_fala.emit(True)
                self.fala = self.reconhecedor_voz.listen(fonte_audio, timeout=7, phrase_time_limit=7)
                if interface is not None:
                    #interface.ui.ui.Habilitar_voz.setVisible(False)
                    self.iniciar_fala.emit(False)
                self.fala_reconhecida = True
            except Exception as e:
                self.iniciar_fala.emit(False)
                print(f"Falha na tentativa de reconhecer alguma voz {str(e)}")
        return self.fala_reconhecida , self.fala
    
    #Função que recebe o audio e o traduz para uma string utilizando o recurso da Google
    def traduzir_audio(self,audio,reconhecedor=sr.Recognizer(),IDIOMA="pt-BR"):
        traduzido, traducao = False, None
        try:
            traducao = reconhecedor.recognize_google(audio, language=IDIOMA)
            traducao = traducao.lower()

            traduzido = True

        except Exception as e:
            print(f"Erro ocorrido no processo de traducao {str(e)}")
        return traduzido, traducao
    
    #Função para obter string por meio da leitura de arquivo de audio
    def obter_string_captura_por_arquivo_audio(self,arquivo, reconhecedor=sr.Recognizer()):
        self.fala_reconhecida, self.fala = None,None
        with sr.AudioFile(arquivo) as fonte_audio:
            try:
                self.fala = reconhecedor.listen(fonte_audio)
                self.fala_reconhecida = True
            except Exception as e:
                print(f"Erro ao obter audio a partir de arquivo de audio: {e}")

        return self.fala_reconhecida, self.fala

    #Função que executa a escuta de audio e a retorna convertida em string
    def obter_string_captura(self):
        traducao = None
        escutado,fala = self.escutaVoz(interface=self.interface)
        traduzido, traducao = self.traduzir_audio(fala)

        if not (escutado and traduzido):
            print("Falha na obtenção ou traducao do audio...")    
        return escutado, traduzido, fala, traducao

        
if __name__ == "__main__":
    voz = capturaAudio(None,None)
    
    _,_,_,traducao = voz.obter_string_captura()

    if traducao is not None:
        print(traducao)
    else:
        print("Nada capturado")
