import random
import math
import numpy as np
import pandas as pd
import scipy.stats
from state import State
from beta_dist import BetaDist
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model


class Comeca(State):

    def carrega_dados(self):
        df = pd.read_csv("lotomania_result.csv")
        df.drop(['Concurso', 'Data Sorteio'], axis=1, inplace=True)
        self.set_data_frame(df);

    def next(self):
        self.set_numbers([])
        self.carrega_dados()

        return GeraBolasRNR(numbers=self.get_numbers(), df=self.get_data_frame())


class GeraBolasRNR(State):
    """
    Estado no qual o modelo de IA gera sua previsão do conjunto com 20 bolas
    """

    def gera(self):
        # Fetch data
        df = self.get_data_frame()   
        to_predict = df.tail(10) # esse modelo foi treinado com window size 10
        to_predict = np.array(to_predict)
        scaler = StandardScaler().fit(df.values)
        scaled_to_predict = scaler.transform(to_predict)

        filepath = 'model_v2.h5'
        model = load_model(filepath)
        y_pred = model.predict(np.array([scaled_to_predict]))
        y_pred = scaler.inverse_transform(y_pred).astype(int)[0]
        #print("The predicted numbers are:", y_pred)
        
        return y_pred.tolist()
    
    def post_process(self, list):
        """
        Faz o pós processamento da saida da rede neural para eliminar numeros
        repetidos e deixar a lista com 20 números caso necessário
        """

        aux_list = [*set(list)]

        if len(aux_list) < 20:
            aux_list.append( random.randint(0,99) )
            aux_list = self.post_process(aux_list)
        else:
            return aux_list
        
        return aux_list


    def next(self):
        N = self.gera()
        N = self.post_process(N)
        self.set_numbers(N)
        print('\nBolas geradas pela rede neural: ', self.get_numbers())
        
        return GeraBolasDistBeta(numbers=self.get_numbers())
        

class GeraBolasUniforme(State):
    """
    Estado no qual são geradas mais 10 bolas com base em uma distribuição uniforme
    """
    
    def gera(self, numbers):
        x = random.randint(0,99)

        if x in numbers:
            return self.gera(numbers)
        else:
            return x
        

    def next(self):
        num_bolas = 0
        while num_bolas < 10:
            n = self.get_numbers()
            rnd = self.gera(n)
            n.append(rnd)
            self.set_numbers(n)
            num_bolas += 1

        print('\nBolas geradas por dist uniforme:')
        print(self.get_numbers())

        return ApresentaResultado(numbers=self.get_numbers())

         
class GeraBolasDistBeta(State):
    """
    Estado no qual são geradas mais 20 bolas com base em uma distribuição BETA
    """
    
    def gera_numero_unico(self, pdf, numbers):
        x = math.floor(pdf.rvs())
        if x in numbers:
            return self.gera_numero_unico(pdf, numbers)
        else:
            return x

    def gera(self):
        numBola = 1
        while numBola <= 20:
            dist = BetaDist('Bola'+str(numBola)).pdf()
            numbers = self.get_numbers()
            rnd_num = self.gera_numero_unico(dist, numbers)
            # Atualiza o array de numeros para que não haja repetição dos numeros
            numbers.append(rnd_num)
            self.set_numbers(numbers)            
            numBola += 1

    def next(self):
        self.gera()
        print('\nNumeros gerados pela dist beta')
        print(self.get_numbers())

        #if event == 'gerou_bolas_dist_beta':
        return GeraBolasUniforme(numbers=self.get_numbers())
        

class ApresentaResultado(State):
    """
    Estado final
    """

    def next(self):
        print('\nVocê deve apostar nestes numeros:')
        print(np.sort(self.get_numbers()))

