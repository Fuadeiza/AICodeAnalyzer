import random

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def generate_random_numbers(n):
    return [random.randint(1, 100) for i in range(n)]

def print_results(numbers, average):
    print("Numbers:", numbers)
    print("Average:", average)

if __name__ == "__main__":
    num_count = 10
    random_numbers = generate_random_numbers(num_count)
    avg = calculate_average(random_numbers)
    print_results(random_numbers, avg)

    # Attempt to calculate average of an empty list
    empty_list = []
    empty_avg = calculate_average(empty_list)
    print_results(empty_list, empty_avg)