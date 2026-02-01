import pandas as pd
import os
from datetime import datetime

FILE_NAME = "tasks.parquet"
VALID_STATUSES = ["new", "in progress", "done", "abandoned"]


def load_tasks():
    """Load tasks from file. Returns DataFrame or None."""
    if not os.path.exists(FILE_NAME):
        return None
    return pd.read_parquet(FILE_NAME)


def save_tasks(df):
    """Save tasks to parquet file."""
    df.to_parquet(FILE_NAME, index=False)


def add_task():
    # Task name (cannot be empty)
    while True:
        task_name = input("\nNew task: ").strip()
        if task_name:
            break
        print("Error: Task name cannot be empty!")

    # Priority (1 to 5)
    while True:
        try:
            task_priority = int(input("Priority (1-5): "))
            if 1 <= task_priority <= 5:
                break
            print("Error: Enter a number from 1 to 5!")
        except ValueError:
            print("Error: Enter a number from 1 to 5!")

    # Deadline (optional)
    deadline_date = None
    deadline_check = input("Add a deadline? (yes/no): ").strip().lower()

    if deadline_check == "yes":
        while True:
            try:
                deadline_input = input("Enter deadline (YYYY-MM-DD): ").strip()
                deadline_date = datetime.strptime(deadline_input, "%Y-%m-%d")

                # Check if deadline is in the past
                if deadline_date < datetime.now():
                    print("Warning: This date has already passed. Add anyway? (yes/no): ", end="")
                    if input().strip().lower() != "yes":
                        continue
                break
            except ValueError:
                print("Error: Invalid format! Use: YYYY-MM-DD (e.g., 2026-03-15)")

    #Create and save task
    new_task = pd.DataFrame({
        "task": [task_name],
        "priority": [task_priority],
        "deadline": [deadline_date],
        "status": ["new"]
    })

    df = load_tasks()
    if df is None:
        save_tasks(new_task)
    else:
        df = pd.concat([df, new_task], ignore_index=True)
        save_tasks(df)

    print(f"Task '{task_name}' added! (Priority: {task_priority})")


def show_tasks(priority=None, sort_by_deadline=False):
    df = load_tasks()

    if df is None or df.empty:
        print("\nTask list is empty!")
        return

    #Filter by priority
    if priority is not None:
        df = df[df['priority'] == priority]
        if df.empty:
            print(f"\nNo tasks with priority {priority}")
            return

    #Sort by deadline
    if sort_by_deadline:
        df = df.sort_values(by="deadline", ascending=True, na_position="last")

    #Display
    now = datetime.now()
    print("\n--- Task List ---")
    print("-" * 70)
    print(f"{'#':<4} {'Task':<25} {'Priority':<10} {'Deadline':<18} {'Status':<12}")
    print("-" * 70)

    for idx, row in df.iterrows():
        #Format deadline
        if pd.isna(row['deadline']):
            deadline_str = "None"
        else:
            deadline = pd.Timestamp(row['deadline'])
            days_left = (deadline - now).days
            deadline_str = deadline.strftime("%Y-%m-%d")

            if days_left < 0:
                deadline_str += " [OVERDUE]"
            elif days_left <= 3:
                deadline_str += " [SOON]"

        print(f"{idx:<4} {row['task']:<25} {row['priority']:<10} {deadline_str:<18} {row['status']:<12}")

    print("-" * 70)


def delete_task():
    df = load_tasks()

    if df is None or df.empty:
        print("\nTask list is empty!")
        return

    show_tasks()

    try:
        index_to_delete = int(input("\nEnter task number to delete: "))

        if index_to_delete not in df.index:
            print("Error: No task with that number!")
            return

        task_name = df.at[index_to_delete, 'task']
        confirm = input(f"Delete task '{task_name}'? (yes/no): ").strip().lower()

        if confirm == "yes":
            df = df.drop(index_to_delete)
            df = df.reset_index(drop=True)
            save_tasks(df)
            print(f"Task '{task_name}' deleted!")
        else:
            print("Cancelled.")

    except ValueError:
        print("Error: Enter a number!")


def change_status():
    df = load_tasks()

    if df is None or df.empty:
        print("\nTask list is empty!")
        return

    show_tasks()

    try:
        task_index = int(input("\nEnter task number: "))

        if task_index not in df.index:
            print("Error: No task with that number!")
            return

        task_name = df.at[task_index, 'task']
        current_status = df.at[task_index, 'status']

        print(f"\nTask: '{task_name}'")
        print(f"Current status: {current_status}")
        print(f"Available statuses: {', '.join(VALID_STATUSES)}")

        new_status = input("New status: ").strip().lower()

        if new_status not in VALID_STATUSES:
            print(f"Error: Invalid status! Choose from: {', '.join(VALID_STATUSES)}")
            return

        if new_status == current_status:
            print("Status is already set to that!")
            return

        df.at[task_index, 'status'] = new_status
        save_tasks(df)
        print(f"Status updated: {current_status} -> {new_status}")

    except ValueError:
        print("Error: Enter a number!")


def show_stats():
    """Display task statistics."""
    df = load_tasks()

    if df is None or df.empty:
        print("\nNo tasks available!")
        return

    total = len(df)
    print("\n--- Statistics ---")
    print("-" * 35)
    print(f"  Total tasks:         {total}")
    print("-" * 35)

    #By status
    print("  By status:")
    for status in VALID_STATUSES:
        count = len(df[df['status'] == status])
        if count > 0:
            print(f"    {status:<16} {count} ({count/total*100:.0f}%)")

    #By priority
    print("  By priority:")
    for p in range(5, 0, -1):
        count = len(df[df['priority'] == p])
        if count > 0:
            print(f"    Priority {p}:      {count}")

    #Overdue tasks
    now = datetime.now()
    overdue = df[df['deadline'].notna() & (df['deadline'] < now) & (df['status'] != 'done')]
    if not overdue.empty:
        print(f"\n  Overdue tasks: {len(overdue)}")
        for _, row in overdue.iterrows():
            print(f"    - {row['task']}")

    print("-" * 35)


def main():
    print("=" * 40)
    print("   My To-Do List")
    print("=" * 40)

    while True:
        print("\n--- Menu ---")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Change status")
        print("4. Delete task")
        print("5. Statistics")
        print("6. Exit")

        choice = input("\nSelect (1-6): ").strip()

        if choice == "1":
            print("\nShow:")
            print("  a. All tasks")
            print("  b. High priority only (5)")
            print("  c. Sort by deadline")
            sub = input("Your choice: ").strip().lower()

            if sub == "a":
                show_tasks()
            elif sub == "b":
                show_tasks(priority=5)
            elif sub == "c":
                show_tasks(sort_by_deadline=True)
            else:
                print("Invalid input")

        elif choice == "2":
            add_task()
        elif choice == "3":
            change_status()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            print("\nBye!")
            break
        else:
            print("Invalid input, try again.")


if __name__ == "__main__":
    main()