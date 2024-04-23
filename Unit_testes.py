import unittest

from assistente.assistente import *
from assistente.capturaAudio import *
from assistente.linguagemNatural import *

AUDIO_LIGAR_GPS = "audios/ligar_gps.wav"
AUDIO_DESLIGAR_AR = "audios/delisgar_ar_condicionado.wav"
AUDIO_ALTERAR_TEMPERATURA = "audios/alterar_temperatura.wav"
AUDIO_ALEXA_NAO_ASSISTENTE = "audios/alexa_ligar_gps.wav"


class TestesUnitariosAssistente(unittest.TestCase):
    def setUp(self):
        self.executor = assistente()
        self.capturaAudio = capturaAudio(iniciar_fala=None,interface=None)
        self.linguagemNatural = linguagemNatural()
        self.nome_assistente = self.executor.nome_assistente
        self.acoes_possiveis = self.executor.acoes    

    def test_01_reconhecer_nome(self):    
        tem_fala, fala = self.capturaAudio.obter_string_captura_por_arquivo_audio(AUDIO_LIGAR_GPS)
        self.assertIsNotNone(fala) and self.assertTrue(tem_fala)

        tem_texto, texto = self.capturaAudio.traduzir_audio(fala)
        self.assertIsNotNone(texto) and self.assertTrue(tem_texto)

        tokens = self.linguagemNatural.obter_tokens(texto)
        self.assertEqual(tokens[0],self.nome_assistente)
        
    def test_02_nao_reconhecer_outro_nome(self):
        tem_fala, fala = self.capturaAudio.obter_string_captura_por_arquivo_audio(AUDIO_ALEXA_NAO_ASSISTENTE)
        self.assertIsNotNone(fala) and self.assertTrue(tem_fala)

        tem_texto, texto = self.capturaAudio.traduzir_audio(fala)
        self.assertIsNotNone(texto) and self.assertTrue(tem_texto)

        tokens = self.linguagemNatural.obter_tokens(texto)
        self.assertNotEqual(tokens[0],self.nome_assistente)
        

    def test_03_ligar_gps(self):
        tem_fala, fala = self.capturaAudio.obter_string_captura_por_arquivo_audio(AUDIO_LIGAR_GPS)
        self.assertIsNotNone(fala) and self.assertTrue(tem_fala)

        tem_texto, texto = self.capturaAudio.traduzir_audio(fala)
        self.assertIsNotNone(texto) and self.assertTrue(tem_texto)

        tokens = self.linguagemNatural.obter_tokens(texto)
        tokens = self.linguagemNatural.retirar_palavras_de_parada(tokens)
        self.assertEqual(tokens[0],self.nome_assistente)

        _,acao,objeto,_,_, = self.executor.validar_comando(tokens,self.nome_assistente,self.acoes_possiveis)
        self.assertEqual(objeto,"gps")


    def test_04_altera_temperatura_ar(self):
        tem_fala, fala = self.capturaAudio.obter_string_captura_por_arquivo_audio(AUDIO_ALTERAR_TEMPERATURA)
        self.assertIsNotNone(fala)
        self.assertTrue(tem_fala)

        tem_texto, texto = self.capturaAudio.traduzir_audio(fala)
        self.assertIsNotNone(texto)
        self.assertTrue(tem_texto)

        tokens = self.linguagemNatural.obter_tokens(texto)
        tokens = self.linguagemNatural.retirar_palavras_de_parada(tokens)
        self.assertEqual(tokens[0],self.nome_assistente)

        _,acao,objeto,valor,uni_medida = self.executor.validar_comando(tokens,self.nome_assistente,self.acoes_possiveis)
        self.assertEqual(objeto,"temperatura")
        self.assertIn(uni_medida,['fahrenheit','celsius'])
    
if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = unittest.TestSuite()

    tests.addTests(loader.loadTestsFromTestCase(TestesUnitariosAssistente))

    executer = unittest.TextTestRunner()
    executer.run(tests)
    pass
    




