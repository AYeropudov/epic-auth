from config import Config


class ActivationService(object):
    @staticmethod
    def send(code, user):
        with open(Config.BASE_DIR + "/activation.txt", "wb") as fo:
            fo.write("{} - {}".format(user.id, code).encode("utf-8"))
