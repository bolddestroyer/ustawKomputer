import subprocess
import sys
import time
import tkinter
from tkinter import messagebox
import screeninfo
from settings import *


def set_two_screens(execution_status, window):
    execution_status.set("Rozszerzanie ekranu ...")
    window.update_idletasks()
    try:
        for i in range(5, 0, -1):
            execution_status.set(f"Rozszerzanie ekranu za {i} ...")
            time.sleep(1)
            window.update_idletasks()

        subprocess.run(["DisplaySwitch.exe", "/extend"], check=True)
        execution_status.set("Rozszerzanie ekranu zakończone ...")

        if len(screeninfo.get_monitors()) == 1:
            execution_status.set("Wystąpił błąd. Spróbuj jeszcze raz.")
            messagebox.showerror(
                "Błąd",
                "Błąd z drugim ekranem (telewizorem). Sprawdź czy kabel HDMI jest podłączony.",
            )
            return

    except Exception as e:
        execution_status.set("Wystąpił błąd. Spróbuj jeszcze raz.")
        messagebox.showerror(
            "Błąd", f"set_two_screens()\nBłąd: {e}\n\nProgram zakończy działanie."
        )
        return


def update_apps(execution_status, window):
    execution_status.set("Aktualizowanie aplikacji ...")
    time.sleep(1)
    window.update_idletasks()

    try:
        execution_status.set("Aktualizowanie aplikacji JW Library ...")
        time.sleep(1)
        window.update_idletasks()
        subprocess.run(["cmd", "/c", "winget upgrade --id 9WZDNCRFJ3B4"], check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode != 2316632107:
            messagebox.showerror("Błąd", f"update_apps()\nBłąd: {e}")

    try:
        execution_status.set("Aktualizowanie aplikacji Zoom ...")
        time.sleep(1)
        window.update_idletasks()
        subprocess.run(["cmd", "/c", "winget upgrade --id XP99J3KP4XZ4VV"], check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode != 2316632107:
            messagebox.showerror(
                "Błąd",
                f"update_apps()\nBłąd: {e}\n\nKliknij OK, program będzie kontynował działanie.",
            )

    execution_status.set("Aktualizowanie aplikacji zakończone ...")


def set_jw_library():
    try:
        subprocess.run(
            [
                "cmd",
                "/c",
                "start",
                f"C:\\Program Files\\WindowsApps\\WatchtowerBibleandTractSo.45909CDBADF3C_15.1.64.0_x64__5rz59y55nfz3e\\JWLibrary.exe",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Błąd", f"set_jw_library()\nBłąd: {e}")


def execute_all(execution_status, window):
    # set_two_screens(execution_status, window)
    # time.sleep(2)
    # update_apps(execution_status, window)
    # time.sleep(2)
    set_jw_library()


def app_window():
    background_color = "#452C63"

    window = tkinter.Tk()
    window.title("Ustaw komputer")
    window.resizable(False, False)
    window.configure(bg=background_color)

    center_window(window)
    set_window_size(window)

    for i in range(4):
        window.grid_rowconfigure(i, weight=1)

    for i in range(3):
        window.grid_columnconfigure(i, weight=1)

    execution_status = tkinter.StringVar()
    execution_status.set("Kliknij guzik żeby rozpocząć ustawianie")
    label_execution_status = tkinter.Label(
        window,
        textvariable=execution_status,
        bg=background_color,
        fg="#FFFFFF",
        font=("FreeSans", 10, "bold"),
    )
    label_execution_status.grid(row=2, column=1)

    btn_run_setup = tkinter.Button(
        window,
        text="Ustaw!",
        command=lambda: execute_all(execution_status, window),
        width=20,
        height=1,
        background="#3C3142",
        fg="#FFFFFF",
        font=("FreeSans", 12, "bold"),
    )
    btn_run_setup.grid(row=1, column=1)

    window.mainloop()


app_window()
