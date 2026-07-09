n = int(input("Enter number of subjects: "))

total = 0

for i in range(n):
    mark = float(input(f"Enter marks for subject {i+1}: "))
    total += mark

average = total / n

print("Average Marks =", average)
