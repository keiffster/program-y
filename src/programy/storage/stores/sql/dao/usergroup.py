"""
users:
  console:
    roles:
      user
    groups:
      sysadmin

groups:
  sysadmin:
    roles:
      root, admin, system
    groups:
      user

  user:
    roles:
      ask

"""

from sqlalchemy import Column, Integer, String

from programy.storage.stores.sql.base import Base


class AuthoriseUser(Base):
    __tablename__ = 'authusers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return ""


class UserRole(Base):
    __tablename__ = 'userroles'

    id = Column(Integer, primary_key=True)
    user =  Column(String)
    role = Column(String)

    def __repr__(self):
        return ""


class UserGroup(Base):
    __tablename__ = 'usergroups'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    group = Column(String)

    def __repr__(self):
        return ""


class AuthoriseGroup(Base):
    __tablename__ = 'authgroups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent = Column(String, nullable=True)

    def __repr__(self):
        return ""


class GroupRole(Base):
    __tablename__ = 'grouproles'

    id = Column(Integer, primary_key=True)
    group = Column(String)
    role = Column(String)

    def __repr__(self):
        return ""


class GroupUser(Base):
    __tablename__ = 'groupusers'

    id = Column(Integer, primary_key=True)
    group = Column(String)
    user = Column(String)

    def __repr__(self):
        return ""
