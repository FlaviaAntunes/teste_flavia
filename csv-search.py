
import pandas as pd
import sys
import argparse
from datetime import date, datetime
import os

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'ind',
            type=str,
            default='0'
        )
        parser.add_argument(
            'dh_iso',
            type=str,
            default='0'
        )
        parser.add_argument(
            '--output',
            type=str,
            default=('json')
        )
        args = parser.parse_args()

        indicador = args.ind
        data_hora = args.dh_iso
        data_hora = data_hora.replace("'","")
        nome = args.output
        now = str(datetime.now())
        now = now.split(".")[0]
        now = now.replace(" ","_")
        now = now.replace(":","-")
        existe = False

        if nome == 'json':
            output_arq = open(now+"."+nome, 'w')
        elif nome == 'csv':
            output_arq = open(now+"."+nome, 'w')
            output_arq.writelines("device,prefix,instant,payload,company\n")
        else:
            print("Formato de arquivo inválido")
            sys.exit()
            
        pesquisa = pd.read_csv('data/eventlog.csv')
        data = data_hora.split("T")[0]
        aux = data_hora.split("T")[1]
        hora = aux.split("-")[0]
        
        data_tabela = []
        hora_tabela = []

        for k in range(len(pesquisa.instant)):
            s = str(pesquisa.instant[k])
            data_tabela.append(s.split("T")[0])
            dados = s.split("T")[1] 
            hora_tabela.append(dados.split("-")[0])
        

        hora_d = hora.split(":")[0]
        minuto_d = hora.split(":")[1]
        segundo_d = hora.split(":")[2]

        for i in range(len(pesquisa.device)):
            if str(indicador) == str(pesquisa.device[i]):
                date = datetime.strptime(data_tabela[i], '%Y-%m-%d').date()
                date2 = datetime.strptime(data, '%Y-%m-%d').date()
                if date.toordinal() == date2.toordinal():
                    hora_t = hora_tabela[i].split(":")[0]
                    minuto_t = hora_tabela[i].split(":")[1]
                    segundo_t = hora_tabela[i].split(":")[2]

                    if hora_t > hora_d or hora_t == hora_d and minuto_t > minuto_d or hora_t == hora_d and minuto_t == minuto_d and segundo_t >= segundo_d:
                        if nome == 'json':
                            output_arq.writelines("{\n \"device\": \""+str(pesquisa.device[i])+'\",\n \"prefix\": \"'+str(pesquisa.prefix[i])+'\",\n \"instant\": \"'+str(pesquisa.instant[i])+'\",\n \"payload\": \"'+str(pesquisa.payload[i])+'\",\n \"company\": \"'+str(pesquisa.company[i])+"\"\n}\n")
                        elif nome == 'csv':
                            output_arq.writelines(str(pesquisa.device[i])+','+str(pesquisa.prefix[i])+','+str(pesquisa.instant[i])+',\"'+str(pesquisa.payload[i])+'\",'+str(pesquisa.company[i])+"\n")
                        existe = True
                        
                            

                elif date.toordinal() > date2.toordinal():
                    if nome == 'json':
                        output_arq.writelines("{\n \"device\": \""+str(pesquisa.device[i])+'\",\n \"prefix\": \"'+str(pesquisa.prefix[i])+'\",\n \"instant\": \"'+str(pesquisa.instant[i])+'\",\n \"payload\": \"'+str(pesquisa.payload[i])+'\",\n \"company\": \"'+str(pesquisa.company[i])+"\"\n}\n")
                    elif nome == 'csv':
                        output_arq.writelines(str(pesquisa.device[i])+','+str(pesquisa.prefix[i])+','+str(pesquisa.instant[i])+',\"'+str(pesquisa.payload[i])+'\",'+str(pesquisa.company[i])+"\n")
                    existe = True
        if(existe):
            name = now+"."+nome
            print ("Pesquisa concluída: Arquivo {} gerado".format(name))
            output_arq.close()
        else:
            name = now + "." + nome
            output_arq.close()
            local = os.path.dirname(os.path.realpath(__file__))
            print ("Pesquisa concluída: Valores não encontrados")
            os.remove(os.path.join(local, name))


if __name__ == '__main__':
  #parser = argparse.ArgumentParser()
  #parser.add_argument(
  #    '--output',
  #    type=str,
  #    default='arq.json'
  #)
  
  main()
    

