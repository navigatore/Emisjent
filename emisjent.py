from random import shuffle, randint
import csv
from operator import attrgetter

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
teacher_name = 'Will Murphy'
input_filename = 'availability_form.csv'


class Student:
    def __init__(self, name, dates):
        self.name = name
        self.dates = dates


class Schedule:
    def __init__(self, teacher, students):
        self.teacher = teacher
        self.students = students
        self.ttlen = len(self.teacher.dates)
        self.assignments = list(students.keys())
        self.assignments += ['nobody'] * self.ttlen
        shuffle(self.assignments)   # Initially randomize elements order
        self.quality = self.check_quality(self.assignments)  # lower is better
        self.vns()

    def check_quality(self, assignments):
        """
        Checks quality of assignments. Lower is better.
        """

        # Constraints
        max_lessons_per_week = 10
        min_lessons_per_day = 4
        max_lessons_per_day = 5
        hard_fail = 1000
        medium_fail = 100
        soft_fail = 1
        one_person_bonus = 10

        quality = 0

        assignments = [(i, student) for i, student in enumerate(assignments[:self.ttlen]) if student != 'nobody']     # Only the "front" part of assignments is evaluated
        assignments_per_day = {}
        for day in days:
            assignments_per_day[day] = [(i, student) for i, student in assignments if day in self.teacher.dates[i]]

        # More people -> better
        quality -= one_person_bonus * len(assignments)

        # 2. Gap fail check
        inner_dates_count = 0
        for assignment in assignments_per_day.values():
            if len(assignment) > 0:
                inner_dates_count += assignment[-1][0] - assignment[0][0] + 1 

        quality += medium_fail * (inner_dates_count - len(assignments))

        # 3. Too many lessons in week check
        if len(assignments) > max_lessons_per_week:
            quality += hard_fail * (len(assignments) - max_lessons_per_week)

        # 4. Too many / too little lessons per day check
        for day in days:
            length = len(assignments_per_day[day])
            if length == min_lessons_per_day - 1:
                quality += soft_fail
            elif length == max_lessons_per_day + 1:
                quality += soft_fail
            elif length != 0 and length < min_lessons_per_day - 1:
                quality += hard_fail * (min_lessons_per_day - length) 
            elif length > max_lessons_per_day + 1:
                quality += hard_fail * (length - max_lessons_per_day)

        # 5. Check if everybody can be present!
        quality += hard_fail * len([student for i, student in assignments if self.teacher.dates[i] not in self.students[student].dates])

        return quality

    def vns(self, max_steps=500, max_changes=3):
        for bound in range(1, max_changes+1):
            for i in range(max_steps):
                tmp = self.assignments[:]
                for k in range(randint(1, bound)):
                    first = randint(0, len(self.assignments) - 1)
                    second = randint(0, len(self.assignments) - 1)
                    tmp[first], tmp[second] = tmp[second], tmp[first]
                if self.check_quality(tmp) <= self.quality:
                    self.assignments = tmp
                    self.quality = self.check_quality(tmp)

    def print_assignments(self):
        print('Solution quality: ' + str(self.quality))
        for i in range(len(self.assignments)):
            if self.assignments[i] != 'nobody':
                print((self.teacher.dates[i] if i < self.ttlen else 'No date') + ' -> ' + self.assignments[i])

    def write_assignments(self, f):
        f.write('Quality of solution: ' + str(self.quality))
        for i in range(len(self.assignments)):
            if self.assignments[i] != 'nobody':
                print((self.teacher.dates[i] if i < self.ttlen else 'No date') + ' -> ' + self.assignments[i])


def main():
    with open(input_filename) as f:
        data = [row[1:] for row in csv.reader(f)]     # Time signature is unnecessary
    data.pop(0)     # Column names are not needed

    students = {}
    for row in data:
        name = row[0]
        dates = []

        for daynum, day in enumerate(row[1:]):
            hours = [days[daynum] + ' ' + hour for hour in day.split(';')]
            if hours != [days[daynum] + ' ']:  # If is equal, then no hour was selected in this day
                dates += hours

        students[name] = Student(name, dates)

    teacher = students[teacher_name]
    students.pop(teacher_name)

    sched = [Schedule(teacher, students) for _ in range(10)]
    sched.sort(key=attrgetter('quality'))
    sched[0].print_assignments()

if __name__ == '__main__':
    main()
