
from ROOT import TFile

# Selector for consecutive samples out of an input TTree

#_____________________________________________________________________________
class ttree_selector:

    #_____________________________________________________________________________
    def __init__(self, infile):

        #open the input
        self.inp = TFile.Open(infile)
        self.tree = self.inp.Get("ltree")

        self.ofs = 0 # offset in input tree

    #_____________________________________________________________________________
    def get_n(self, n, outfile):

        #get a given number 'n' of events and put them to 'outfile'

        #create the output
        out = TFile.Open(outfile, "recreate")

        #subset of 'n' events starting at offset 'ofs'
        otree = self.tree.CopyTree("", "", n, self.ofs)

        #write the tree and close
        otree.Write()
        out.Close()

        #move the offset
        self.ofs += n



