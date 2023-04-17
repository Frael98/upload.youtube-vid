import os
from datetime import datetime
#
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build # Proporciona la interfaz de interaccion con los servicios de google
from googleapiclient.http import MediaFileUpload



class UpVid:
        
    EXT_VID = ['.mp4']
    DIRECTORIO = '' #os.getcwd()

    # Cuenta
    USUARIO = ''
    PASS = ''
    CREDS = None
    
    #
    FILE_TO_UPLOAD = ''
    VIDEOS_PROP = []

    def __init__(cls):
        print(cls)

    def setAccount(cls):
        cls.USUARIO = ''
        cls.PASS = ''

    def setDir(cls, directorio):
        if cls.DIRECTORIO == '':
            print({directorio})
            cls.DIRECTORIO = directorio

    def autenticar(cls):
        if os.path.exists('token.json') :
            cls.CREDS = Credentials.from_authorized_user_file('token.json')
        if not cls.CREDS or not cls.CREDS.valid:
            if cls.CREDS and cls.CREDS.expired and cls.CREDS.refresh_token:
                cls.CREDS.refresh(google.auth.transport.requests.Request()) #
            else :
                flujo = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', scopes = ['https://www.googleapis.com/auth/youtube.upload']
                )
                cls.CREDS = flujo.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(cls.CREDS.to_json())
            
    def uploadVid(cls):
        youtube = build('youtube', 'v3', credentials=cls.CREDS)
        video_to_up = MediaFileUpload(cls.FILE_TO_UPLOAD, chunksize=-1, resumable=True)

        request = youtube.videos().insert()

    def searchVids(cls):
        os.chdir(cls.DIRECTORIO) # setea el directorio
        files = os.listdir()
        """ print(f'Archivos del dir') """
        print(files)
        vids = []
        for f in files:
            name, _ext = os.path.splitext(f)
            if _ext in cls.EXT_VID:
                vids.append(f)
        if vids == []:
            print('No videos to upload!')
        else:
            cls.searchCurrenVid(vids)
                

    def searchCurrenVid(cls, vids):
        for v in vids:
            prop = os.stat(v)
            #print(f'Fecha del vid {datetime.fromtimestamp(prop.st_ctime).strftime("%d/%m/%y")}')
            fechaVid = datetime.fromtimestamp(prop.st_ctime).strftime("%d/%m/%Y")
            actualFecha = datetime.now().strftime("%d/%m/%y")
            #print(fechaVid)
            if fechaVid == actualFecha:
                cls.FILE_TO_UPLOAD = v
                #cls.VIDEOS_PROP = os.stat(v)
                print(cls.FILE_TO_UPLOAD)

    def prepareVid(cls):
        if cls.FILE_TO_UPLOAD == '':
            print('Not vid to upload')
            return

        ruta_video = os.path.join(os.getcwd(), cls.FILE_TO_UPLOAD)
        titulo_video = os.path.basename(os.path.join(os.getcwd, cls.FILE_TO_UPLOAD))

    def main(cls):
        print()
        #upload():
        cls.searchVids()