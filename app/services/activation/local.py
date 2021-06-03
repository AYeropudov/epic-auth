from config import Config


class ActivationService(object):
    @staticmethod
    def send(code, user):
        with open(Config.BASE_DIR + "/activation.txt", "a") as fo:
            fo.write("\n{} # {} # {}".format(user.id, user.email, code))
