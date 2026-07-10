from rv.core.tui.colors import blue,green,yellow,red

APP_NAME = "rv"

PROCEED_QUESTION_MESSAGE = "Do you still want to proceed ? Y/n : "

def LOG(message : str,color = blue)->None:
    print(f"[{color(APP_NAME)}]: {message}")

def LOG_WARNING(message : str)->None:
    LOG(message,yellow)

def LOG_ERROR(message : str)->None:
    LOG(message,red)

def LOG_DEV(message : str,color = blue)->None:
    print(f'[{color(APP_NAME)}] <{color("DEV")}> : {message}')

def LOG_DEV_WARNING(message : str) -> None:
    LOG_DEV(message,yellow)

def LOG_DEV_INFO(message : str) -> None:
    LOG_DEV(message,green)

def MODULE_NOT_FOUND_MESSAGE(module_name : str) -> str:
    return f"'{module_name}' is not an {APP_NAME} command. See '{APP_NAME} --help'\n\nIt may be because the associated module can not be found."

def MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(module_name : str) -> str:    return f"{APP_NAME}: the entrypoint of the module associated to '{module_name}' can not be found."

SYSTEM_CALL_ERROR_MESSAGE = "An error occured during a system call."

def PATH_DOES_NOT_EXIST_MESSAGE(path : str) -> str:
    return f"The following path does not exist : {path}"