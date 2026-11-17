import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from calculator import FORMULAS, generate_values, summarize, transform_values


BACKGROUND = "#0b1020"
PANEL = "#121a2d"
PANEL_LIGHT = "#18233a"
TEXT = "#edf2ff"
MUTED = "#8995b2"
ACCENT = "#7c5cff"
CYAN = "#44d7c8"
GRID = "#26314a"


class DataLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DataLab — Score Studio")
        self.root.geometry("1180x790")
        self.root.minsize(980, 680)
        self.root.configure(bg=BACKGROUND)

        self.values = generate_values(50)
        self.formula_name = tk.StringVar(value=next(iter(FORMULAS)))
        self.stat_labels = {}

        self._style_ttk()
        self._build_ui()
        self.refresh()

    def _style_ttk(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "DataLab.TCombobox",
            fieldbackground=PANEL_LIGHT,
            background=PANEL_LIGHT,
            foreground=TEXT,
            arrowcolor=TEXT,
            bordercolor=GRID,
            lightcolor=GRID,
            darkcolor=GRID,
            padding=10,
        )
        style.map(
            "DataLab.TCombobox",
            fieldbackground=[("readonly", PANEL_LIGHT)],
            foreground=[("readonly", TEXT)],
            selectbackground=[("readonly", PANEL_LIGHT)],
            selectforeground=[("readonly", TEXT)],
        )

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        header = tk.Frame(self.root, bg=BACKGROUND)
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(24, 16))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="DATA LAB  /  SCORE STUDIO",
            bg=BACKGROUND,
            fg=CYAN,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="Premeníme dáta na príbeh.",
            bg=BACKGROUND,
            fg=TEXT,
            font=("Segoe UI Semibold", 23),
        ).grid(row=1, column=0, sticky="w", pady=(5, 2))
        tk.Label(
            header,
            text="Generátor skóre · štatistika · živé porovnanie vzorca",
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).grid(row=2, column=0, sticky="w")
        self._button(header, "↻  NOVÝ SET", self.generate_new, ACCENT).grid(
            row=1, column=1, rowspan=2, padx=(12, 0), sticky="e"
        )
        self._button(header, "↓  EXPORT CSV", self.export_csv, PANEL_LIGHT).grid(
            row=1, column=2, rowspan=2, padx=(10, 0), sticky="e"
        )

        stats = tk.Frame(self.root, bg=BACKGROUND)
        stats.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 16))
        for column in range(4):
            stats.grid_columnconfigure(column, weight=1, uniform="stat")
        for column, (key, title) in enumerate(
            (("minimum", "MINIMUM"), ("maximum", "MAXIMUM"), ("average", "PRIEMER"), ("median", "MEDIÁN"))
        ):
            card = tk.Frame(stats, bg=PANEL, padx=16, pady=12)
            card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 10, 0))
            tk.Label(card, text=title, bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
            value_label = tk.Label(card, text="—", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 20))
            value_label.pack(anchor="w", pady=(3, 0))
            self.stat_labels[key] = value_label

        content = tk.Frame(self.root, bg=BACKGROUND)
        content.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 18))
        content.grid_columnconfigure(0, minsize=270)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        controls = tk.Frame(content, bg=PANEL, padx=18, pady=18)
        controls.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        controls.grid_columnconfigure(0, weight=1)
        tk.Label(controls, text="01  /  TRANSFORMÁCIA", bg=PANEL, fg=CYAN, font=("Segoe UI", 8, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(controls, text="Vyber vzorec", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 14)).grid(
            row=1, column=0, sticky="w", pady=(7, 10)
        )
        formula_picker = ttk.Combobox(
            controls,
            textvariable=self.formula_name,
            values=list(FORMULAS),
            state="readonly",
            style="DataLab.TCombobox",
        )
        formula_picker.grid(row=2, column=0, sticky="ew")
        formula_picker.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        tk.Label(
            controls,
            text="Vzorec sa použije na každú z 50 hodnôt. Graf zobrazí pôvodné aj vypočítané skóre.",
            bg=PANEL,
            fg=MUTED,
            justify="left",
            wraplength=235,
            font=("Segoe UI", 9),
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))

        tk.Frame(controls, bg=GRID, height=1).grid(row=4, column=0, sticky="ew", pady=18)
        tk.Label(controls, text="02  /  OPERÁCIE S POĽOM", bg=PANEL, fg=CYAN, font=("Segoe UI", 8, "bold")).grid(
            row=5, column=0, sticky="w"
        )
        tk.Label(
            controls,
            text="Minimum, maximum, priemer a medián počítame zo vstupného poľa. Vzorky nižšie sú zoradené vzostupne.",
            bg=PANEL,
            fg=TEXT,
            justify="left",
            wraplength=235,
            font=("Segoe UI", 9),
        ).grid(row=6, column=0, sticky="w", pady=(8, 12))
        tk.Label(controls, text="50 ZORADENÝCH HODNÔT", bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).grid(
            row=7, column=0, sticky="w"
        )
        self.sorted_values_label = tk.Label(
            controls,
            text="",
            bg=PANEL_LIGHT,
            fg=TEXT,
            justify="left",
            anchor="nw",
            padx=10,
            pady=9,
            wraplength=235,
            font=("Consolas", 8),
        )
        self.sorted_values_label.grid(row=8, column=0, sticky="ew", pady=(7, 0))

        chart_panel = tk.Frame(content, bg=PANEL, padx=16, pady=15)
        chart_panel.grid(row=0, column=1, sticky="nsew")
        chart_panel.grid_rowconfigure(1, weight=1)
        chart_panel.grid_columnconfigure(0, weight=1)
        chart_header = tk.Frame(chart_panel, bg=PANEL)
        chart_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        chart_header.grid_columnconfigure(0, weight=1)
        tk.Label(chart_header, text="POROVNANIE SKÓRE", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 12)).grid(
            row=0, column=0, sticky="w"
        )
        self.formula_caption = tk.Label(chart_header, text="", bg=PANEL, fg=MUTED, font=("Segoe UI", 9))
        self.formula_caption.grid(row=1, column=0, sticky="w", pady=(3, 0))
        legend = tk.Frame(chart_header, bg=PANEL)
        legend.grid(row=0, column=1, rowspan=2, sticky="e")
        self._legend_item(legend, ACCENT, "Pôvodné")
        self._legend_item(legend, CYAN, "Výsledok")

        self.chart = tk.Canvas(chart_panel, bg=PANEL, highlightthickness=0)
        self.chart.grid(row=1, column=0, sticky="nsew")
        self.chart.bind("<Configure>", lambda _event: self.draw_chart())

        footer = tk.Frame(self.root, bg=BACKGROUND)
        footer.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 14))
        tk.Label(
            footer,
            text="DATA LAB  •  50 VZORIEK  •  NÁHODNÉ SKÓRE 10–100",
            bg=BACKGROUND,
            fg=MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left")
        self.dataset_label = tk.Label(footer, text="", bg=BACKGROUND, fg=MUTED, font=("Segoe UI", 8))
        self.dataset_label.pack(side="right")

    @staticmethod
    def _button(parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=TEXT,
            activebackground=ACCENT,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            padx=15,
            pady=11,
            cursor="hand2",
            font=("Segoe UI", 8, "bold"),
        )

    @staticmethod
    def _legend_item(parent, color, label):
        item = tk.Frame(parent, bg=PANEL)
        item.pack(side="left", padx=(10, 0))
        marker = tk.Canvas(item, width=12, height=12, bg=PANEL, highlightthickness=0)
        marker.pack(side="left", padx=(0, 5))
        marker.create_oval(2, 2, 10, 10, fill=color, outline=color)
        tk.Label(item, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(side="left")

    def generate_new(self):
        self.values = generate_values(50)
        self.refresh()

    def refresh(self):
        summary = summarize(self.values)
        for key in ("minimum", "maximum", "average", "median"):
            self.stat_labels[key].configure(text=f"{summary[key]:.1f}")
        self.sorted_values_label.configure(text="  ".join(str(value) for value in summary["ordered"]))
        self.formula_caption.configure(text=f"Použitý vzorec: {self.formula_name.get()}")
        self.dataset_label.configure(text=f"{len(self.values)} hodnôt  ·  rozsah {summary['minimum']}–{summary['maximum']}")
        self.draw_chart()

    def draw_chart(self):
        if not hasattr(self, "chart"):
            return
        canvas = self.chart
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 100 or height < 100:
            return

        calculated = transform_values(self.values, self.formula_name.get())
        all_values = self.values + calculated
        y_min = min(0, min(all_values) - 5)
        y_max = max(all_values) + 10
        if y_max <= y_min:
            y_max = y_min + 1
        left, right, top, bottom = 48, 16, 24, 42
        plot_width = width - left - right
        plot_height = height - top - bottom

        for step in range(5):
            ratio = step / 4
            y = top + plot_height * ratio
            value = y_max - (y_max - y_min) * ratio
            canvas.create_line(left, y, width - right, y, fill=GRID)
            canvas.create_text(left - 9, y, text=f"{value:.0f}", anchor="e", fill=MUTED, font=("Segoe UI", 8))

        for index in (0, 9, 19, 29, 39, 49):
            x = left + plot_width * index / (len(self.values) - 1)
            canvas.create_text(x, height - bottom + 19, text=str(index + 1), fill=MUTED, font=("Segoe UI", 8))

        def point(index, value):
            x = left + plot_width * index / (len(self.values) - 1)
            y = top + plot_height * (y_max - value) / (y_max - y_min)
            return x, y

        for series, color in ((self.values, ACCENT), (calculated, CYAN)):
            points = [coordinate for index, value in enumerate(series) for coordinate in point(index, value)]
            canvas.create_line(*points, fill=color, width=2, smooth=True, splinesteps=12)
            for index, value in enumerate(series):
                x, y = point(index, value)
                canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=color, outline=color)

        canvas.create_text(left + plot_width / 2, height - 8, text="ČÍSLO VZORKY", fill=MUTED, font=("Segoe UI", 8, "bold"))

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Exportovať výsledky",
            defaultextension=".csv",
            filetypes=(("CSV súbor", "*.csv"),),
            initialfile="datalab_vysledky.csv",
        )
        if not path:
            return
        calculated = transform_values(self.values, self.formula_name.get())
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(("Vzorka", "Pôvodná hodnota", "Vypočítaná hodnota", "Vzorec"))
                for index, (original, result) in enumerate(zip(self.values, calculated), start=1):
                    writer.writerow((index, original, f"{result:.2f}", self.formula_name.get()))
        except OSError as error:
            messagebox.showerror("Export zlyhal", f"Súbor sa nepodarilo uložiť:\n{error}")
            return
        messagebox.showinfo("Export dokončený", f"Výsledky boli uložené do súboru:\n{path}")


def main():
    root = tk.Tk()
    DataLabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
