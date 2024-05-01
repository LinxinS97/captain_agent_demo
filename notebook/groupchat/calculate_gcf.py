# filename: calculate_gcf.py
def calculate_gcf(a, b):
    while b:
        a, b = b, a % b
    return a

# Given numbers
num1 = 6432
num2 = 132

# Calculate GCF
gcf = calculate_gcf(num1, num2)
print(f"The Greatest Common Factor of {num1} and {num2} is: {gcf}")