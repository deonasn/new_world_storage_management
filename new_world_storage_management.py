import os
import time
import sys
import ctypes
from screeninfo import get_monitors as getmon
import select
import msvcrt
from pathlib import Path

def terminal_window():
    os.system('mode con: cols=120 lines=30')
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    monitors = getmon()
    if len(monitors) > 1:
        monitor = monitors[1]
    else:
        monitor = monitors[0]

    monitor_left = monitor.x
    monitor_top = monitor.y
    monitor_width = monitor.width
    monitor_height = monitor.height

    console_width = 120 * 8
    console_height = 30 * 16

    left = monitor_left + (monitor_width - console_width) // 2
    top = monitor_top + (monitor_height - console_height) // 2

    hwnd = kernel32.GetConsoleWindow()

    SWP_NOSIZE = 0x0001
    ctypes.windll.user32.SetWindowPos(hwnd, 0, left, top, 0, 0, SWP_NOSIZE)

def display_intro():
    intro = ('\n\n\n\n\n\n'
             '\n\t\t\t\t\t  ----------------------------------'
             '\n\t\t\t\t\t ///////////////////////////////////|'
             '\n\t\t\t\t\t----------------------------------  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||           Welcome            ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||          New World           ||  |'
             '\n\t\t\t\t\t||      Storage Management      ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t||                              ||  |'
             '\n\t\t\t\t\t-------------------------------------'
             '\n\t\t\t\t\t-------------------------------------\n')
    print(intro)
    time.sleep(4)

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
        while msvcrt.kbhit():
            _ = msvcrt.getch()
    else:
        _ = os.system('clear')
        while select.select([sys.stdin], [], [], 0)[0]:
            _ = sys.stdin.read(1)

def working_directory():
    working_directory = Path(r"D:\Documents\New World")
    return working_directory

def initialize_program():
    current_dir = working_directory()
    nw_sdata_matches = list(current_dir.rglob('*_nw_sdata.txt'))
    nw_sdata_number = len(nw_sdata_matches)
    if len(nw_sdata_matches) == 0:
        print('\n\n\n\n\n\n\n\n\n\n\n\t\tNo New World Storage data files found. Must have 1 file present in the working directory')
        time.sleep(2.5)
        clear_screen()
        display_goodbye_message()
    elif len(nw_sdata_matches) >= 1:
        while True:
            print(f"\n\n\n\n\n\n\n\n\n\t\t\t\t\t{len(nw_sdata_matches)} New World Storage data files found:\n")
            for i in range(len(nw_sdata_matches)):
                print(f"\t\t\t\t\t      {i+1} : {nw_sdata_matches[i].name}")
            try:
                nw_sdata_choice = int(input('\n\n\n\t\t\t\t      Please choose which file you want to use: '))
                if 1 <= nw_sdata_choice <= nw_sdata_number:
                    nw_sdata_file_path = nw_sdata_matches[nw_sdata_choice - 1]
                    nw_sdata_file_name = nw_sdata_matches[int(nw_sdata_choice) - 1].name
                    # print(nw_sdata_file_path)
                    return nw_sdata_file_name
                else:
                    if nw_sdata_number == 1:
                        print(f'\n\n\n\t\t\t\t\t     Please enter 1 to proceed!')
                    else:
                        print(f'\n\n\n\t\t\t\t        Please enter a number between 1 and {nw_sdata_number}!')
                    time.sleep(2)
                    clear_screen()
            except ValueError:
                if nw_sdata_number == 1:
                    print(f'\n\n\n\t\t\t\t\t     Please enter 1 to proceed!')
                else:
                    print(f'\n\n\n\t\t\t\t        Please enter a number between 1 and {nw_sdata_number}!')
                time.sleep(2)
                clear_screen()

