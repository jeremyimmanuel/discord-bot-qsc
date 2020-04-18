import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]

# You can get your own creds.json from your Google Cloud Console
# make sure you have the Google Drive and Google Sheets API enabled
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("Staff Log in").sheet1

'''
Constants for column number
NAME DATE CHECK-IN-TIME CHECK-OUT-TIME WORK-DURATION
'''
NAME, DATE, CHECKIN, CHECKOUT, WORKDUR = 1, 2, 3, 4, 5

def check_in_staff(name: str):
    global creds
    client = gspread.authorize(creds)
    sheet = client.open("Staff Log in").sheet1

    target_row = len(sheet.get_all_records()) + 2
    if target_row > sheet.row_count:
        sheet.add_rows(10)
    now = datetime.datetime.now()
    
    
    d = gspread.utils.rowcol_to_a1(target_row, DATE)
    sheet.format(d, {
        'numberFormat' : {
            'type' : 'DATE',
            'pattern' : 'mm/dd/yyyy'
        }
    })
    ci = gspread.utils.rowcol_to_a1(target_row, CHECKIN)
    sheet.format(ci, {
         'numberFormat' : {
            'type' : 'TIME',
            'pattern' : 'hh:mm am/pm'
        }
    })

    co = gspread.utils.rowcol_to_a1(target_row, CHECKOUT)
    # =IF(ISBLANK(D32), "", D32-C32)

    dur = gspread.utils.rowcol_to_a1(target_row, WORKDUR)
    durVal = f'=IF(ISBLANK({co}), "", {co}-{ci})'

    values = [name, now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S'), '', durVal]
    sheet.insert_row(values, target_row, value_input_option='USER_ENTERED')

def check_out_staff(name: str):
    global creds
    client = gspread.authorize(creds)
    sheet = client.open("Staff Log in").sheet1
    
    cells = sheet.findall(name)

    cell = cells[-1]
    
    now = datetime.datetime.now()
    target_row = cell.row
    val = now.strftime('%H:%M:%S')
    # sheet.format()
    ci = gspread.utils.rowcol_to_a1(target_row, CHECKIN)
    co = gspread.utils.rowcol_to_a1(target_row, CHECKOUT)
    sheet.format(co, {
         'numberFormat' : {
            'type' : 'TIME',
            'pattern' : 'hh:mm am/pm'
        }
    })
    # dur = gspread.utils.rowcol_to_a1(target_row, WORKDUR)
    # sheet.format(dur, {
    #      'numberFormat' : {
    #         'type' : 'TIME',
    #         'pattern' : '[hh]:[mm]'
    #     }
    # })
    # cell_list = sheet.range(f'{co}:{dur}')
    # cell_list[0].value = val
    # cell_list[1].value = f'={co}-{ci}'

    # sheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    sheet.update_cell(target_row, CHECKOUT, val)
    # sheet.update_cell(target_row, WORKDUR, f'={co}-{ci}')
    
    


# data = sheet.get_all_records()
# print(data)
# target_row = len(data) + 2
# sheet.insert_row(["antoher", datetime.datetime().now(), 11], target_row)

# row = sheet.row_values(1)
# print(row)
# # print(f'{sheet.row_count}')
# cell = sheet.findall('Jeremy')[-1]

# print(f'row : {cell.row}; col : {cell.col}')