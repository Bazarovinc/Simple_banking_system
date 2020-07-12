class Student:

    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        self.id = self.name[0] + self.last_name + str(self.birth_year)


name = input()
l_name = input()
b_year = int(input())
t_student = Student(name, l_name, b_year)
print(t_student.id)
