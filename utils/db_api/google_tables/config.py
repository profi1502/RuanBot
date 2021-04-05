from __future__ import print_function
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

gc = gspread.service_account(filename='credentials.json')
