students = []
excellent_students = []

n = int(input("enter number of students: "))

for i in range(n):
    name = input(f"enter students name{i+1}: ")
    
    count = int(input(f"number of counts {name}: "))
    scores = []
    
    for j in range(count):
        score = float(input(f"count {j+1}: "))
        scores.append(score)
    
    average = sum(scores) / len(scores)

    if average >= 18:
        status = "excellent"
        excellent_students.append(name)
    elif average >= 15:
        status = "good"
    else:
        status = "need more effort"

    students.append({
        "name": name,
        "average": average,
        "status": status
    })

print("results:")
for student in students:
    print(f"name: {student['name']} | average: {student['average']:.2f} | status: {student['status']}")

print("excellent students:")
print(excellent_students)
