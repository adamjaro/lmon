
#read parameters from config parser

from configparser import RawConfigParser

#_____________________________________________________________________________
class read_con:
    #_____________________________________________________________________________
    def __init__(self, config):

        self.con = RawConfigParser(inline_comment_prefixes=(";","#"))
        self.con.read(config)

    #_____________________________________________________________________________
    def __call__(self, par):

        return self.con.getfloat("main", par)

    #_____________________________________________________________________________
    def str(self, par):

        return self.con.get("main", par).strip("\"'")

    #_____________________________________________________________________________
    def int(self, par):

        return self.con.getint("main", par)


