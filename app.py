import os
import sys
import webbrowser
from pathlib import Path

import customtkinter
from utils import short_link

ORANGE = "#ff8c00"
ORANGE_LIGHT = "#ffa94d"
WINDOW_WIDTH = 560
WINDOW_HEIGHT = 400
LANG_FILE = "lang_pref.txt"
TOKEN_FILE = "token.txt"
ICON_FILE = "logo.ico"

LANG_OPTIONS = [("English", "en"), ("Русский", "ru")]
DISPLAY_TO_CODE = {disp: code for disp, code in LANG_OPTIONS}
CODE_TO_DISPLAY = {code: disp for disp, code in LANG_OPTIONS}

TRANSLATIONS = {
    "en": {
        "title": "BitlyClick",
        "prompt": "Paste a long URL to shorten it via Bitly:",
        "button_shorten": "Shorten link",
        "short_link_label": "Short link:",
        "enter_link": "Enter a link",
        "error_link": "Link is invalid. Please try again.",
        "error_token": "Your token is invalid. Please update it in token.txt",
        "theme_dark": "Theme: dark",
        "theme_light": "Theme: light",
        "splash": [
            "Loading Bitly API...",
            "Connecting token...",
            "Preparing interface...",
            "Done!",
        ],
        "lang": "Language",
    },
    "ru": {
        "title": "BitlyClick",
        "prompt": "Вставьте длинную ссылку, чтобы сократить её через Bitly:",
        "button_shorten": "Сократить ссылку",
        "short_link_label": "Сокращенная ссылка:",
        "enter_link": "Введите ссылку",
        "error_link": "Ссылка некорректна. Попробуйте ещё раз.",
        "error_token": "Ваш токен неверный. Пожалуйста, измените его в token.txt",
        "theme_dark": "Тема: тёмная",
        "theme_light": "Тема: светлая",
        "splash": [
            "Подключаемся к API Bitly...",
            "Проверяем токен...",
            "Готовим интерфейс...",
            "Почти готово...",
            "Готово!",
        ],
        "lang": "Язык",
    },
}


