import time
from math import sqrt
start_time = time.time()


def PrimeNumberCalculation(n):
    if(n > 2):
        prime = [*range(2, n)]
        x = 2
        while (x * x < n):
            if (x < sqrt(n)):
                for i in range(x * x, n, x):
                    prime.remove(i)
            x += 1
    
        number_of_elements = len(prime)
        print("Total number of prime numbers less than provided limit: ", number_of_elements)
    else:
        print("Please enter a limit that is greater than 2.")

limit = int(input("Enter an upper limit for the prime number search: "))
PrimeNumberCalculation(limit)

print("Program Run Time: %s seconds" % (time.time() - start_time))