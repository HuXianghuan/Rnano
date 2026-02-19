from collections import Counter

from elements import *


class Nanoparticle:

    def __init__(self, id=None, structure=None):

        self.id = id
        self.structure = structure
        self.element_counts = Counter()
        self._element_list = {}
        self.sequence = None

        self.mfe = None
        self.ss = None
        self.frequency = None
        self.diversity = None

    def count_elements(self):
        self.element_counts = Counter(type(e) for e in self.structure)
        return self.element_counts

    def set_element_list(self, clazz, lst, required_length=None):
        if required_length is None:
            required_length = self.element_counts.get(clazz, 0)
        if len(lst) != required_length:
            raise ValueError(
                f"length of {clazz.__name__} list ({len(lst)}) does not match requirement ({required_length})"
            )
        self._element_list[clazz] = lst

    def get_element_list(self, clazz):
        return self._element_list.get(clazz, None)



    def get_dot_bracket(self):
        res = []
        open_pair_ids = set()

        for element in self.structure:

            if isinstance(element, StrictPairedElement):
                pid = element.pair_id

                if pid not in open_pair_ids:
                    res.append("("*element.length)
                    open_pair_ids.add(pid)
                else:
                    res.append(")"*element.length)
                    open_pair_ids.remove(pid)
            else:
                res.append("."*element.length)

        if open_pair_ids:
            raise ValueError(f"unclosed pairs: {open_pair_ids}")

        return "".join(res)


    def render_sequence(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement render_sequence()"
        )


    def check_element_sequence(self):
        for i in range(len(self.structure)):
            element = self.structure[i]
            try:
                if element.sequence is None:
                    raise ValueError(f"the {i} element {element} has sequence set to None")

            except AttributeError:
                raise AttributeError(f"the {i} element {element} has no attribute 'sequence'")
            except TypeError as e:
                raise TypeError(f"the {i} element {element} has invalid sequence: {e}")



    def rnafold_testify(self):

        if self.sequence is None:
            raise ValueError("sequence is empty")

        expected_ss, mfe, freq, div = seq_tools.get_rnafold_parameters(self.sequence)
        if expected_ss != self.get_dot_bracket():
            raise ValueError()
        else:
            self.ss = expected_ss
            self.mfe = mfe
            self.frequency = freq
            self.diversity = div



    def base_substitution(self, ratio=0.5, target=AntiSenseSirna):
        for element in self.structure:
            if isinstance(element, target):
                seq = element.sequence
                if seq is None:
                    raise ValueError(f"element {element} has not been rendered")
                else:
                    seq = seq_tools.mutate_sequence(seq=seq, from_base="A", to_base="G", prob=ratio)
                    element.sequence = seq
        res = "".join(element.sequence for element in self.structure)
        self.sequence = res
        return res



# ----------------------------------------------------------------------------------------------





