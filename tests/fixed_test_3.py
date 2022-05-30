from src.KMap import KarnaughMap


def run():
    exp = "A^¬Bv¬C"
    kmap = KarnaughMap(expression=exp)
    kmap.create_map()
    # kmap.print()
    # print(kmap.to_string())
    # print(str(kmap))
    solution = kmap.solve_map()
    # print(solution)
    return exp, solution, str(kmap)
