import xlsxwriter
import os

def putting_list_to_xlxs(db_collection):
    # putting mongodb collection into list
    dict_before = []
    for eachgame in db_collection:
        dict_before.append(eachgame)

    # check if the file gonna be created already exists
    if os.path.exists("gamesales.xlsx"):
        os.remove("gamesales.xlsx")

    # opening gamesales file and input list into an excel sheet
    with xlsxwriter.Workbook('gamesales.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(dict_before):
            worksheet.write_row(row_num, 0, data.values())
            # for columns
            worksheet.set_column(0, 0, 50)
            worksheet.set_column(1, 2, 15)
            worksheet.set_column(3, 3, 80)
            
# data in mongodb is scrapped from psn website.. and adapted to telegram parsing.. got couple of misplaced char          
def cleaning(db_collection):
    new_list = []
    replacable = ('\\-', '\\+', '\\.', '\\)', '\\(')
    for eachdict in db_collection:
        eachdict.pop('_id')
        dict = {}
        dict.update(eachdict)

        for eachvalue in dict.keys():
            if eachvalue is not None:
                executed = False
                is_there = False
                for letter in replacable:
                	
                    if letter in eachdict[eachvalue] and executed == False:
                        executed = True
                        is_there = True
                        dict[eachvalue]=eachdict[eachvalue].replace(letter, letter[1])
                        
                    elif letter in dict[eachvalue] and executed == True:
                        dict[eachvalue]=eachdict[eachvalue].replace(letter, letter[1])
                        
                if is_there == False:
                    dict[eachvalue]=eachdict[eachvalue]

        new_list.append(dict)
    return new_list
