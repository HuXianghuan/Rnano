import seq_tools
class Element:

    def __init__(self, id=None, length=None, sequence=None):
        self.id = str(id)
        self.length = length
        self.sequence = sequence

    def render_sequence(self):
        raise NotImplementedError(f"{self.__class__.__name__} did not implemented render_sequence")
class SingleElement(Element):

    def __init__(self):
        super().__init__()


class PairedElement(Element):

    def __init__(self, pair_id):
        super().__init__()
        self.pair_id = pair_id

class StrictPairedElement(PairedElement):
    pass

class TetraU(SingleElement):
    pass

class HairpinLoop(SingleElement):
    pass






class KissingLoop(PairedElement):
    pass
class GCPair(StrictPairedElement):
    pass

class UU(StrictPairedElement):
    pass
class AA(StrictPairedElement):
    pass




class SenseSirna(StrictPairedElement):
    pass



class AntiSenseSirna(StrictPairedElement):
    pass

