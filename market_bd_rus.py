import re
import csv
import chardet
import xlrd
from prettytable import PrettyTable


class CreateBD:
    def __init__(self):
        pass

# Make a dict scv with right encoding
    def make_goods_dict(self, file1_name=None, file2_name=None, encoding='Windows-1251'):
        '''That function make csv file with utf8 encoding from other encoding.
        file1_name - track of the file with some encoding; file2_name - track of new file
        field_names - list of field names; encoding - encoding of first file'''
        data_aux = []
        with open(file1_name, 'r', encoding=encoding) as file:
            reader = csv.reader(file, delimiter=',')
            field_names = next(reader)
            for line in reader:
                data_aux.append(line)
        self.make_dict_csv_file(file_name=file2_name, field_names=field_names, data=data_aux)

# Make a dict csv from a matrix
    def make_dict_csv_file(self, file_name=None, field_names=None, data=None):
        '''That function make csv dict file from matrix (list of lists).
        file_name - track of creating file; field_names - list of field names; data - matrix with data'''
        field_names = self.edit_text(text_row=field_names)
        with open(file_name, 'w', newline="") as new_csv:
            csv_writer = csv.DictWriter(new_csv, delimiter=',', fieldnames=field_names)
            csv_writer.writeheader()
            for row_aux in data:
                row_aux = self.edit_text(text_row=row_aux)
                row = dict(zip(field_names, row_aux))
                csv_writer.writerow(row)
# Edition the text
    def edit_text(self, text_row=None):
        '''That function edition the text; text_row - the list of the texts'''
        new_text_row = []
        for text in text_row:
            try:
                text = re.sub('\n', ' ', text)
                text = text.lower()
            except:
                pass
            new_text_row.append(text)
        return new_text_row



# Make a csv from xls
    def from_xls_to_csv(self, file_name=None, sheet_name=None, csv_file_name=None):
        '''That function read whole data from one sheet of xls document and make csv file from that data.
        first row in this sheet is fieldname.
        file_name - track of xls file; sheet_name - name of sheet; csv_file_name -  track of creating file'''
        rb = xlrd.open_workbook(file_name)
        sheet = rb.sheet_by_name(sheet_name)
        main_data = []
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            sub_data = []
            for c_el in row:
                sub_data.append(c_el)
            main_data.append(sub_data)
        self.make_dict_csv_file(file_name=csv_file_name, field_names=main_data[0], data=main_data[1:])

# Make a pretty table from csv
    def make_table_from_csv(self, file_name=None):
        '''That function make and show pretty table from data from dict csv file.
        file_name - name of csv file; field_names - list of field names'''
        table = PrettyTable()
        with open(file_name) as file:
            reader = csv.DictReader(file, delimiter=',')
            field_names = reader.fieldnames
            table.field_names = field_names
            for line in reader:
                table_line = [line[name] for name in field_names]
                table.add_row(table_line)
        print(table)

# Add features to BD
    def addition_of_bds(self, file1_name=None, file2_name=None, field_name_compare=None, field_names_for_add=None, new_file_name=None):
        '''That function addition two BD, communicating by one common feature.
        file1_name - name of main file; file2_name - name of file with addition info
        field1_names - list of field names in main csv; field2_names-  list of field names of auxiliary csv'''
        data1 = []
        with open(file1_name) as file:
            reader = csv.DictReader(file, delimiter=',')
            feild_names1 = reader.fieldnames
            for row in reader:
                data1.append(row)
        data2 = []
        with open(file2_name) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                data2.append(row)
        new_data = []
        new_field_name= ''
        for name in field_names_for_add:
            new_field_name = new_field_name + name
        for row1 in data1:
            aux_data = []
            for row2 in data2:
                if row1[field_name_compare] == row2[field_name_compare]:
                    aux_data.append({field_name_for_add: row2[field_name_for_add] for field_name_for_add in field_names_for_add})
            row1.update({new_field_name:aux_data})
            new_data.append(row1)
        print(feild_names1)
        print(field_names_for_add)
        field_names = feild_names1 + field_names_for_add
        print(field_names)
        with open(new_file_name, 'w', newline="") as new_csv:
            csv_writer = csv.DictWriter(new_csv, delimiter=',', fieldnames=field_names)
            csv_writer.writeheader()
            for row in new_data:
                csv_writer.writerow(row)



class AnalysisBD:
    def __init__(self):
        pass

# Choose category from ОКВЭД2 dict csv
    def read_dict_scv(self, file_name=None, field_names=None):
        with open(file_name) as file:
            reader = csv.DictReader(file, delimiter=',')
            data_main = []
            for line in reader:
                data_main.append(line)
        # choose section
        for line in data_main:
            if len(line['code']) == 1:
                print(line['section'] + ': ' + line['name'])
        section = input('Choose the section and put it Letter: ')
        # remember section
        data_section = []
        for line in data_main:
            if line['section'] == section:
                data_section.append(line)
        # code clarification
        code = ''
        self.show_list(data=data_section, name='code', var=code, num='2')
        code_1 = input('Choose section and put two number: ')
        code = code + code_1 + '.'
        self.show_list(data=data_section, name='code', var=code, num='1')
        if self.check == 0:
            return self.save_line(data=data_section, name='code', var=code[:-3], num='2')
        code_2 = input('Choose section and put one number: ')
        code = code + code_2
        self.show_list(data=data_section, name='code', var=code, num='1')
        if self.check == 0:
            return self.save_line(data=data_section, name='code', var=code[:-1], num='1')
        code_3 = input('Choose section and put one number: ')
        code = code + code_3 + '.'
        self.show_list(data=data_section, name='code', var=code, num='1')
        if self.check == 0:
            return self.save_line(data=data_section, name='code', var=code[:-2], num='1')
        code_4 = input('Choose section and put one number: ')
        code = code + code_4
        self.show_list(data=data_section, name='code', var=code, num='1')
        if self.check == 0:
            return self.save_line(data=data_section, name='code', var=code[:-1], num='1')
        code_5 = input('Choose section and put one number: ')
        code = code + code_5
        self.show_list(data=data_section, name='code', var=code, num='1')
        if self.check == 0:
            return self.save_line(data=data_section, name='code', var=code[:-1], num='1')

    def show_list(self, data=None, name=None, var=None, num=None):
        expression = re.compile('^'+var+'[0-9]{'+num+'}$')
        self.check = 0
        for line in data:
            if re.search(expression, line[name]):
                self.check += 1
                print(line[name] + ': ' + line['name'])
        if self.check == 0:
            print("It's last branch")

    def save_line(self, data=None, name=None, var=None, num=None):
        last_num = input('Choose the section and put ' + num + ' number: ')
        code = var + last_num
        for line in data:
            if line[name] == code:
                print(line['section'] + '.' + line['code'] + ': ' + line['name'])





