import tkinter as tk

from calculator import FORMULA_LABEL, calculate, generate_values, summarize, transform_values


BACKGROUND = "#f4f5f7"
TEXT = "#20242c"
MUTED = "#6b7280"
BLUE = "#4568dc"
ORANGE = "#ec8b45"
GRID = "#e2e5e9"


class DataLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DataLab")
        self.root.geometry("900x650")
        self.root.minsize(720, 500)
        self.root.configure(bg=BACKGROUND)
        self.values = generate_values()

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=0)

        header = tk.Frame(self.root, bg=BACKGROUND)
        header.grid(row=0, column=0, sticky="ew", padx=26, pady=(22, 12))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="DataLab", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 21, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(header, text=f"Vzorec: {FORMULA_LABEL}", bg=BACKGROUND, fg=MUTED, font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", pady=(2, 0)
        )
        tk.Button(
            header,
            text="Generovať 50 hodnôt",
            command=self.generate_new,
            bg=TEXT,
            fg="white",
            activebackground=BLUE,
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=9,
            cursor="hand2",
        ).grid(row=0, column=1, rowspan=2, sticky="e")

        input_row = tk.Frame(self.root, bg=BACKGROUND)
        input_row.grid(row=1, column=0, sticky="ew", padx=26, pady=(10, 18))
        tk.Label(input_row, text="Číslo:", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 10)).pack(side="left")
        self.number_entry = tk.Entry(
            input_row,
            width=14,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=0,
        )
        self.number_entry.insert(0, "10")
        self.number_entry.pack(side="left", padx=(9, 8), ipady=5)
        self.number_entry.bind("<Return>", lambda _event: self.calculate_input())
        tk.Button(
            input_row,
            text="Vypočítať",
            command=self.calculate_input,
            bg=BLUE,
            fg="white",
            activebackground=TEXT,
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2",
        ).pack(side="left")
        self.result_label = tk.Label(input_row, text="Výsledok: —", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 11, "bold"))
        self.result_label.pack(side="left", padx=(16, 0))

        self.stats_label = tk.Label(
            self.root,
            text="",
            bg=BACKGROUND,
            fg=TEXT,
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.stats_label.grid(row=2, column=0, sticky="ew", padx=26, pady=(0, 10))

        chart_header = tk.Frame(self.root, bg=BACKGROUND)
        chart_header.grid(row=3, column=0, sticky="new", padx=26)
        chart_header.grid_columnconfigure(0, weight=1)
        tk.Label(chart_header, text="Graf", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w", pady=(3, 5)
        )
        legend = tk.Frame(chart_header, bg=BACKGROUND)
        legend.grid(row=0, column=1, sticky="e")
        tk.Label(legend, text="● Pôvodné", bg=BACKGROUND, fg=BLUE, font=("Segoe UI", 9)).pack(side="left", padx=7)
        tk.Label(legend, text="● Vypočítané", bg=BACKGROUND, fg=ORANGE, font=("Segoe UI", 9)).pack(side="left", padx=7)

        self.chart = tk.Canvas(self.root, bg="white", highlightthickness=1, highlightbackground=GRID)
        self.chart.grid(row=4, column=0, sticky="nsew", padx=26, pady=(0, 24))
        self.root.grid_rowconfigure(4, weight=1)
        self.chart.bind("<Configure>", lambda _event: self.draw_chart())

    def generate_new(self):
        self.values = generate_values()
        self.refresh()

    def calculate_input(self):
        try:
            value = float(self.number_entry.get().strip().replace(",", "."))
        except ValueError:
            self.result_label.configure(text="Zadaj číslo.", fg="#c0392b")
            return
        self.result_label.configure(text=f"Výsledok: {calculate(value):g}", fg=TEXT)

    def refresh(self):
        stats = summarize(self.values)
        self.stats_label.configure(
            text=f"50 hodnôt     Min: {stats['minimum']}     Max: {stats['maximum']}     Priemer: {stats['average']:.1f}"
        )
        self.draw_chart()

    def draw_chart(self):
        canvas = self.chart
        if not hasattr(self, "chart"):
            return
        canvas.delete("all")
        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width < 100 or height < 100:
            return

        calculated = transform_values(self.values)
        low = min(0, min(self.values + calculated))
        high = max(self.values + calculated) + 10
        if high == low:
            high += 1

        left, right, top, bottom = 42, 16, 18, 30
        plot_width = width - left - right
        plot_height = height - top - bottom

        for step in range(5):
            ratio = step / 4
            y = top + plot_height * ratio
            value = high - (high - low) * ratio
            canvas.create_line(left, y, width - right, y, fill=GRID)
            canvas.create_text(left - 8, y, text=f"{value:.0f}", anchor="e", fill=MUTED, font=("Segoe UI", 8))

        def point(index, value):
            x = left + plot_width * index / (len(self.values) - 1)
            y = top + plot_height * (high - value) / (high - low)
            return x, y

        for series, color in ((self.values, BLUE), (calculated, ORANGE)):
            points = [coordinate for index, value in enumerate(series) for coordinate in point(index, value)]
            canvas.create_line(*points, fill=color, width=2, smooth=True)


def main():
    root = tk.Tk()
    DataLabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
