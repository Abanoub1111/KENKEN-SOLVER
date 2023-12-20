from kenken import Kenken
import matplotlib.pyplot as plt
import time
import math
import sys


from kenken import Kenken
import time

def main():
    kenken_solver = Kenken("input2.txt")

    start_time = time.time()

    kenken_solver.solve()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.6f} seconds")

if __name__ == "__main__":
    main()
