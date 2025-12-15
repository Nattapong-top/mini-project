import os

def loal_menu(filename:str):
    '''
    อ่านไฟล์ menu.txt แล้วคืนค่า list of lists
    ตัวอย่าง return: [['ชานม', 40], ['ชาเขียว', 45]]
    '''
    data = []
    with open(filename, encoding='utf-8') as list_data:
        for line in list_data:
            product, price = line.strip().split(',')
            data.append([product, int(price)])
        return data

menu_list = loal_menu('menu.txt')
print(menu_list)
        
    
def show_menu(menu_list):
    ''' 
    รับ List เมนูร้านชานม ป๋า POS ^_^ _/|\_
    '''
    print('='*30)
    print('     เมนูร้านชานม ป๋า POS ^_^ _/|\_     ')
    print('='*30)
    for i, p in enumerate(menu_list):
        return f'{i+1}. {p}'

print(show_menu(menu_list))
print(len(menu_list))