def read_file():
    storage_dict = {}
    storage_types = []
    storage_places = []
    global continue_status

    current_dir = working_directory()
    input_file_name = nw_sdata_file_name
    input_file_path = str(current_dir) + '\\' + input_file_name

    nw_sdata_file = open(input_file_path, 'r+')

    input_file_char_name = input_file_name.removesuffix('_nw_sdata.txt')

    char_name = nw_sdata_file.readline().strip("Character Name - ").strip()

    if input_file_char_name != char_name:
        print("\n\n\n\n\n\n\n\n\n\n\t\t\t\t\t\tWrong character name!\n\n")
        print(f"\t\t\t\t\tIn-file Character Name - '{char_name}'.\n\n")
        print(f"\t\t\t\t   Please look into the New World Storage Data File!")
        time.sleep(3)
        continue_status = False
        clear_screen()

    nw_sdata_file.readline()

    for line in nw_sdata_file:
        storage = line.strip().split(' - ')
        storage_type = storage[0].strip()

        storage_types.append(storage_type)

        if ',' in storage[1]:
            storage_place = storage[1].split(', ')
        else:
            storage_place = storage[1]

        storage_places.append(storage_place)

        storage_dict[storage_type] = storage_place

    nw_sdata_file.close()
    return storage_dict, storage_types

def display_storage_type(storage_types):
    storage_types = storage_types
    # number_storage_types = 0

    while True:
        number_storage_types = 0
        print("\n\n\n")
        print("\t\t\t\t\t          STORAGE TYPES\n"
              "\t\t\t\t\t         ---------------\n")

        for i in range(len(storage_types)):
            print(f"\t\t\t\t\t         {i+1}\t:   {storage_types[i]}")
            number_storage_types += 1


        try:
            storage_type_number_choice = int(input(f"\n\n\t\t\t\t     Please enter the type of storage you want (1:{number_storage_types}): "))
            if 1 <= storage_type_number_choice <= number_storage_types:
                break
            else:
                print(f"\n\n\t\t\t\t       Please enter an integer number between 1 and {number_storage_types}!")
                time.sleep(2)
                clear_screen()
        except ValueError:
            print(f"\n\n\t\t\t\t       Please enter an integer number between 1 and {number_storage_types}!")
            time.sleep(2)
            clear_screen()

    storage_type_choice = storage_types[int(storage_type_number_choice) - 1]

    return storage_type_choice

def display_storage_place(storage_dict, storage_type_choice):
    storage_type = storage_type_choice

    print("\n\n\n\n\n\n\n")
    print(f"\t\t\t\t\t\tStorage Type: {storage_type}")
    print("\t\t\t\t\t----------------------------------------\n\n")

    if storage_type in storage_dict.keys():
        storage_places = storage_dict[storage_type]
        if isinstance(storage_places, str):
            storage_places = [storage_places]
        for i in range(len(storage_places)):
            print(f"\t\t\t\t\t           {i+1} : {storage_places[i]}")

    print("\n")

def display_goodbye_message():
    goodbye_message = ('\n\n\n\n\n\n\n\n\n\n\n'
                       '\n\t\t\t\t    Thank you for using New World Storage Management!\n')
    print(goodbye_message)
    time.sleep(4)
    sys.exit()

if __name__ == '__main__':
    terminal_window()
    display_intro()
    clear_screen()

    nw_sdata_file_name = initialize_program()
    clear_screen()

    continue_status = True

    while continue_status:
        storage_dict, storage_types = read_file()
        storage_type_choice = display_storage_type(storage_types)
        clear_screen()

        while True:
            display_storage_place(storage_dict, storage_type_choice)
            continue_choice = input("\n\n\n\t\t\t\t\t    Do you want to continue (Y/N): ").strip().capitalize()
            if continue_choice == 'Y':
                continue_status = True
                break
            elif continue_choice == 'N':
                continue_status = False
                break
            else:
                print("\n\n\t\t\t\t\t   Invalid Entry. Enter either Y or N")
                time.sleep(2)
            clear_screen()

        clear_screen()

    display_goodbye_message()