def resource_path(relative: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        exec_dir = Path(sys.executable).resolve().parent
        candidate = exec_dir / relative
        if candidate.exists():
            return candidate
        bundled = Path(sys._MEIPASS) / relative
        if bundled.exists():
            return bundled
        return candidate
    return Path(__file__).resolve().parent / relative


def load_lang() -> str:
    lang_path = resource_path(LANG_FILE)
    if lang_path.exists():
        try:
            value = lang_path.read_text(encoding="utf-8").strip()
            if value in TRANSLATIONS:
                return value
        except OSError:
            pass
    return "en"


def save_lang(lang: str) -> None:
    lang_path = resource_path(LANG_FILE)
    try:
        lang_path.write_text(lang, encoding="utf-8")
    except OSError:
        pass


token_cache: str | None = None


def load_token() -> str | None:
    global token_cache
    if token_cache is not None:
        return token_cache
    token_path = resource_path(TOKEN_FILE)
    if token_path.exists():
        try:
            value = token_path.read_text(encoding="utf-8").strip()
            if value:
                token_cache = value
                return value
        except OSError:
            return None
    return None


app = customtkinter.CTk()
app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
app.title("BitlyClick")
app.iconbitmap(resource_path(ICON_FILE))
customtkinter.set_appearance_mode("dark")
app.withdraw()
app.attributes("-alpha", 0)

current_theme = "dark"
current_lang = load_lang()


def t(key: str) -> str:
    return TRANSLATIONS[current_lang][key]


def center_app_window() -> None:
    app.update_idletasks()
    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()
    x = int((screen_w - WINDOW_WIDTH) / 2)
    y = int((screen_h - WINDOW_HEIGHT) / 2)
    app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


def handle_shorten() -> None:
    long_url = entry_long_url.get().strip()
    link_label.unbind("<Button-1>")

    token_value = load_token()
    if not token_value:
        label_result.configure(text=t("error_token"))
        link_label.configure(text="", cursor="")
        return

    if not long_url:
        label_result.configure(text=t("enter_link"))
        link_label.configure(text="", cursor="")
        return
    try:
        link = short_link(long_url, token=token_value)
    except Exception as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status in (401, 403):
            label_result.configure(text=t("error_token"))
        else:
            label_result.configure(text=t("error_link"))
        link_label.configure(text="", cursor="")
        return

    label_result.configure(text=t("short_link_label"))
    link_label.configure(
        text=link,
        text_color=ORANGE,
        font=("Arial", 16, "underline"),
        cursor="hand2",
    )
    link_label.bind("<Button-1>", lambda _e, url=link: webbrowser.open(url))


def fade_theme(next_mode: str) -> None:
    steps = 8
    start_alpha = 1.0
    mid_alpha = 0.9

    def fade_down(step: int = 0):
        if step <= steps:
            alpha = start_alpha - (start_alpha - mid_alpha) * (step / steps)
            app.attributes("-alpha", alpha)
            app.after(15, lambda: fade_down(step + 1))
        else:
            customtkinter.set_appearance_mode(next_mode)
            fade_up()

    def fade_up(step: int = 0):
        if step <= steps:
            alpha = mid_alpha + (start_alpha - mid_alpha) * (step / steps)
            app.attributes("-alpha", alpha)
            app.after(15, lambda: fade_up(step + 1))
        else:
            app.attributes("-alpha", start_alpha)

    fade_down()


def toggle_theme() -> None:
    global current_theme
    if current_theme == "dark":
        current_theme = "light"
        theme_button.configure(text="☀")
        label_theme.configure(text=t("theme_light"))
        fade_theme("light")
    else:
        current_theme = "dark"
        theme_button.configure(text="☾")
        label_theme.configure(text=t("theme_dark"))
        fade_theme("dark")


def fade_in_on_start(step: int = 0, steps: int = 15) -> None:
    alpha = step / steps
    app.attributes("-alpha", alpha)
    if step < steps:
        app.after(20, lambda: fade_in_on_start(step + 1, steps))


def show_splash() -> None:
    splash = customtkinter.CTkToplevel()
    splash.overrideredirect(True)
    splash.geometry("320x160")
    splash.attributes("-topmost", True)

    x = (splash.winfo_screenwidth() // 2) - 160
    y = (splash.winfo_screenheight() // 2) - 80
    splash.geometry(f"+{x}+{y}")

    splash_frame = customtkinter.CTkFrame(splash, corner_radius=12)
    splash_frame.pack(expand=True, fill="both", padx=12, pady=12)

    splash_label = customtkinter.CTkLabel(
        splash_frame,
        text="Starting...",
        font=("Arial", 16, "bold"),
    )
    splash_label.pack(pady=(12, 8))

    splash_progress = customtkinter.CTkProgressBar(
        splash_frame, width=240, progress_color=ORANGE
    )
    splash_progress.pack(pady=(4, 12))
    splash_progress.set(0.0)

    messages = TRANSLATIONS[current_lang]["splash"]

    def run_step(idx: int = 0):
        if idx < len(messages):
            splash_label.configure(text=messages[idx])
            splash_progress.set((idx + 1) / len(messages))
            splash.after(450, lambda: run_step(idx + 1))
        else:
            splash.destroy()
            center_app_window()
            app.deiconify()
            fade_in_on_start()

    run_step()


def set_lang_by_display(display: str) -> None:
    global current_lang
    code = DISPLAY_TO_CODE.get(display, "en")
    if code == current_lang:
        return
    current_lang = code
    save_lang(current_lang)
    app.title(t("title"))
    label_title.configure(text=t("title"))
    label_prompt.configure(text=t("prompt"))
    button_shorten.configure(text=t("button_shorten"))
    label_result.configure(text=t("short_link_label"))
    label_theme.configure(
        text=t("theme_dark") if current_theme == "dark" else t("theme_light")
    )
    lang_label.configure(text=t("lang"))
    lang_option.set(CODE_TO_DISPLAY[current_lang])


label_title = customtkinter.CTkLabel(
    app, text=t("title"), fg_color="transparent", font=("Arial", 32, "bold")
)
label_title.pack(pady=(16, 8))

label_prompt = customtkinter.CTkLabel(
    app,
    text=t("prompt"),
    fg_color="transparent",
    font=("Arial", 14),
)
label_prompt.pack(pady=(4, 6))

entry_long_url = customtkinter.CTkEntry(app, width=480, font=("Arial", 14))
entry_long_url.pack(padx=20, pady=(0, 10))

button_shorten = customtkinter.CTkButton(
    app,
    text=t("button_shorten"),
    fg_color=ORANGE,
    hover_color=ORANGE_LIGHT,
    text_color="black",
    font=("Arial", 14, "bold"),
    corner_radius=26,
    height=46,
    command=handle_shorten,
)
button_shorten.pack(pady=(8, 12))

label_result = customtkinter.CTkLabel(
    app,
    text=t("short_link_label"),
    fg_color="transparent",
    font=("Arial", 18),
)
label_result.pack(pady=(4, 4))

link_label = customtkinter.CTkLabel(
    app,
    text="",
    fg_color="transparent",
    font=("Arial", 16),
)
link_label.pack(pady=(0, 12))

theme_frame = customtkinter.CTkFrame(app, fg_color="transparent")
theme_frame.place(relx=0.02, rely=0.92, anchor="w")

label_theme = customtkinter.CTkLabel(
    theme_frame, text=t("theme_dark"), fg_color="transparent", font=("Arial", 12)
)
label_theme.pack(side="left", padx=(0, 10))

theme_button = customtkinter.CTkButton(
    theme_frame,
    width=34,
    height=34,
    text="☾",
    font=("Arial", 18, "bold"),
    fg_color=ORANGE,
    hover_color=ORANGE_LIGHT,
    text_color="black",
    corner_radius=17,
    command=toggle_theme,
)
theme_button.pack(side="left")

lang_frame = customtkinter.CTkFrame(app, fg_color="transparent")
lang_frame.place(relx=0.98, rely=0.92, anchor="e")

lang_label = customtkinter.CTkLabel(
    lang_frame, text=t("lang"), fg_color="transparent", font=("Arial", 12)
)
lang_label.pack(side="left", padx=(0, 10))

lang_option = customtkinter.CTkOptionMenu(
    lang_frame,
    width=120,
    values=[disp for disp, _ in LANG_OPTIONS],
    fg_color=ORANGE,
    button_color=ORANGE,
    button_hover_color=ORANGE_LIGHT,
    text_color="black",
    font=("Arial", 12, "bold"),
    dropdown_font=("Arial", 12),
    dropdown_fg_color="white",
    dropdown_text_color="black",
    command=set_lang_by_display,
)
lang_option.pack(side="left")
lang_option.set(CODE_TO_DISPLAY[current_lang])

center_app_window()
show_splash()
app.mainloop()
