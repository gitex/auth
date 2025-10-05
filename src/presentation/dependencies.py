from typing import Annotated

from fastapi import Depends

from src.application.login import LoginHandler, get_login_handler


LoginHandlerDepend = Annotated[LoginHandler, Depends(get_login_handler)]
