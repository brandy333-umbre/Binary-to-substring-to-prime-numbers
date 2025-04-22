import time
import math

#  Test Cases
test_cases = [
    ("0100001101001111", 999999),
    ("01000011010011110100110101010000", 999999),
    ("1111111111111111111111111111111111111111", 999999),
    ("010000110100111101001101010100000011000100111000", 999999999),
    ("0100001101001111010011010101000000110001001110000110001", 123456789012),
    ("010000110100111101001101010100000011000100111000011000100111001", 123456789012345),
    ("01000011010011110100110101010000001100010011100001100010011100100100001", 123456789012345678),
    ("0100001101001111010011010101000000110001001110000110001001110010010000101000001", 1234567890123456789),
    ("010000110100111101001101010100000011000100111000011000100111001001000010100000101000100", 1234567890123456789),
    ("010000110100111101001101010100000011000100111000001100010011100100100001010000010100010001010011",
     12345678901234567890)
]

SIEVE_LIMIT = 10 ** 8  # Limit for the precomputed Sieve of Eratosthenes


def segmented_sieve(limit):
    """ Segmented Sieve of Eratosthenes for efficient prime generation up to a given limit. """
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False  # 0 and 1 are not prime
    for start in range(2, int(math.sqrt(limit)) + 1):
        if sieve[start]:
            for multiple in range(start * start, limit + 1, start):
                sieve[multiple] = False
    return {i for i, is_prime in enumerate(sieve) if is_prime}


# Generate primes up to the sieve limit
prime_set = segmented_sieve(SIEVE_LIMIT)


def is_prime(n):
    """ Check if a number is prime using precomputed primes or trial division for large numbers. """
    if n <= SIEVE_LIMIT:
        return n in prime_set
    if n < 2 or n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def generate_substrings(binary_str):
    """ Generate all possible decimal values from binary substrings with valid length constraints. """
    decimal_values = set()
    length = len(binary_str)

    for i in range(length):
        if binary_str[i] == '0':  # Skip leading zeros
            continue
        num = 0
        for j in range(i, min(i + 300, length)):  # Adjust length to avoid large non-prime numbers
            num = (num << 1) | int(binary_str[j])
            if num > 1:  # Ensure at least 2
                decimal_values.add(num)

    return decimal_values


def find_unique_primes(binary_str, N):
    """ Extract unique prime numbers from binary substrings using the segmented sieve approach. """
    if not all(c in '01' for c in binary_str):
        return "0: Invalid binary strings"

    decimal_numbers = generate_substrings(binary_str)
    prime_numbers = sorted({num for num in decimal_numbers if num < N and is_prime(num)})

    count = len(prime_numbers)
    if count == 0:
        return "0: No primes found"
    return f"{count}: {', '.join(map(str, prime_numbers[:3] + prime_numbers[-3:]))}"


# Run test cases and measure execution time
for i, (binary_string, N) in enumerate(test_cases, start=1):
    start_time = time.time()
    result = find_unique_primes(binary_string, N)
    print(f"Test Case {i}: {result} (Execution Time: {time.time() - start_time:.4f} seconds)")

# Profile Performance

