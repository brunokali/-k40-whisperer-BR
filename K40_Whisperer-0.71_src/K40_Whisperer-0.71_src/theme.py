"""
theme.py — Configurações visuais do K40 Whisperer BR
Centraliza fontes, cores e estilos para fácil manutenção.
"""
import tkinter as tk
from tkinter import ttk
import platform
import ctypes

# ─── Detecção de modo do Windows ──────────────────────────────────────────────
def get_windows_theme():
    """Retorna 'dark' se o Windows estiver em modo escuro, senão 'light'."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return "light" if value == 1 else "dark"
    except Exception:
        return "light"

# ─── DPI Awareness (evita interface borrada em telas HiDPI) ───────────────────
def enable_dpi_awareness():
    """Ativa DPI awareness para Windows 10/11."""
    try:
        if platform.system() == "Windows":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# ─── Fontes ───────────────────────────────────────────────────────────────────
FONT_FAMILY  = "Segoe UI"   # Fonte moderna nativa do Windows 10/11
FONT_SIZE    = 9
FONT_NORMAL  = (FONT_FAMILY, FONT_SIZE)
FONT_BOLD    = (FONT_FAMILY, FONT_SIZE, "bold")
FONT_SMALL   = (FONT_FAMILY, 8)
FONT_TITLE   = (FONT_FAMILY, 10, "bold")

# ─── Cores de destaque (independem do tema claro/escuro) ─────────────────────
COLOR_ACCENT   = "#0078D4"   # Azul Windows 11
COLOR_SUCCESS  = "#107C10"   # Verde
COLOR_WARNING  = "#FFC83D"   # Amarelo
COLOR_ERROR    = "#C42B1C"   # Vermelho

# ─── Aplicar estilos ttk personalizados ──────────────────────────────────────
def apply_styles():
    """Configura estilos ttk adicionais sobre o tema sv-ttk."""
    style = ttk.Style()

    # Botões de ação principal (ex: Inicializar, Gravar)
    style.configure(
        "Accent.TButton",
        font=FONT_BOLD,
    )

    # Labels de seção/título
    style.configure(
        "Title.TLabel",
        font=FONT_TITLE,
    )

    # Labels normais com fonte moderna
    style.configure(
        "TLabel",
        font=FONT_NORMAL,
    )

    # Botões normais com fonte moderna
    style.configure(
        "TButton",
        font=FONT_NORMAL,
    )

    # Entries com fonte moderna
    style.configure(
        "TEntry",
        font=FONT_NORMAL,
    )

    # Checkbuttons
    style.configure(
        "TCheckbutton",
        font=FONT_NORMAL,
    )

    # Radiobuttons
    style.configure(
        "TRadiobutton",
        font=FONT_NORMAL,
    )

    # Combobox
    style.configure(
        "TCombobox",
        font=FONT_NORMAL,
    )

    # Botão Parar/Stop — vermelho coral
    style.configure(
        "Stop.TButton",
        font=FONT_BOLD,
        foreground="#8B0000",
    )
    style.map(
        "Stop.TButton",
        foreground=[("active", "#C42B1C")],
    )

    # Botão de aviso — laranja
    style.configure(
        "Warning.TButton",
        font=FONT_NORMAL,
    )


def set_button_style(btn, style_name):
    """Aplica um estilo ttk a um ttk.Button de forma segura."""
    try:
        btn.configure(style=style_name)
    except Exception:
        pass

def setup(root):
    """
    Ponto de entrada único: ativa DPI, aplica tema sv-ttk automático
    e configura estilos adicionais.

    Chame esta função logo após criar o root = Tk().
    """
    enable_dpi_awareness()

    try:
        import sv_ttk
        theme = get_windows_theme()
        sv_ttk.set_theme(theme)
    except ImportError:
        # Se sv-ttk não estiver disponível, usa tema nativo do sistema
        style = ttk.Style()
        try:
            style.theme_use("vista")    # Windows
        except Exception:
            pass

    apply_styles()

    # Fonte padrão global para widgets tk (não-ttk, ex: Menu, Canvas)
    root.option_add("*Font", FONT_NORMAL)
