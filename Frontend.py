import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# LOST & FOUND - FRONTEND
# Tkinter UI
# ============================================================

class LostFoundApp(tk.Tk):

    # ---------- Colors ----------
    BG = "#F5F7FA"
    WHITE = "#FFFFFF"
    TEXT = "#172033"
    MUTED = "#667085"
    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"
    BORDER = "#E4E7EC"
    GREEN = "#16A34A"

    def __init__(self):
        super().__init__()

        self.title("Lost & Found")
        self.geometry("1050x700")
        self.minsize(900, 620)
        self.configure(bg=self.BG)

        # Temporary local data.
        # Later this will be replaced with Supabase/backend calls.
        self.items = [
            {
                "type": "Lost",
                "name": "Black Wallet",
                "description": "Small black leather wallet",
                "location": "Library",
                "status": "Active"
            },
            {
                "type": "Found",
                "name": "Blue Water Bottle",
                "description": "Blue bottle with silver cap",
                "location": "Cafeteria",
                "status": "Active"
            }
        ]

        self.selected_type = tk.StringVar(value="Lost")
        self.search_text = tk.StringVar()

        self.item_name = tk.StringVar()
        self.location = tk.StringVar()

        self.setup_styles()
        self.create_ui()
        self.refresh_items()

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TEntry",
            padding=9,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview",
            background=self.WHITE,
            fieldbackground=self.WHITE,
            foreground=self.TEXT,
            rowheight=42,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#F8FAFC",
            foreground=self.MUTED,
            font=("Segoe UI", 9, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", self.TEXT)]
        )

    # ========================================================
    # MAIN UI
    # ========================================================

    def create_ui(self):

        # Main container
        main = tk.Frame(
            self,
            bg=self.BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            main,
            bg=self.BG
        )

        header.pack(
            fill="x",
            pady=(0, 25)
        )

        tk.Label(
            header,
            text="Lost & Found",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Report lost items and help others find theirs.",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 0))

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        content = tk.Frame(
            main,
            bg=self.BG
        )

        content.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # LEFT CARD - REPORT ITEM
        # ====================================================

        form_card = tk.Frame(
            content,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        form_card.pack(
            side="left",
            fill="y",
            padx=(0, 20)
        )

        form_card.configure(width=330)
        form_card.pack_propagate(False)

        tk.Label(
            form_card,
            text="Report an Item",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(22, 3)
        )

        tk.Label(
            form_card,
            text="Tell us about the item.",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 20)
        )

        # Item type
        self.label(form_card, "ITEM TYPE")

        type_frame = tk.Frame(
            form_card,
            bg=self.WHITE
        )

        type_frame.pack(
            fill="x",
            padx=22,
            pady=(7, 18)
        )

        self.lost_button = tk.Button(
            type_frame,
            text="Lost",
            command=lambda: self.select_type("Lost"),
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            pady=8
        )

        self.lost_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.found_button = tk.Button(
            type_frame,
            text="Found",
            command=lambda: self.select_type("Found"),
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            pady=8
        )

        self.found_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        self.select_type("Lost")

        # Item name
        self.label(form_card, "ITEM NAME")

        ttk.Entry(
            form_card,
            textvariable=self.item_name
        ).pack(
            fill="x",
            padx=22,
            pady=(6, 16)
        )

        # Location
        self.label(form_card, "LOCATION")

        ttk.Entry(
            form_card,
            textvariable=self.location
        ).pack(
            fill="x",
            padx=22,
            pady=(6, 16)
        )

        # Description
        self.label(form_card, "DESCRIPTION")

        self.description_box = tk.Text(
            form_card,
            height=6,
            wrap="word",
            bg=self.WHITE,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="solid",
            bd=1,
            font=("Segoe UI", 10),
            padx=10,
            pady=8
        )

        self.description_box.pack(
            fill="x",
            padx=22,
            pady=(6, 18)
        )

        # Submit button
        tk.Button(
            form_card,
            text="Submit Report",
            command=self.submit_item,
            bg=self.PRIMARY,
            fg="white",
            activebackground=self.PRIMARY_DARK,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            pady=11
        ).pack(
            fill="x",
            padx=22,
            pady=(0, 22)
        )

        # ====================================================
        # RIGHT CARD - ITEMS
        # ====================================================

        list_card = tk.Frame(
            content,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        list_card.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Top section
        top = tk.Frame(
            list_card,
            bg=self.WHITE
        )

        top.pack(
            fill="x",
            padx=22,
            pady=(22, 15)
        )

        tk.Label(
            top,
            text="Recent Items",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")

        # Search
        search = ttk.Entry(
            top,
            textvariable=self.search_text,
            width=25
        )

        search.pack(
            side="right"
        )

        search.bind(
            "<KeyRelease>",
            lambda event: self.refresh_items()
        )

        tk.Label(
            top,
            text="Search",
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            side="right",
            padx=(0, 8)
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table_frame = tk.Frame(
            list_card,
            bg=self.WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=22
        )

        columns = (
            "type",
            "name",
            "location",
            "status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.table.heading(
            "type",
            text="TYPE"
        )

        self.table.heading(
            "name",
            text="ITEM"
        )

        self.table.heading(
            "location",
            text="LOCATION"
        )

        self.table.heading(
            "status",
            text="STATUS"
        )

        self.table.column(
            "type",
            width=80,
            anchor="center"
        )

        self.table.column(
            "name",
            width=180
        )

        self.table.column(
            "location",
            width=150
        )

        self.table.column(
            "status",
            width=100,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------------------------
        # BOTTOM ACTION
        # ----------------------------------------------------

        bottom = tk.Frame(
            list_card,
            bg=self.WHITE
        )

        bottom.pack(
            fill="x",
            padx=22,
            pady=20
        )

        tk.Button(
            bottom,
            text="Mark Selected as Returned",
            command=self.mark_returned,
            bg="#F0FDF4",
            fg=self.GREEN,
            activebackground="#DCFCE7",
            activeforeground=self.GREEN,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=8
        ).pack(
            side="right"
        )

    # ========================================================
    # HELPER
    # ========================================================

    def label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            bg=self.WHITE,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=22
        )

    # ========================================================
    # LOST / FOUND
    # ========================================================

    def select_type(self, value):

        self.selected_type.set(value)

        if value == "Lost":

            self.lost_button.configure(
                bg=self.PRIMARY,
                fg="white"
            )

            self.found_button.configure(
                bg="#F2F4F7",
                fg=self.MUTED
            )

        else:

            self.found_button.configure(
                bg=self.PRIMARY,
                fg="white"
            )

            self.lost_button.configure(
                bg="#F2F4F7",
                fg=self.MUTED
            )

    # ========================================================
    # SUBMIT ITEM
    # ========================================================

    def submit_item(self):

        name = self.item_name.get().strip()
        location = self.location.get().strip()

        description = self.description_box.get(
            "1.0",
            "end"
        ).strip()

        if not name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the item name."
            )

            return

        if not location:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the location."
            )

            return

        new_item = {

            "type": self.selected_type.get(),

            "name": name,

            "description": description,

            "location": location,

            "status": "Active"
        }

        # ----------------------------------------------------
        # TEMPORARY
        # Later:
        # self.backend.create_item(new_item)
        # ----------------------------------------------------

        self.items.insert(
            0,
            new_item
        )

        # Clear form

        self.item_name.set("")
        self.location.set("")

        self.description_box.delete(
            "1.0",
            "end"
        )

        self.refresh_items()

        messagebox.showinfo(
            "Success",
            "Item submitted successfully!"
        )

    # ========================================================
    # DISPLAY ITEMS
    # ========================================================

    def refresh_items(self):

        for row in self.table.get_children():

            self.table.delete(row)

        query = self.search_text.get().lower().strip()

        for index, item in enumerate(self.items):

            searchable = (

                item["type"]
                + " "
                + item["name"]
                + " "
                + item["description"]
                + " "
                + item["location"]
                + " "
                + item["status"]

            ).lower()

            if query and query not in searchable:
                continue

            self.table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    item["type"],
                    item["name"],
                    item["location"],
                    item["status"]
                )
            )

    # ========================================================
    # MARK RETURNED
    # ========================================================

    def mark_returned(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an item first."
            )

            return

        index = int(selected[0])

        self.items[index]["status"] = "Returned"

        # Later:
        # backend.update_item_status(index, "Returned")

        self.refresh_items()

        messagebox.showinfo(
            "Updated",
            "Item marked as returned."
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app = LostFoundApp()

    app.mainloop()