# Google Sheet Lib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:

    def get_sheet(self):
        
        # Google Sheet Scopes
        
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
    
        creds = ServiceAccountCredentials.from_json_keyfile_name("G:/Python/Django/TelegramBot/auth/sheets.json", scope)
        
        client = gspread.authorize(creds)
        
        sheet = client.open("Tabook").sheet1  # Open the spreadhseet
                
        return sheet



# class GoogleSheet:
    
#     scope =[
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive",
#             "https://www.googleapis.com/auth/drive.file",
#             "https://www.googleapis.com/auth/drive.readonly",
#             "https://www.googleapis.com/auth/spreadsheets.readonly",
#             "https://www.googleapis.com/auth/spreadsheets",
#     ]

#     def __init__(self) -> None:
#         self.sheet = self.open_sheet(0)

#     def scope_valuse(self):
#         return self.scope

#     def create_credentials(self):
#         creds = ServiceAccountCredentials.from_json_keyfile_name("G:/Python/Django/Test/auth/sheets.json", self.scope)
#         return creds

#     def authorize_creds(self):
#         client = gspread.authorize(self.create_credentials())
#         return client

#     def open_sheet(self,sheet_number):
#         sheet = self.authorize_creds().open("Tabook")
#         return sheet.get_worksheet(sheet_number)
    
#     def numbers_list(self):
#         list = self.sheet.col_values(1)
#         return list 
    
#     def update_cell(self,row,col,value):
#         self.sheet.update_cell(row, col,value)

