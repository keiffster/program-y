
class Group(object):

    def __init__(self, groupid):
        self._groupid = groupid
        self._roles = []
        self._groups = []

    @property
    def groupid(self):
        return self._groupid

    @property
    def roles(self):
        return self._roles

    def available_roles(self):
        roles = self._roles[:]
        for group in self._groups:
            roles += group.available_roles()
        return roles

    def has_role(self, role):
        return bool(role in self._roles)

    @property
    def groups(self):
        return self._groups

    def has_group(self, groupid):
        for group in self._groups:
            if groupid == group.groupid:
                return True
            else:
                return group.has_group(groupid)
        return False


class User(object):

    def __init__(self, userid):
        self._userid = userid
        self._roles = []
        self._groups = []

    @property
    def userid(self):
        return self._userid

    @property
    def roles(self):
        return self._roles

    def available_roles(self):
        roles = self._roles[:]
        for group in self._groups:
            roles += group.available_roles()
        return roles

    def has_role(self, role):
        if role in self._roles:
            return True
        else:
            for group in self._groups:
                if group.has_role(role):
                    return True
            return False

    @property
    def groups(self):
        return self._groups

    def has_group(self, groupid):
        for group in self._groups:
            if groupid == group.groupid:
                return True
            else:
                return group.has_group(groupid)
        return False
