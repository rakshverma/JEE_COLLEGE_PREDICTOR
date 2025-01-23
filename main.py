import pandas as pd
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_institute_csv():
    rounds = {}
    for i in range(1, 6):
        filename = f"2024_Round_{i}.csv"
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            df.columns = df.columns.str.strip()
            rounds[f"Round {i}"] = df

    output_dir = "institutes_csv"
    os.makedirs(output_dir, exist_ok=True)

    for round_name, df in rounds.items():
        round_dir = os.path.join(output_dir, round_name)
        os.makedirs(round_dir, exist_ok=True)

        unique_institutes = df['Institute'].unique()

        for institute in unique_institutes:
            institute_data = df[df['Institute'] == institute].drop(columns=['Institute'])
            institute_filename = os.path.join(round_dir, f"{institute.replace(' ', '_')}.csv")
            institute_data.to_csv(institute_filename, index=False)

    return rounds

def classify_institutes(df):
    def classify(row):
        institute_name = row['Institute'].lower().replace(" ", "")
        if "indianinstituteoftechnology" in institute_name:
            return "IIT"
        elif "indianinstituteofinformationtechnology" in institute_name:
            return "IIIT"
        elif "nationalinstituteoftechnology" in institute_name:
            return "NIT"
        else:
            return "GFTI"

    df['Institute Type'] = df.apply(classify, axis=1)
    return df

rounds = generate_institute_csv()

iits = pd.DataFrame()
iiits = pd.DataFrame()
nits = pd.DataFrame()
gftis = pd.DataFrame()

for round_name, df in rounds.items():
    classified_df = classify_institutes(df)
    rounds[round_name] = classified_df

    iits = pd.concat([iits, classified_df[classified_df['Institute Type'] == 'IIT']])
    iiits = pd.concat([iiits, classified_df[classified_df['Institute Type'] == 'IIIT']])
    nits = pd.concat([nits, classified_df[classified_df['Institute Type'] == 'NIT']])
    gftis = pd.concat([gftis, classified_df[classified_df['Institute Type'] == 'GFTI']])

for round_name, df in rounds.items():
    df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
    df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
    rounds[round_name] = df

