import os
import shutil
from datetime import datetime
#
import google.auth
import google.auth.transport.requests
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# Proporciona la interfaz de interaccion con los servicios de google
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from moviepy.video.io.VideoFileClip import VideoFileClip


class UpVid:

    EXT_VID = ['.mp4']
    # configuraciones
    SETTINGS = {}

    # Credenciales
    CREDS = None
    CREDS2 = None

    # nombre.mp4
    VID_TO_UPLOAD = []

    # propiedades del video: ruta, nombre
    VIDEO_PROP = []

    def __init__(cls):
        print(cls)

    @classmethod
    def setSettings(cls, settings):
        """ Setea directorio de videos """
        if cls.SETTINGS != settings:
            print({settings})
            cls.SETTINGS['DIRECTORIO'] = settings['DIRECTORIO']
            cls.SETTINGS['vidsToUpload'] = settings['vidsToUpload']

    @classmethod
    def autenticar(cls):
        """ Autenticacion de la aplicacion y el usuario """
        if os.path.exists('token.json') and os.path.exists('token_r.json'):
            cls.CREDS = Credentials.from_authorized_user_file('token.json')
            cls.CREDS2 = Credentials.from_authorized_user_file('token_r.json')
        if not cls.CREDS or not cls.CREDS.valid:
            if (cls.CREDS or cls.CREDS2) and (cls.CREDS.expired or cls.CREDS2.expired) and (cls.CREDS.refresh_token or cls.CREDS2.refresh_token):
                cls.CREDS.refresh(google.auth.transport.requests.Request())
                cls.CREDS2.refresh(google.auth.transport.requests.Request())
            else:
                flujo = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', scopes=['https://www.googleapis.com/auth/youtube.upload']
                )
                cls.CREDS = flujo.run_local_server(port=0)

                flujo = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', scopes=['https://www.googleapis.com/auth/youtube.readonly']
                )
                cls.CREDS2 = flujo.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(cls.CREDS.to_json())
            with open('token_r.json', 'w') as token:
                token.write(cls.CREDS2.to_json())

    @classmethod
    def searchVids(cls):
        """ Busca los videos en el directorio """
        os.chdir(cls.SETTINGS['DIRECTORIO'])  # setea el directorio
        files = os.listdir()
        vids = []
        for f in files:
            name, _ext = os.path.splitext(f)
            if _ext in cls.EXT_VID:
                vids.append(f)
        if vids == []:
            print('No videos en directorio!')
        if cls.SETTINGS['vidsToUpload'] == 1:
            cls.VID_TO_UPLOAD.append(cls.searchCurrentVid(vids))
        elif cls.SETTINGS['vidsToUpload'] == 2:
            cls.VID_TO_UPLOAD = vids

    @classmethod
    def searchCurrentVid(cls, vids):
        """ Busca el video actual para subir """
        for v in vids:
            prop = os.stat(v)
            fechaVid = datetime.fromtimestamp(
                prop.st_ctime).strftime("%d/%m/%Y")
            actualFecha = datetime.now().strftime("%d/%m/%y")
            if fechaVid == actualFecha:
                print(f'Video actual es : {v}')
                return v

    @classmethod
    def prepareVid(cls):
        """ Setea lass propiedades del video """
        if cls.VID_TO_UPLOAD == [] or cls.VID_TO_UPLOAD == '':
            print('Not vid to upload')
            return False
        for _v_to_up in (cls.VID_TO_UPLOAD):
            ruta_video = os.path.join(
                cls.SETTINGS['DIRECTORIO'], _v_to_up)
            titulo_video = os.path.basename(
                os.path.join(cls.SETTINGS['DIRECTORIO'], _v_to_up))

            video = VideoFileClip(ruta_video)
            duracion = int(video.duration)
            horas = (duracion // 3600)
            minutos = (duracion // 60)
            segundos = (duracion % 60)
            print(
                f'Duracion del video es {horas} horas con {minutos} minutos y {segundos} segundos')

            video_prop = {
                'ruta_video': ruta_video,
                'titulo_video': titulo_video,
                'duracion': duracion,
                'duracion_horas': horas,
                'duracion_minutos': minutos,
                'duracion_segundos': segundos
            }

            cls.VIDEO_PROP.append(video_prop)

            if horas >= 24:
                if cls.dividirVideo(video=video, video_prop=video_prop):
                    cls.uploadVid()
            else:
                cls.uploadVid()


    def verificarVideoUploaded(cls, video_title):
        youtube = build('youtube', 'v3', credentials=cls.CREDS2)
        # Hacemos una solicitud de búsqueda en la lista de reproducción de nuestro canal de YouTube
        request = youtube.videos().list(
            part="snippet",
            id='UCV_g0WY6argVD0LXTFa1n6w',
            # mine=True,
            # playlistId=PLAYLIST_ID,
            maxResults=50
        )
        response = None
        try:
            response = request.execute()
        except HttpError as e:
            print(f'Error en la peticion {e}')
            return False

        if response['items'] == []:
            print(response)
            print(f'No se encontraron items')
            return False
        else:
            # Verificamos si el título del video ya está en la lista de reproducción
            for item in response['items']:
                if item['snippet']['title'] == video_title:
                    print("El video ya ha sido subido.")
                    return True

    @classmethod
    def uploadVid(cls):
        """ Subida del archivo a la cuenta """
        # print(cls.verificarVideoUploaded(cls, video_title=cls.VID_TO_UPLOAD[0]['titulo_video']))
        for vids in cls.VIDEO_PROP:
            if cls.verificarVideoUploaded(cls, video_title=vids['titulo_video']):
                print(f'Preparando peticion ')
                youtube = build('youtube', 'v3', credentials=cls.CREDS)
                video_to_up = MediaFileUpload(
                    vids['ruta_video'], chunksize=-1, resumable=True)
                video_to_up_desc = {
                    'snippet': {
                        'title': vids['titulo_video'],
                        'description': 'video ',
                        'tags': [],
                        'categoryId': ''
                    },
                    'status': {
                        'privacyStatus': 'private'
                    }
                }
                response = None
                try:
                    request = youtube.videos().insert(
                        part='snippet,status',
                        body=video_to_up_desc,
                        media_body=video_to_up
                    )

                    while response is None:
                        estado, response = request.next_chunk()
                        if estado:
                            print(
                                'Subiendo video ', vids['titulo_video'], f': {int(estado.progress() *100)}% completado')

                    print('el video ', vids['titulo_video'],
                          ' se ha subido con exito')
                except HttpError as e:
                    print('Error en subida de video ',
                          vids['titulo_video'], f' - {e}')

                cls.moveVidUploaded(ruta=vids['ruta_video'])
            else:
                print('video ya subido')
                cls.moveVidUploaded(ruta=vids['ruta_video'])

    @classmethod
    def moveVidUploaded(cls, ruta):
        """ Mover video subido """
        print('Moviendo video a subidos ...')
        if os.path.exists(os.path.join(cls.SETTINGS['DIRECTORIO'],'upvid - vidsUploaded')):
            shutil.move(ruta, os.path.join(
                cls.SETTINGS['DIRECTORIO'], 'upvid - vidsUploaded'))
        else:
            os.mkdir('upvid - vidsUploaded')
            cls.moveVidUploaded(ruta=ruta)

    @classmethod
    def dividirVideo(cls, video, video_prop):
        """ Divide el video en dos partes si este es de una duracion mayor o igual a 12 horas """
        parte_1 = None
        parte_2 = None

        mitad = video_prop['duracion'] // 2
        parte_1 = video.subclip(0, mitad)
        parte_2 = video.subclip(mitad)

        titulo_1 = video_prop['titulo_video'] + '_1'
        titulo_2 = video_prop['titulo_video'] + '_2'
        ruta_1 = os.path.join(cls.SETTINGS['DIRECTORIO'], titulo_1 + '.mp4')
        ruta_2 = os.path.join(cls.SETTINGS['DIRECTORIO'], titulo_2 + '.mp4')
        try:
            print(f'Dividiendo videos ... ')
            parte_1.write_videofile(ruta_1)
            parte_2.write_videofile(ruta_2)

            subvid_1 = {
                'ruta_video': ruta_1,
                'titulo_video': titulo_1
            }
            subvid_2 = {
                'ruta_video': ruta_2,
                'titulo_video': titulo_2
            }
            cls.VIDEO_PROP.append(subvid_1)
            cls.VIDEO_PROP.append(subvid_2)
        except Exception as er:
            print(f'Ocurrio un error en la division del video: {er}')
            return False
        return True

    def deleteVideo(cls):
        pass

    @classmethod
    def main(cls):
        """ Metodo principal """
        print('Autenticando ...')
        # upload():
        cls.autenticar()
        print('Buscando Video ...')
        cls.searchVids()
        print('Preparando video ...')
        cls.prepareVid()
            