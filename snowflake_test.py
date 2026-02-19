from nanoparticles_pack.snowflake import Snowflake
import random
a = Snowflake(extra_edge=4, gc_clasp_length=1, overhang_length=2)

print(a.element_counts)
sirna = ["UGAAACUCUCUUCUGGGCCACGC",
         "UCAUCAGAAGCCACCACAUGGGC",
         "GCUAGGAUUUGUUAGGUUUCCCG",
         "CGACCCGACCUGCUUAGCCUCGC",
         "CGACUUCCUCAAUGUGCCUCACG",
         "UGAAACUCUCUUCUGGGCCACUC",
         "GAUGAAACUCUCUUCUGGGCCAC",
         "UACGACCCGACCUGCUUAGCCGC",
         "AUGAAACUCUCUUCUGGGCCACC",
         "CUAGGAUUUGUUAGGUUUCCCGC",
         "UCACGACUUCCUCAAUGUGCCUC",
         "UGCGCGAGAUGUGAUGAGCACGC",
         "UGUCACGACUUCCUCAAUGUGCC"]

hp = ["UCCG", "GCAA", "UUCG"]
kl = [("AAAGCGGUA", "AAACCGCUA")]

a.siRNA_list = random.choices(sirna, k=18)
a.hairpin_list = random.choices(hp, k=6)
a.kisspair_list = random.choices(kl, k=1)


res = a.render_sequence()
print(res)


print(a.get_dot_bracket())
