from nanoparticles_pack.others import ThreeWayJunction
import random
from elements import *


a = ThreeWayJunction()

sirna = [
    "UCAUCAGAAGCCACCACAUGGGC",
    "UGAAACUCUCUUCUGGGCCACGC",
    "UGCGCGAGAUGUGAUGAGCACGC",
    "UGAAACUCUCUUCUGGGCCACUC",
    "CGACUUCCUCAAUGUGCCUCACG",
    "CUAGGAUUUGUUAGGUUUCCCGC",
    "GAUGAAACUCUCUUCUGGGCCAC",
    "AUGAAACUCUCUUCUGGGCCACC",
    "UACGACCCGACCUGCUUAGCCGC"]
random.shuffle(sirna)

a.siRNA_list = random.choices(sirna, k = a.element_counts[SenseSirna])

# hpl = ["UCCG", "GCAA", "UUCG"]  # hair pin loop
# kl = [("AAAGCGGUA", "AAACCGCUA"), ("AACAGGUGA", "AACACCUGA"), ("AAACGGCAA", "AAUGCCGUA"), ("AAGUGGACA", "AAGUCCACA"),
#       ("AAUCGCCAA", "AAUGGCGAA")]
n = ["UCCG", "GCAA", "UUCG"]
m  = [("AAAGCGGUA", "AAACCGCUA")]
a.hairpin_list = random.choices(n, k = a.element_counts[HairpinLoop])
a.kisspair_list = random.choices(m, k=a.element_counts[KissingLoop])



# a.render_sequence()
# print(a.structure[3].sequence)

# print([element.sequence for element in a.structure])

print(a.render_sequence())
print(a.get_dot_bracket())

print(a.rnafold_testify())