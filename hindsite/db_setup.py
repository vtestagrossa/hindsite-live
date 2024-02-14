"""
Back-end variables to set up database interactions.
"""

from sqlalchemy import Table, Column, ForeignKey
from typing_extensions import Annotated
import sqlalchemy.orm
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):  # pylint: disable=too-few-public-methods
    """
    The base model for the classes to be declared.
    """


# Defines association table for the User/Group relationship
user_membership = Table(
    'user_membership',
    Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True)
)

# pylint: disable=invalid-name
intpk = Annotated[int, sqlalchemy.orm.mapped_column(primary_key=True,
                                                    autoincrement=True)]
