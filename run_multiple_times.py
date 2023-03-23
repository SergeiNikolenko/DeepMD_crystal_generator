import subprocess
import os

def run_find_script(n_times):
    script_path = os.path.join(os.path.dirname(__file__), "find.py")
    start_mol_script_path = os.path.join(os.path.dirname(__file__), "start_mol.py")

    for i in range(n_times):
        try:
            print(f"Запуск {i + 1} из {n_times}")
            subprocess.run(["python", start_mol_script_path], check=True)
            result = subprocess.run(["python", script_path], check=True)
            if result.returncode != 0:
                print(f"Ошибка во время выполнения {i + 1} из {n_times}")
                break
            print(f"Завершение {i + 1} из {n_times}")

        except KeyboardInterrupt:
            print("Остановка выполнения. Программа прервана пользователем.")
            break

if __name__ == "__main__":
    n_times = 10  # Заданное количество раз для запуска find.py
    run_find_script(n_times)