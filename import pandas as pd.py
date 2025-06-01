import pandas as pd
import time
from abc import ABC, abstractmethod
import matplotlib
matplotlib.use('Agg')  # ✅ Use non-GUI backend to prevent Tkinter issues
import matplotlib.pyplot as plt

# ------------------ Abstract Classes ------------------
class SortAlgorithm(ABC):
    @abstractmethod
    def sort(self, data):
        pass

# ------------------ Data Model ------------------
class WorkoutSession:
    def __init__(self, user, duration, calories, met_goal, logged_3days, logic_expr):
        self.user = user
        self.duration = int(duration)
        self.calories = float(calories)
        self.met_goal = bool(met_goal)
        self.logged_3days = bool(logged_3days)
        self.logic_expr = logic_expr

    def evaluate_logic(self):
        p = self.met_goal
        q = self.logged_3days
        try:
            return eval(self.logic_expr.replace('p', str(p)).replace('q', str(q)))
        except Exception as e:
            print(f"Logic error for {self.user}: {e}")
            return False

    def to_dict(self):
        return {
            "user": self.user,
            "duration": self.duration,
            "calories": self.calories,
            "met_goal": self.met_goal,
            "logged_3days": self.logged_3days,
            "logic_expr": self.logic_expr,
            "logic_value": self.evaluate_logic()
        }

    def __repr__(self):
        return f"{self.user} - {self.duration}min - {self.calories}cal - Logic: {self.evaluate_logic()}"

# ------------------ Sorting Algorithms ------------------
class InsertionSort(SortAlgorithm):
    def sort(self, sessions):
        for i in range(1, len(sessions)):
            key = sessions[i]
            j = i - 1
            while j >= 0 and (sessions[j].duration > key.duration or
                (sessions[j].duration == key.duration and not sessions[j].evaluate_logic())):
                sessions[j + 1] = sessions[j]
                j -= 1
            sessions[j + 1] = key
        return sessions

class MergeSort(SortAlgorithm):
    def sort(self, sessions):
        if len(sessions) <= 1:
            return sessions
        mid = len(sessions) // 2
        left = self.sort(sessions[:mid])
        right = self.sort(sessions[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        while left and right:
            if (left[0].duration < right[0].duration or
                (left[0].duration == right[0].duration and left[0].evaluate_logic())):
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        return result + left + right

# ------------------ Search Algorithm ------------------
def linear_search(sessions, min_calories):
    return [s for s in sessions if s.calories >= min_calories and s.evaluate_logic()]

# ------------------ Performance Analysis ------------------
def analyze_performance(sessions):
    insertion = InsertionSort()
    merge = MergeSort()

    t1 = time.time()
    insertion.sort(sessions.copy())
    t2 = time.time()

    t3 = time.time()
    merge.sort(sessions.copy())
    t4 = time.time()

    print(f"Insertion Sort Time: {t2 - t1:.6f}s")
    print(f"Merge Sort Time: {t4 - t3:.6f}s")

    plt.bar(['Insertion', 'Merge'], [t2 - t1, t4 - t3])
    plt.title("Sorting Performance")
    plt.ylabel("Time (s)")
    plt.savefig("performance_plot.png")  # ✅ Save plot as image
    print("Performance plot saved as 'performance_plot.png'.")

# ------------------ Data Handling ------------------
def load_sessions(filename):
    df = pd.read_csv(filename)
    sessions = []
    for _, row in df.iterrows():
        try:
            sessions.append(WorkoutSession(
                row['user'], row['duration'], row['calories'],
                row['met_goal'], row['logged_3days'], row['logic_expr']
            ))
        except Exception as e:
            print(f"Row loading error: {e}")
    return sessions

def save_sessions(filename, sessions):
    df = pd.DataFrame([s.to_dict() for s in sessions])
    df.to_csv(filename, index=False)


    def get_badge(self):
         if self.duration >= 60 and self.calories >= 500:

# ------------------ Manual Input ------------------
def manual_input():
    sessions = []
    print("\n--- Enter Workout Sessions (type 'done' to finish) ---")
    while True:
        user = input("Enter patient name (or 'done' to stop): ")
        if user.lower() == 'done':
            break
        try:
            duration = int(input("Duration (in minutes): "))
            calories = float(input("Calories burned: "))
            met_goal = input("Met goal? (True/False): ").strip().lower() == 'true'
            logged_3days = input("Logged 3+ days? (True/False): ").strip().lower() == 'true'
            logic_expr = input("Logic expression using p and q (e.g., p and q): ")
            sessions.append(WorkoutSession(user, duration, calories, met_goal, logged_3days, logic_expr))
        except ValueError:
            print("Invalid input. Please enter numbers for duration/calories and 'True'/'False' for boolean fields.")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return sessions

# ------------------ Main Interface ------------------
def main():
    print("\nExample CSV format you can use:")
    print("user,duration,calories,met_goal,logged_3days,logic_expr")
    print("Alice,45,400,True,True,p and q")
    print("Bob,30,250,True,False,p and q")
    print("Charlie,60,600,True,True,p or not q")
    print("Diana,25,200,False,True,not p and q")

    choice = input("\nWould you like to (1) Load from CSV or (2) Enter manually? ")
    sessions = []
    if choice == '1':
        filename = input("Enter the path to your CSV file (e.g., fitness_data.csv): ")
        sessions = load_sessions(filename)
    elif choice == '2':
        sessions = manual_input()
    else:
        print("Invalid option. Exiting.")
        return

    print("\nChoose Sorting Algorithm:")
    print("1. Insertion Sort (Loop-Based)")
    print("2. Merge Sort (Recursive)")
    sort_choice = input("Enter choice (1 or 2): ")

    sorter = InsertionSort() if sort_choice == '1' else MergeSort()
    sorted_sessions = sorter.sort(sessions.copy())

    print("\nSorted Sessions:")
    for s in sorted_sessions:
        print(s)

    analyze_performance(sessions)

    try:
        target = float(input("\nSearch: Enter minimum calories burned to filter: "))
        result = linear_search(sessions, target)
        print(f"\nSearch Results (calories >= {target} and logic = True):")
        for r in result:
            print(r)
    except ValueError:
        print("Invalid input for calories.")

    save_sessions("sorted_fitness_data.csv", sorted_sessions)
    print("\nSorted sessions saved to 'sorted_fitness_data.csv'.")

if __name__ == "__main__":
    main()



