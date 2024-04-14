'''
Classe criada para conter funçoes de captura de audio por meio da biblioteca
speech_recognition '''

import speech_recognition as sr

class capturaAudio():
    def __init__(self):
        self.TEMPO_DE_ESCUTA = 4
        pass

    def escutaVoz(self, interface=None):
        self.reconhecedor_voz = sr.Recognizer()
        self.fala_reconhecida = False
        self.fala = None
        with sr.Microphone() as fonte_audio:
            try:
                self.reconhecedor_voz.adjust_for_ambient_noise(fonte_audio)
                if not interface:
                    #Adicionar informação na interface gráfica
                    pass

                print("Fale alguma coisa...")
                self.fala = self.reconhecedor_voz.listen(fonte_audio, timeout=4, phrase_time_limit=4)
                self.fala_reconhecida = True
            except Exception as e:
                print(f"Falha na tentativa de reconhecer alguma voz {str(e)}")
        return self.fala_reconhecida , self.fala

    def traduzir_audio(self, reconhecedor, audio, IDIOMA="pt-BR"):
        traduzido, traducao = False, None
        try:
            traducao = reconhecedor.recognize_google(audio, language=IDIOMA)
            traducao = traducao.lower()

            traduzido = True

        except Exception as e:
            print(f"Erro ocorrido no processo de traducao {str(e)}")
        return traduzido, traducao


if __name__ == "__main__":
    voz = capturaAudio()
    
    escutado,fala = voz.escutaVoz()
    traduzido, traducao = voz.traduzir_audio(voz.reconhecedor_voz,fala)

    if escutado:
        print(traducao)
    else:
        print("Nada capturado")
