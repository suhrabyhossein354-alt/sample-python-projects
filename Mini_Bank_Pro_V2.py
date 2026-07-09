
import tkinter as tk
from tkinter import ttk, messagebox
import json, os

DB = "users.json"

def load_db():
    if not os.path.exists(DB):
        data = {
            "users": {
                "admin": {"password": "1234", "balance": 0}
            },
            "loan_requests": []
        }
        with open(DB, "w") as f:
            json.dump(data, f, indent=4)
    with open(DB, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

current_user = None

root = tk.Tk()
root.title("Mini Bank Pro V2")
root.geometry("1100x700")

def login():
    global current_user
    db = load_db()
    u = ent_user.get().strip()
    p = ent_pass.get().strip()

    if u in db["users"] and db["users"][u]["password"] == p:
        current_user = u
        show_panel()
    else:
        messagebox.showerror("Login", "Invalid credentials")

def register():
    db = load_db()
    u = ent_user.get().strip()
    p = ent_pass.get().strip()

    if not u or not p:
        return

    if u in db["users"]:
        messagebox.showerror("Register", "User exists")
        return

    db["users"][u] = {"password": p, "balance": 0}
    save_db(db)
    messagebox.showinfo("Register", "Account created")

def show_panel():
    for w in root.winfo_children():
        w.destroy()

    db = load_db()

    top = ttk.Frame(root)
    top.pack(fill="x")

    balance_lbl = ttk.Label(
        top,
        text=f"User: {current_user} | Balance: {db['users'][current_user]['balance']}$"
    )
    balance_lbl.pack(pady=10)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Banking
    bank = ttk.Frame(notebook)
    notebook.add(bank, text="Banking")

    amount = ttk.Entry(bank)
    amount.pack(pady=5)

    receiver = ttk.Entry(bank)
    receiver.pack(pady=5)

    def deposit():
        db = load_db()
        db["users"][current_user]["balance"] += float(amount.get())
        save_db(db)
        show_panel()

    def transfer():
        db = load_db()
        r = receiver.get().strip()
        a = float(amount.get())
        if r in db["users"] and db["users"][current_user]["balance"] >= a:
            db["users"][current_user]["balance"] -= a
            db["users"][r]["balance"] += a
            save_db(db)
            show_panel()

    ttk.Button(bank, text="Deposit", command=deposit).pack()
    ttk.Button(bank, text="Transfer", command=transfer).pack()

    # Loans
    loan = ttk.Frame(notebook)
    notebook.add(loan, text="Loans")

    ttk.Label(loan, text="Loan Amount").pack()
    loan_amount = ttk.Entry(loan)
    loan_amount.pack()

    ttk.Label(loan, text="Months").pack()
    months = ttk.Entry(loan)
    months.pack()

    def request_loan():
        db = load_db()
        db["loan_requests"].append({
            "user": current_user,
            "amount": float(loan_amount.get()),
            "months": int(months.get()),
            "status": "pending"
        })
        save_db(db)
        messagebox.showinfo("Loan", "Request sent")

    ttk.Button(loan, text="Request Loan", command=request_loan).pack(pady=10)

    # Admin
    if current_user == "admin":
        admin = ttk.Frame(notebook)
        notebook.add(admin, text="Admin")

        tree = ttk.Treeview(admin, columns=("user","amount","months","status"), show="headings")
        for c in ("user","amount","months","status"):
            tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)

        db = load_db()
        for req in db["loan_requests"]:
            tree.insert("", "end", values=(req["user"], req["amount"], req["months"], req["status"]))

        def approve():
            sel = tree.selection()
            if not sel:
                return
            vals = tree.item(sel[0])["values"]
            db = load_db()

            for req in db["loan_requests"]:
                if req["user"] == vals[0] and req["status"] == "pending":
                    req["status"] = "approved"

                    total = req["amount"] * 1.12
                    monthly = round(total / req["months"], 2)

                    db["users"][req["user"]]["balance"] += req["amount"]
                    db["users"][req["user"]]["loan"] = {
                        "remaining": round(total,2),
                        "monthly": monthly,
                        "months_left": req["months"]
                    }
                    break

            save_db(db)
            show_panel()

        ttk.Button(admin, text="Approve Loan", command=approve).pack(pady=5)

    ttk.Button(root, text="Logout", command=restart).pack(pady=10)

def restart():
    for w in root.winfo_children():
        w.destroy()
    build_login()

def build_login():
    frame = ttk.Frame(root)
    frame.pack(expand=True)

    ttk.Label(frame, text="Mini Bank Pro V2").pack(pady=10)

    global ent_user, ent_pass
    ent_user = ttk.Entry(frame)
    ent_user.pack()

    ent_pass = ttk.Entry(frame, show="*")
    ent_pass.pack()

    ttk.Button(frame, text="Login", command=login).pack(pady=5)
    ttk.Button(frame, text="Register", command=register).pack(pady=5)

build_login()
root.mainloop()
