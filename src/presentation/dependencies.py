from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application import LoginService, RegisterService

from src.bootstrap.wiring import AuthContainer


LoginServiceDepend = Annotated[
    LoginService,
    Depends(Provide[AuthContainer.login_service]),
]
RegisterServiceDepend = Annotated[
    RegisterService,
    Depends(Provide[AuthContainer.register_service]),
]