def create_tooltip(widget):
    tooltip = None

    def show_tooltip(event):
        nonlocal tooltip
        if tooltip is not None:
            tooltip.destroy()
        item = widget.identify_row(event.y)
        column = widget.identify_column(event.x)
        if item and column:
            cell_value = widget.item(item)['values'][int(column[1:]) - 1]
            if cell_value:
                tooltip = tk.Toplevel(widget)
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
                label = tk.Label(tooltip, text=cell_value, background="lightyellow", borderwidth=1, relief="solid")
                label.pack()

    def hide_tooltip(event):
        nonlocal tooltip
        if tooltip is not None:
            tooltip.destroy()
            tooltip = None

    widget.bind("<Motion>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

def plot_comparisons(df):
    new_window = tk.Toplevel(root)
    new_window.title("Data Comparisons")
    new_window.geometry("1400x800")

    canvas = tk.Canvas(new_window, width=1300)
    scroll_y = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    institute_types = df['Institute Type'].unique()

    for institute_type in institute_types:
        institute_df = df[df['Institute Type'] == institute_type]

        label = tk.Label(scroll_frame, text=f"Institute Type: {institute_type}", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        fig, axes = plt.subplots(5, 1, figsize=(12, 20))
        genders = institute_df['Gender'].unique()
        opening_ranks_by_gender = [institute_df[institute_df['Gender'] == g]['Opening Rank'].mean() for g in genders]
        axes[0].bar(genders, opening_ranks_by_gender, color='skyblue')
        axes[0].set_title('Opening Rank by Gender', fontsize=10)
        axes[0].set_xlabel('Gender', fontsize=8)
        axes[0].set_ylabel('Opening Rank', fontsize=8)
        closing_ranks_by_gender = [institute_df[institute_df['Gender'] == g]['Closing Rank'].mean() for g in genders]
        axes[1].bar(genders, closing_ranks_by_gender, color='lightgreen')
        axes[1].set_title('Closing Rank by Gender', fontsize=10)
        axes[1].set_xlabel('Gender', fontsize=8)
        axes[1].set_ylabel('Closing Rank', fontsize=8)
        seat_types = institute_df['Seat Type'].unique()
        opening_ranks_by_seat_type = [institute_df[institute_df['Seat Type'] == s]['Opening Rank'].mean() for s in seat_types]
        axes[2].bar(seat_types, opening_ranks_by_seat_type, color='lightcoral')
        axes[2].set_title('Opening Rank by Seat Type', fontsize=10)
        axes[2].set_xlabel('Seat Type', fontsize=8)
        axes[2].set_ylabel('Opening Rank', fontsize=8)
        closing_ranks_by_seat_type = [institute_df[institute_df['Seat Type'] == s]['Closing Rank'].mean() for s in seat_types]
        axes[3].bar(seat_types, closing_ranks_by_seat_type, color='orange')
        axes[3].set_title('Closing Rank by Seat Type', fontsize=10)
        axes[3].set_xlabel('Seat Type', fontsize=8)
        axes[3].set_ylabel('Closing Rank', fontsize=8)
        if institute_type == "NIT":
            quotas = institute_df['Quota'].unique()
            opening_ranks_by_quota = [institute_df[institute_df['Quota'] == q]['Opening Rank'].mean() for q in quotas]
            closing_ranks_by_quota = [institute_df[institute_df['Quota'] == q]['Closing Rank'].mean() for q in quotas]

            axes[4].bar(quotas, opening_ranks_by_quota, label='Opening Rank', color='skyblue', alpha=0.6)
            axes[4].bar(quotas, closing_ranks_by_quota, label='Closing Rank', color='lightgreen', alpha=0.6)
            axes[4].set_title('Opening and Closing Rank by Quota for NITs', fontsize=10)
            axes[4].set_xlabel('Quota', fontsize=8)
            axes[4].set_ylabel('Rank', fontsize=8)
            axes[4].legend()
        else:
            fig.delaxes(axes[4])

        fig.tight_layout()

        canvas_plot = FigureCanvasTkAgg(fig, master=scroll_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack(pady=10)

def display_filtered_data(df):
    new_window = tk.Toplevel(root)
    new_window.title("Filtered Data")
    new_window.attributes('-fullscreen', True)

    tree = ttk.Treeview(new_window, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    columns = list(df.columns)
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.column("Institute", width=250)
    tree.column("Quota", width=100)
    tree.column("Seat Type", width=100)
    tree.column("Gender", width=160)
    tree.column("Institute Type", width=50)
    tree.column("Opening Rank", width=115)
    tree.column("Closing Rank", width=115)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    create_tooltip(tree)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 8))
    tree.configure(style="Treeview")

    sort_button = tk.Button(new_window, text="Sort Data", command=lambda: sort_data(tree, df))
    sort_button.pack(side=tk.BOTTOM, pady=5)

    plot_button = tk.Button(new_window, text="Show Comparisons", command=lambda: plot_comparisons(df))
    plot_button.pack(side=tk.BOTTOM, pady=5)

    close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack(side=tk.BOTTOM, pady=10)

    tree.pack(expand=True)

def sort_data(tree, df):
    sorted_df = df.sort_values(by='Opening Rank')
    for item in tree.get_children():
        tree.delete(item)
    for index, row in sorted_df.iterrows():
        tree.insert("", "end", values=list(row))

def display_data():
    selected_round = round_combobox.get()
    selected_institute_type = institute_type_combobox.get()
    selected_institute = institute_combobox.get()
    entered_rank = rank_entry.get()
    selected_quota = quota_combobox.get()
    selected_seat_type = seat_type_combobox.get()
    selected_gender = gender_combobox.get()

    if not selected_round:
        messagebox.showwarning("Input Error", "Please select a round.")
        return

    df = rounds[selected_round]
    if selected_institute_type:
        df = df[df['Institute Type'] == selected_institute_type]

    if selected_institute:
        df = df[df['Institute'] == selected_institute]

    if entered_rank.isdigit():
        entered_rank = int(entered_rank)
        df = df[df['Closing Rank'] > entered_rank]
    else:
        messagebox.showwarning("Input Error", "Please enter a valid rank number.")
        return

    if selected_quota:
        df = df[df['Quota'] == selected_quota]

    if selected_seat_type:
        df = df[df['Seat Type'] == selected_seat_type]

    if selected_gender:
        df = df[df['Gender'] == selected_gender]

    if df.empty:
        messagebox.showinfo("No Data", "No data found for the selected criteria.")
        return

    df = df.sort_values(by=['Institute'])

    display_filtered_data(df)

def update_institutes_by_type(event):
    selected_type = institute_type_combobox.get()
    selected_round = round_combobox.get()

    if selected_round:
        df = rounds[selected_round]

        if selected_type:
            filtered_institutes = df[df['Institute Type'] == selected_type]['Institute'].unique()
            institute_combobox['values'] = filtered_institutes.tolist()
        else:
            institute_combobox['values'] = df['Institute'].unique()

    institute_combobox.set('')

def populate_quota_seat_gender(selected_round):
    if selected_round:
        df = rounds[selected_round]

        unique_quotas = df['Quota'].unique().tolist()
        unique_seat_types = df['Seat Type'].unique().tolist()
        unique_genders = df['Gender'].unique().tolist()

        quota_combobox['values'] = unique_quotas
        quota_combobox.set('')

        seat_type_combobox['values'] = unique_seat_types
        seat_type_combobox.set('')

        gender_combobox['values'] = unique_genders
        gender_combobox.set('')

def update_filters(event):
    selected_round = round_combobox.get()

    if selected_round:
        df = rounds[selected_round]
        unique_types = df['Institute Type'].unique()
        institute_type_combobox['values'] = unique_types.tolist()

        institute_type_combobox.set('')
        institute_combobox.set('')

        populate_quota_seat_gender(selected_round)

root = tk.Tk()
root.title("Institute Data Viewer")
root.attributes('-fullscreen', True)

frame = Frame(root)
frame.pack(pady=10)

round_label = ttk.Label(frame, text="Select Round:")
round_label.grid(row=0, column=0, padx=10)
round_combobox = ttk.Combobox(frame, values=list(rounds.keys()), state="readonly")
round_combobox.grid(row=0, column=1, padx=10)
round_combobox.bind("<<ComboboxSelected>>", update_filters)

institute_type_label = ttk.Label(frame, text="Select Institute Type:")
institute_type_label.grid(row=1, column=0, padx=10)
institute_type_combobox = ttk.Combobox(frame, state="readonly")
institute_type_combobox.grid(row=1, column=1, padx=10)
institute_type_combobox.bind("<<ComboboxSelected>>", update_institutes_by_type)

institute_label = ttk.Label(frame, text="Select Institute:")
institute_label.grid(row=2, column=0, padx=10)
institute_combobox = ttk.Combobox(frame, state="readonly")
institute_combobox.grid(row=2, column=1, padx=10)

rank_label = ttk.Label(frame, text="Enter Rank:")
rank_label.grid(row=3, column=0, padx=10)
rank_entry = ttk.Entry(frame)
rank_entry.grid(row=3, column=1, padx=10)

quota_label = ttk.Label(frame, text="Select Quota:")
quota_label.grid(row=4, column=0, padx=10)
quota_combobox = ttk.Combobox(frame, state="readonly")
quota_combobox.grid(row=4, column=1, padx=10)

seat_type_label = ttk.Label(frame, text="Select Seat Type:")
seat_type_label.grid(row=5, column=0, padx=10)
seat_type_combobox = ttk.Combobox(frame, state="readonly")
seat_type_combobox.grid(row=5, column=1, padx=10)

gender_label = ttk.Label(frame, text="Select Gender:")
gender_label.grid(row=6, column=0, padx=10)
gender_combobox = ttk.Combobox(frame, state="readonly")
gender_combobox.grid(row=6, column=1, padx=10)

filter_button = ttk.Button(frame, text="Filter Data", command=display_data)
filter_button.grid(row=7, column=0, columnspan=2, pady=10)

close_button = ttk.Button(root, text="Close", command=root.destroy)
close_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
