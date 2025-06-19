from core.timetable import TimeTable
from core.genetic_algorithm import GeneticAlgorithm
from core.schedule_printer import print_schedule
def main():
    timetable = TimeTable()
    ga = GeneticAlgorithm(timetable)
    solution = ga.run()
    print_schedule(timetable, solution)
if __name__ == "__main__":
    main()
