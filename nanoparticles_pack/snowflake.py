from .nanoparticles import Nanoparticle
from elements import *
from collections import defaultdict
import copy


class Snowflake(Nanoparticle):
    def __init__(self, extra_edge=1, overhang_length=2, gc_clasp_length=2):
        super().__init__()

        self.overhang_length = int(overhang_length)
        self.gc_clasp_length = int(gc_clasp_length)

        foundation = [
            AntiSenseSirna(pair_id=1),

            TetraU(),
            SenseSirna(pair_id=2),
            HairpinLoop(),
            AntiSenseSirna(pair_id=2),
            TetraU(),

            "attachment1",

            # kissing edge
            SenseSirna(pair_id=3),
            KissingLoop(pair_id=0),
            AntiSenseSirna(pair_id=3),

            "attachment2",

            TetraU(),
            SenseSirna(pair_id=1),
            AntiSenseSirna(pair_id=4),
            TetraU(),
            # kissing
            SenseSirna(pair_id=5),
            KissingLoop(pair_id=0),
            AntiSenseSirna(pair_id=5),
            TetraU(),
            SenseSirna(pair_id=6),
            HairpinLoop(),
            AntiSenseSirna(pair_id=6),
            TetraU(),

            SenseSirna(pair_id=4)
        ]

        motif1 = [
            SenseSirna(pair_id=None),
            AntiSenseSirna(pair_id=None),
            TetraU(),
            SenseSirna(pair_id=None),
            HairpinLoop(),
            AntiSenseSirna(pair_id=None),
            TetraU(),
        ]

        motif2 = [
            TetraU(),
            SenseSirna(pair_id=None),
            AntiSenseSirna(pair_id=None),
        ]

        attachment1 = []
        attachment2 = []
        for i in range(extra_edge):
            a = copy.deepcopy(motif1)
            b = copy.deepcopy(motif2)
            a[0].pair_id = f"m{i}"
            b[2].pair_id = f"m{i}"

            a[1].pair_id = f"n{i}"
            b[1].pair_id = f"n{i}"

            a[3].pair_id = f"p{i}"
            a[5].pair_id = f"p{i}"

            attachment1 = attachment1 + a
            attachment2 = b + attachment2

        index1 = foundation.index("attachment1")
        foundation[index1:index1 + 1] = attachment1

        index2 = foundation.index("attachment2")
        foundation[index2:index2 + 1] = attachment2

        structure_with_gc = []
        partial_gc_counter = 0

        for idx, element in enumerate(foundation):
            if isinstance(element, (KissingLoop, HairpinLoop)):

                structure_with_gc.extend([
                    GCPair(pair_id=f"gc_{partial_gc_counter}"),
                    element,
                    GCPair(pair_id=f"gc_{partial_gc_counter}")
                ])

                partial_gc_counter += 1
            elif isinstance(element, TetraU):
                previous_stem_id = foundation[idx - 1].pair_id
                next_stem_id = foundation[idx + 1].pair_id

                structure_with_gc.extend([
                    GCPair(pair_id=f"gcs_{previous_stem_id}"),
                    element,
                    GCPair(pair_id=f"gcs_{next_stem_id}")
                ])
            else:
                structure_with_gc.append(element)

        foundation = structure_with_gc

        structure_with_overhang = []

        for element in foundation:
            if isinstance(element, SenseSirna):
                id = element.pair_id
                structure_with_overhang.extend([
                    element,
                    UU(pair_id=f"oh_{id}")
                ])
            elif isinstance(element, AntiSenseSirna):
                id = element.pair_id
                structure_with_overhang.extend([
                    AA(pair_id=f"oh_{id}"),
                    element
                ])
            else:
                structure_with_overhang.append(element)

        foundation = structure_with_overhang

        self.structure = foundation
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

    @property
    def kisspair_list(self):
        return self.get_element_list(clazz=KissingLoop)

    @kisspair_list.setter
    def kisspair_list(self, lst):
        self.set_element_list(clazz=KissingLoop, lst=lst,
                              required_length=int(self.element_counts.get(KissingLoop, 0) / 2))

    def render_sequence(self):

        siRNA_list = self.siRNA_list.copy()
        hairpin_list = self.hairpin_list.copy()
        kiss_list = self.kisspair_list.copy()

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

        for element in map[KissingLoop]:  # type: KissingLoop
            if element.sequence is not None:
                continue
            pair_id = element.pair_id
            pair_seq_list = list(kiss_list.pop())

            seq = pair_seq_list.pop()
            element.sequence = seq
            element.length = len(seq)

            for element in map[KissingLoop]:  # type: KissingLoop
                if element.sequence is not None:
                    continue
                if element.pair_id == pair_id:
                    seq = pair_seq_list.pop()
                    element.sequence = seq
                    element.length = len(seq)

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


class Triangle(Snowflake):
    def __init__(self, overhang_length=2, gc_clasp_length=2):
        super().__init__(extra_edge=1,
                         overhang_length=overhang_length,
                         gc_clasp_length=gc_clasp_length)

class Square(Snowflake):
    def __init__(self, overhang_length=2, gc_clasp_length=2):
        super().__init__(extra_edge=2,
                         overhang_length=overhang_length,
                         gc_clasp_length=gc_clasp_length)



class Pentagon(Snowflake):
    def __init__(self, overhang_length=2, gc_clasp_length=2):
        super().__init__(extra_edge=3,
                         overhang_length=overhang_length,
                         gc_clasp_length=gc_clasp_length)


class Hexagon(Snowflake):
    def __init__(self, overhang_length=2, gc_clasp_length=2):
        super().__init__(extra_edge=4,
                         overhang_length=overhang_length,
                         gc_clasp_length=gc_clasp_length)