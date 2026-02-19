from .nanoparticles import Nanoparticle
from elements import *
from collections import defaultdict

class ThreeWayJunction(Nanoparticle):
    def __init__(self, gc_clasp_length=1, overhang_length=2):
        super().__init__()

        self.overhang_length = int(overhang_length)
        self.gc_clasp_length = int(gc_clasp_length)

        self.structure = [
            GCPair(pair_id="g_1"),

            AA(pair_id="o_1"),
            AntiSenseSirna(pair_id=1),


            GCPair(pair_id="g_2"),
            TetraU(),
            GCPair(pair_id="g_3"),

            SenseSirna(pair_id=2),
            UU(pair_id="o_2"),

            GCPair(pair_id="g_4"),
            HairpinLoop(),
            GCPair(pair_id="g_4"),

            AA(pair_id="o_2"),
            AntiSenseSirna(pair_id=2),

            GCPair(pair_id="g_3"),
            TetraU(),
            GCPair(pair_id="g_5"),

            SenseSirna(pair_id=3),
            UU(pair_id="o_3"),

            GCPair(pair_id="g_6"),
            HairpinLoop(),
            GCPair(pair_id="g_6"),

            AA(pair_id="o_3"),
            AntiSenseSirna(pair_id=3),

            GCPair(pair_id="g_5"),
            TetraU(),
            GCPair(pair_id="g_2"),


            SenseSirna(pair_id=1),
            UU(pair_id="o_1"),

            GCPair(pair_id="g_1")
        ]

        self.count_elements()

    @property
    def siRNA_list(self):
        return self.get_element_list(clazz=SenseSirna)

    @siRNA_list.setter
    def siRNA_list(self, lst):
        self.set_element_list(clazz=SenseSirna, lst=lst)

    @property
    def hairpin_list(self):
        return self.get_element_list(clazz=HairpinLoop)

    @hairpin_list.setter
    def hairpin_list(self, lst):
        self.set_element_list(clazz=HairpinLoop, lst=lst)

    def render_sequence(self):

        siRNA_list = self.siRNA_list.copy()
        hairpin_list = self.hairpin_list.copy()


        map = defaultdict(list)

        for e in self.structure:
            map[type(e)].append(e)

        for element in map[TetraU]:  # type: TetraU
            element.sequence = "UUUU"
            element.length = 4

        for element in map[HairpinLoop]:  # type: HairpinLoop
            seq = hairpin_list.pop()
            element.sequence = seq
            element.length = len(seq)

        for element in map[SenseSirna]:  # type: SenseSirna
            pair_id = element.pair_id
            seq = siRNA_list.pop()
            element.sequence = seq
            element.length = len(seq)

            anti_seq = seq_tools.complementary_seq(seq_tools.reversed_seq(seq))
            for element in map[AntiSenseSirna]:  # type: AntiSenseSirna
                if element.pair_id == pair_id:
                    element.sequence = anti_seq
                    element.length = len(anti_seq)



        for element in map[GCPair]:  # type: GCPair
            id = element.pair_id
            if element.sequence is not None:
                continue
            seq = seq_tools.generate_random_seq(length=self.gc_clasp_length, probs={'G': 0.5, 'C': 0.5})
            element.sequence = seq
            element.length = len(seq)
            anti_seq = seq_tools.complementary_seq(seq_tools.reversed_seq(seq))

            for element in map[GCPair]:  # type: GCPair
                if element.sequence is not None:
                    continue
                if element.pair_id == id:
                    element.sequence = anti_seq
                    element.length = len(anti_seq)

        for element in map[AA]:
            element.sequence = "A" * self.overhang_length
            element.length = self.overhang_length

        for element in map[UU]:
            element.sequence = "U" * self.overhang_length
            element.length = self.overhang_length

        self.check_element_sequence()

        res = "".join(element.sequence for element in self.structure)
        self.sequence = res

        return res