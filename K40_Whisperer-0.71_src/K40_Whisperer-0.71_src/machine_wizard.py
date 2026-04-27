#!/usr/bin/env python
"""
machine_wizard.py — Assistente de Configuração de Máquina
K40 Studio BR — Focado em CO2 (M2 Nano)
"""
import tkinter as tk
from tkinter import ttk
import threading

try:
    import usb.core
    USB_AVAILABLE = True
except ImportError:
    USB_AVAILABLE = False

from i18n import _

# ─── Paleta de cores do wizard ────────────────────────────────────────────────
ACCENT  = "#0078D4"
SUCCESS = "#107C10"
ERROR   = "#C42B1C"
WARN    = "#FFC83D"

class MachineWizard(tk.Toplevel):
    """
    Wizard passo-a-passo simplificado para configuração da K40.
    """

    def __init__(self, parent, current_config=None):
        super().__init__(parent)
        self.parent = parent
        self.result = None

        cfg = current_config or {}
        self.machine_type   = tk.StringVar(value="co2")
        self.board_name     = tk.StringVar(value=cfg.get("board_name", "LASER-M2"))
        self.area_width     = tk.StringVar(value=str(cfg.get("laser_area_width", 300)))
        self.area_height    = tk.StringVar(value=str(cfg.get("laser_area_height", 200)))
        self.detection_status = tk.StringVar(value="")

        self._step = 0
        self._frames = []

        self._build_window()
        self._build_steps()
        self._show_step(0)

    def _build_window(self):
        self.title(_("Assistente de Configuração K40"))
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        W, H = 500, 400
        self.geometry("%dx%d+%d+%d" % (
            W, H,
            self.parent.winfo_rootx() + (self.parent.winfo_width()  - W) // 2,
            self.parent.winfo_rooty() + (self.parent.winfo_height() - H) // 2,
        ))

        hdr = ttk.Frame(self, padding=(0, 0))
        hdr.pack(fill="x")
        ttk.Label(hdr, text="⚙  " + _("Configuração da Máquina"), font=("Segoe UI", 12, "bold")).pack(padx=20, pady=(15, 2), anchor="w")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        self.step_bar = ttk.Frame(self, padding=(20, 8))
        self.step_bar.pack(fill="x")
        self._step_labels = []
        step_names = [_("Conexão"), _("Área"), _("Confirmar")]
        for i, name in enumerate(step_names):
            lbl = ttk.Label(self.step_bar, text="%d. %s" % (i + 1, name), font=("Segoe UI", 8))
            lbl.grid(row=0, column=i * 2, padx=10)
            self._step_labels.append(lbl)

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        self.content = ttk.Frame(self, padding=(24, 16))
        self.content.pack(fill="both", expand=True)

        ttk.Separator(self, orient="horizontal").pack(fill="x")
        footer = ttk.Frame(self, padding=(16, 10))
        footer.pack(fill="x")

        self.btn_cancel = ttk.Button(footer, text=_("Cancelar"), command=self.destroy)
        self.btn_cancel.pack(side="left")

        self.btn_back = ttk.Button(footer, text=_("← Anterior"), command=self._back, state="disabled")
        self.btn_back.pack(side="right", padx=(6, 0))

        self.btn_next = ttk.Button(footer, text=_("Próximo →"), command=self._next, style="Accent.TButton")
        self.btn_next.pack(side="right")

    def _build_steps(self):
        self._frames = [
            self._step_conexao(),
            self._step_area(),
            self._step_confirmar(),
        ]

    def _step_conexao(self):
        f = ttk.Frame(self.content)
        ttk.Label(f, text=_("Detecção da Placa Laser"), font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))

        self.btn_detect_usb = ttk.Button(f, text=_("🔍  Verificar Conexão USB"), command=self._detect_usb)
        self.btn_detect_usb.pack(anchor="w", pady=5)

        self.lbl_usb_status = ttk.Label(f, textvariable=self.detection_status, font=("Segoe UI", 9), wraplength=440)
        self.lbl_usb_status.pack(anchor="w", pady=(10, 10))

        ttk.Separator(f, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(f, text=_("Modelo da Placa:")).pack(anchor="w")
        board_cb = ttk.Combobox(f, textvariable=self.board_name,
                                values=["LASER-M2", "LASER-M3", "LASER-M1"],
                                state="readonly", width=15)
        board_cb.pack(anchor="w", pady=4)
        
        return f

    def _step_area(self):
        f = ttk.Frame(self.content)
        ttk.Label(f, text=_("Área de Trabalho (mm)"), font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))

        grid = ttk.Frame(f)
        grid.pack(anchor="w")
        ttk.Label(grid, text=_("Largura:")).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(grid, textvariable=self.area_width, width=10).grid(row=0, column=1, padx=10)
        ttk.Label(grid, text=_("Altura:")).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(grid, textvariable=self.area_height, width=10).grid(row=1, column=1, padx=10)

        ttk.Label(f, text=_("Padrão K40: 300x200 mm"), foreground="gray", font=("Segoe UI", 8)).pack(anchor="w", pady=10)
        return f

    def _step_confirmar(self):
        f = ttk.Frame(self.content)
        ttk.Label(f, text=_("Resumo"), font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))
        self.summary_text = tk.Text(f, height=8, width=50, state="disabled", font=("Segoe UI", 9), bg=self.cget("bg"), bd=0)
        self.summary_text.pack(fill="both", expand=True)
        return f

    def _show_step(self, step):
        for f in self._frames: f.pack_forget()
        self._update_step_bar(step)
        self._frames[step].pack(fill="both", expand=True)
        self.btn_back.configure(state="normal" if step > 0 else "disabled")
        if step == len(self._frames) - 1:
            self._fill_summary()
            self.btn_next.configure(text=_("Salvar"))
        else:
            self.btn_next.configure(text=_("Próximo →"))

    def _next(self):
        if self._step == len(self._frames) - 1: self._save_and_close()
        else: self._step += 1; self._show_step(self._step)

    def _back(self):
        if self._step > 0: self._step -= 1; self._show_step(self._step)

    def _update_step_bar(self, active):
        for i, lbl in enumerate(self._step_labels):
            color = ACCENT if i == active else (SUCCESS if i < active else "gray")
            lbl.configure(foreground=color)

    def _detect_usb(self):
        self.detection_status.set(_("🔍 Procurando..."))
        def run():
            if not USB_AVAILABLE:
                self.detection_status.set(_("❌ Erro: Biblioteca USB não encontrada."))
                return
            try:
                if usb.core.find(idVendor=0x1a86, idProduct=0x5512):
                    self.detection_status.set(_("✅ Placa M2 Nano Detectada!"))
                else:
                    self.detection_status.set(_("⚠  Placa não encontrada. Verifique o cabo e drivers."))
            except:
                self.detection_status.set(_("❌ Erro ao acessar USB."))
        threading.Thread(target=run, daemon=True).start()

    def _fill_summary(self):
        lines = [
            _("Máquina: CO2 (M2 Nano)"),
            _("Placa: ") + self.board_name.get(),
            _("Área: ") + self.area_width.get() + "x" + self.area_height.get() + " mm"
        ]
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("end", "\n".join(lines))
        self.summary_text.configure(state="disabled")

    def _save_and_close(self):
        self.result = {
            "machine_type"      : "co2",
            "board_name"        : self.board_name.get(),
            "laser_area_width"  : float(self.area_width.get() or 300),
            "laser_area_height" : float(self.area_height.get() or 200),
        }
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    wiz = MachineWizard(root)
    root.wait_window(wiz)
    root.destroy()
