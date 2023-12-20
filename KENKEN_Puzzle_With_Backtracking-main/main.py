from kenken import Kenken
import time

def main():
    start_time = time.time()

    kenken_solver = Kenken("input.txt")
    kenken_solver.solve()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time:.6f} seconds")
    
main()
