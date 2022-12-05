import os
import tweepy
import schedule
import time
import random, os
from decouple import config

# Llaves de la API
os.environ['API_KEY'] = config('API_KEY')
os.environ['API_KEY_SECRET'] = config('API_KEY_SECRET')
API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']

os.environ['ACCESS_TOKEN'] = config('ACCESS_TOKEN')
os.environ['ACCESS_TOKEN_SECRET'] = config('ACCESS_TOKEN_SECRET')
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

#Autorizacion / Inicio de sesion
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)

# #Array de comandos
comandos = ['!req']

# #Funcion para leer la ultima id - Cuando lo mencionen (Esta funcion regresa como valor la id almacenada en la hoja de texto)
def read_last_id():
    file = open('ultima_id.txt', 'r')
    id = int(file.read().strip())
    file.close
    return id


# #Funcion para sobreescribir la ultima id - Cuando lo mencionen
def store_last_id(id):
    file = open('ultima_id.txt', 'w')
    file.write(str(id))
    file.close


# #Funcion para responder a una mencion con una imagen al azar
def reply_random_file(tweet):
    #Aca ingresa a la carpeta imagenes
    path = 'imagenes'
    #Esta cosa es para elegir un archivo al azar
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
        ])

    archivo_sin_extension = os.path.basename(random_filename)

    #Aca imprime el nobre del archivo en la consola sin la extension
    print('Respondiendo con la imagen: ' + os.path.splitext(archivo_sin_extension)[0] + '\n')

    #Esto cambia el directorio de trabajo
    back = os.getcwd()
    os.chdir('./imagenes/')

    #Esto guarda el archivo escogido en la variable media
    media = api.media_upload(random_filename)
    #Esto es el texto que acompaña a la imagen que se sube
    status = 'Su imagen\n' + 'Num. de imagen: ' + os.path.splitext(archivo_sin_extension)[0]

    #Esto hace que se postee el resultado (el stautus y el archivo)
    post_result = api.update_status('@' + tweet.user.screen_name + ' ' + status, media_ids=[media.media_id],
    in_reply_to_status_id = tweet.id)

#     #Esto hace que se al directorio padre
    os.chdir(back)
    #Se llama a la funcion para sobreescribir la id una ves se haya posteado el resultado
    store_last_id(tweet.id)


# #Funcion para responder con una imagen requerica con el comando !req
# def reply_req(tweet, numero_final):
#     img_req = numero_final
#     path_req = 'imagenes/' + img_req
#     filename_req = path_req + '.jpg'

#     archivo_sin_extension_req = os.path.basename(filename_req)
#     print('Respondiendo con la imagen: ' + os.path.splitext(archivo_sin_extension_req)[0] + '\n')

#     back = os.getcwd()
#     os.chdir('./imagenes/')
#     os.chdir(back)

#     media = api.media_upload(filename_req)
#     status = 'Su pedido\nNum. de imagen: ' + numero_final

#     post_result = api.update_status('@' + tweet.user.screen_name + ' ' + status, media_ids=[media.media_id],
#     in_reply_to_status_id = tweet.id)

#     os.chdir(back)
    
#     store_last_id(tweet.id)


#Funcion para checar las menciones
def check_mentions():
    mentions = api.mentions_timeline(since_id = read_last_id(), tweet_mode = 'extended')

    for tweet in reversed(mentions):
        string_list_tweet = tweet.full_text.split()
        print('\nCita del tuit:')
        print(tweet.full_text)
        print('Array de la cita:')
        print(string_list_tweet)

        # if any(x in tweet.full_text for x in comandos):
        #     separar_comando = tweet.full_text.split(sep = '(')
        #     # print(separar_comando[-1])
        #     if (separar_comando[0] == comandos[0]):
        #         numero_requerido = separar_comando[-1].split(sep = ')')
        #         numero_final = numero_requerido[0]
        #         print('El numero de la imagen solicitada: ' + numero_final)
        #         reply_req(tweet, numero_final)

        # else:
        reply_random_file(tweet)

def main():
    #Esto se encarga de revisar las menciones cada 40 segundos
    schedule.every(3).seconds.do(check_mentions)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except tweepy.error.TweepError as e:
            raise e

if __name__ == "__main__":
	main()