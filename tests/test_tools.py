from jarvis_tools import (
    open_application,
    open_folder,
    create_folder,
    get_time
)


print(get_time())

print(open_application("notepad"))

print(create_folder(r"C:\Jarvius\Test"))

print(open_folder(r"C:\Jarvius\Test"))