from openpyxl import load_workbook
import openpyxl
from openpyxl import Workbook
import os

km_var = 0.40
filename_main = "{}\jogos_excel.xlsx".format(os.getcwd())
wb_main = load_workbook(filename_main)
wb_main['Tabela de prémios']['B14'].value = 0.40


wb_main.save(filename_main)
