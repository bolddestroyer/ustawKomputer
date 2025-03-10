def center_window(window):
    try:
        window.update_idletasks()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_center_x = (window.winfo_screenwidth() // 2) - (window_width // 2)
        screen_center_y = (window.winfo_screenheight() // 2) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{screen_center_x}+{screen_center_y}")
    except Exception as e:
        print(f"Error center_window: {e}")


def set_window_size(window):
    try:
        window.update_idletasks()
        window.geometry(f"384x216")
    except Exception as e:
        print(f"Error set_window_size: {e}")