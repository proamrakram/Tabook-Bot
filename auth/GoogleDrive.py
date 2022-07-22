# Google Drive Uploading Lib
from .Google import Create_Service

class GoogleDrive:

    def get_google_drive_services():
        # Google Drive Config
        Client_secret_file = "G:/Python/Django/TelegramBot/auth/auth.json"
        Api_Name = "drive"
        Api_Version = "V3"
        Scopes = [
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        services = Create_Service(Client_secret_file, Api_Name, Api_Version, Scopes)
        return services
