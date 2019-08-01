import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

         
def next_available_row(worksheet):
    str_list = list(filter(None, sheet.col_values(1)))
    return str(len(str_list)+1)

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

client = gspread.authorize(credentials)

sheet = client.open("prices").sheet1

# before
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)


next_row = next_available_row(sheet)

sheet.update_cell(next_row, 1, "teste store")
sheet.update_cell(next_row, 2, "teste price")


# after
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)


