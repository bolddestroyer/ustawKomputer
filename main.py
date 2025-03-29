import subprocess
import sys
import time
import tkinter
import pyautogui
import pygetwindow
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
        subprocess.run(
            [
                "cmd",
                "/c",
                "winget upgrade --id 9WZDNCRFJ3B4",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        if e.returncode != 2316632107:
            messagebox.showerror("Błąd", f"update_apps()\nBłąd: {e}")

    try:
        execution_status.set("Aktualizowanie aplikacji Zoom ...")
        time.sleep(1)
        window.update_idletasks()
        subprocess.run(
            [
                "cmd",
                "/c",
                "winget upgrade --id XP99J3KP4XZ4VV --accept-package-agreements",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        if e.returncode != 2316632107:
            messagebox.showerror(
                "Błąd",
                f"update_apps()\nBłąd: {e}\n\nKliknij OK, program będzie kontynował działanie.",
            )

    execution_status.set("Aktualizowanie aplikacji zakończone ...")


def set_jw_library(execution_status, window):
    try:
        execution_status.set("Uruchamianie aplikacji JW Library...")
        window.update_idletasks()
        pyautogui.press("win")
        time.sleep(1)
        pyautogui.write("JW Library")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(5)

        execution_status.set("Ustawianie okna aplikacji JW Library...")
        window.update_idletasks()

        for w in pygetwindow.getWindowsWithTitle("JW Library"):
            w.activate()
            w.maximize()
            pyautogui.keyDown("win")
            pyautogui.press("left")
            pyautogui.press("up")
            pyautogui.keyUp("win")
            pyautogui.press("escape")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Błąd", f"set_jw_library()\nBłąd: {e}")

    execution_status.set("Ustawianie aplikacji JW Library zakończone...")
    window.update_idletasks()


def set_file_explorer(execution_status, window):
    try:
        execution_status.set("Uruchamianie folderu z plikami wideo...")
        window.update_idletasks()
        subprocess.Popen('explorer "F:"')

        execution_status.set("Ustawianie okna z folderem z plikami wideo...")
        window.update_idletasks()
        time.sleep(1)

        for w in pygetwindow.getAllWindows():
            if "File Explorer" in w.title:
                w.activate()
                w.maximize()
                pyautogui.keyDown("win")
                pyautogui.press("left")
                pyautogui.press("down")
                pyautogui.keyUp("win")
                pyautogui.press("escape")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Błąd", f"set_file_explorer()\nBłąd: {e}")

    execution_status.set("Ustawianie okna z folderem z plikami wideo zakończone...")
    window.update_idletasks()


def execute_all(execution_status, window):
    # set_two_screens(execution_status, window)
    # time.sleep(2)
    # update_apps(execution_status, window)
    # time.sleep(2)
    # set_jw_library(execution_status, window)
    # time.sleep(2)
    set_file_explorer(execution_status, window)


def app_window():
    background_color = "#452C63"
    window = tkinter.Tk()
    window.title("Ustaw komputer")
    window.resizable(False, False)
    window.configure(bg=background_color)
    window.wm_attributes("-topmost", 1)

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
