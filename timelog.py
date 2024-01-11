import os
from datetime import date

def log_task(decimal_value, task_description):
    today = date.today()
    file_name = f"{today.strftime('%Y-%m-%d')}.txt"

    if not os.path.isfile(file_name):
        with open(file_name, "w") as file:
            file.write(f"Date: {today}\n")

    # Count existing tasks to determine the next ID
    task_id = 0
    with open(file_name, "r") as file:
        for line in file:
            if "-" in line:
                task_id += 1

    with open(file_name, "a") as file:
        file.write(f"{decimal_value:.2f} - {task_description} ({task_id})\n")

def edit_task(task_id, new_decimal_value):
    today = date.today()
    file_name = f"{today.strftime('%Y-%m-%d')}.txt"

    if not os.path.isfile(file_name):
        print("No log file for today.")
        return

    with open(file_name, "r") as file:
        lines = file.readlines()

    edited = False
    with open(file_name, "w") as file:
        for line in lines:
            if f"({task_id})" in line:
                parts = line.split("-")
                if len(parts) == 2:
                    try:
                        new_line = f"{new_decimal_value:.2f} - {parts[1].strip()}\n"
                        file.write(new_line)
                        edited = True
                    except ValueError:
                        pass
            else:
                file.write(line)

    if edited:
        print(f"Task {task_id} edited successfully.")
    else:
        print(f"Task {task_id} not found in the log.")

def list_total_time():
    today = date.today()
    file_name = f"{today.strftime('%Y-%m-%d')}.txt"

    if not os.path.isfile(file_name):
        print("No log file for today.")
        return

    total_time = 0.0
    with open(file_name, "r") as file:
        for line in file:
            parts = line.split("-")
            if len(parts) == 2:
                time_str = parts[0].strip()
                try:
                    time_value = float(time_str)
                    total_time += time_value
                except ValueError:
                    pass

    print(f"Total time spent today: {total_time:.2f} hours")

def display_log():
    today = date.today()
    file_name = f"{today.strftime('%Y-%m-%d')}.txt"

    if not os.path.isfile(file_name):
        print("No log file for today.")
        return

    with open(file_name, "r") as file:
        content = file.read()
        print(content)

def main():
    while True:
        user_input = input("Enter a command (e.g., '2.5 - some comment', 'h', or 'l'): ").strip()

        if user_input.lower() == "h":
            list_total_time()
        elif user_input.lower() == "l":
            display_log()
        elif user_input.startswith("e "):
            parts = user_input.split()
            if len(parts) == 3:
                try:
                    task_id = int(parts[1])
                    new_decimal_value = float(parts[2])
                    edit_task(task_id, new_decimal_value)
                except ValueError:
                    print("Error: Invalid task ID or decimal value.")
            else:
                print("Invalid input format. Use 'e task_id new_decimal_value'.")
        elif "-" in user_input:
            parts = user_input.split("-")
            if len(parts) == 2:
                try:
                    decimal_value = float(parts[0].strip())
                    task_description = parts[1].strip()
                    log_task(decimal_value, task_description)
                except ValueError:
                    print("Error: The first part must be a decimal value.")
            else:
                print("Invalid input format. Use 'decimal_value - task_description'.")
        else:
            print("Invalid command. Use 'decimal_value - task_description', 'list', or 'l'.")

if __name__ == "__main__":
    main()
