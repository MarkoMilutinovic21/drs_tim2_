"""
DTO module initialization.
"""
from .user_dto import UserRegistrationDTO, UserUpdateDTO, PasswordChangeDTO, BalanceUpdateDTO
from .auth_dto import LoginDTO, RoleUpdateDTO
from .airline_dto import AirlineCreateDTO, AirlineUpdateDTO

__all__ = [
    'UserRegistrationDTO',
    'UserUpdateDTO',
    'PasswordChangeDTO',
    'BalanceUpdateDTO',
    'LoginDTO',
    'RoleUpdateDTO',
    'AirlineCreateDTO',
    'AirlineUpdateDTO'
]