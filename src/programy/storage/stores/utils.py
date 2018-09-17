
class DAOUtils(object):

    NOT_APPLIC = "n/a"

    @staticmethod
    def get_value_from_data(data, name):
        if name in data:
            return data[name]
        return None

    @staticmethod
    def valid_id(id):
        if id is not None:
            return str(id)
        return DAOUtils.NOT_APPLIC