import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import platform

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter File Explorer")
        self.root.geometry("900x600")

        self.current_path = os.path.abspath(os.getcwd())
        self.copy_source = None

        # Setup UI frames
        left_frame = ttk.Frame(root)
        left_frame.pack(side="left", fill="y")

        right_frame = ttk.Frame(root)
        right_frame.pack(side="right", fill="both", expand=True)

        # Treeview for folders/files
        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill="both", expand=True)

        # Buttons below tree
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x")

        self.btn_open = ttk.Button(btn_frame, text="Abrir arquivo", command=self.open_item)
        self.btn_open.pack(side="left", fill="x", expand=True)

        self.btn_up = ttk.Button(btn_frame, text="Pasta Anterior", command=self.go_up)
        self.btn_up.pack(side="left", fill="x", expand=True)

        self.btn_delete = ttk.Button(btn_frame, text="Deletar", command=self.delete_item)
        self.btn_delete.pack(side="left", fill="x", expand=True)

        self.btn_copy = ttk.Button(btn_frame, text="Copiar", command=self.copy_item)
        self.btn_copy.pack(side="left", fill="x", expand=True)

        self.btn_paste = ttk.Button(btn_frame, text="Colar", command=self.paste_item)
        self.btn_paste.pack(side="left", fill="x", expand=True)

        self.btn_rename = ttk.Button(btn_frame, text="Renomear", command=self.rename_item)
        self.btn_rename.pack(side="left", fill="x", expand=True)

        # Text area to show file contents
        self.text = tk.Text(right_frame, wrap="word")
        self.text.pack(fill="both", expand=True)

        # Bindings
        self.tree.bind("<<TreeviewOpen>>", self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh_tree()

    def refresh_tree(self):
        # Clear current tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert root node
        self.insert_node("", self.current_path, self.current_path)
        self.tree.item(self.tree.get_children()[0], open=True)

    def insert_node(self, parent, text, full_path):
        node = self.tree.insert(parent, "end", text=text, open=False, values=[full_path])
        if os.path.isdir(full_path):
            # Add a dummy child so the node shows expandable
            self.tree.insert(node, "end")

    def open_node(self, event):
        node = self.tree.focus()
        path = self.tree.item(node)["values"][0]
        if os.path.isdir(path):
            # Clear dummy children before loading real ones
            children = self.tree.get_children(node)
            for child in children:
                self.tree.delete(child)
            try:
                for name in sorted(os.listdir(path), key=lambda s: s.lower()):
                    full_path = os.path.join(path, name)
                    self.insert_node(node, name, full_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open folder:\n{e}")

    def on_select(self, event):
        node = self.tree.focus()
        if not node:
            return
        path = self.tree.item(node)["values"][0]
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, content)
            except Exception as e:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f"Error opening file:\n{e}")
        else:
            self.text.delete("1.0", tk.END)

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.current_path = parent
            self.refresh_tree()
        else:
            messagebox.showinfo("Info", "You are already at the root directory.")

    def open_item(self):
        path = self.get_selected_path()
        if not path:
            return

        if os.path.isfile(path):
            try:
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", path])
                else: 
                    subprocess.run(["xdg-open", path])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")
        else:
            messagebox.showinfo("Info", "Selected item is not a file.")

        

    def get_selected_path(self):
        node = self.tree.focus()
        if not node:
            messagebox.showwarning("Warning", "No item selected.")
            return None
        return self.tree.item(node)["values"][0]

    def delete_item(self):
        path = self.get_selected_path()
        if not path:
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n{path}?")
        if not confirm:
            return
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            messagebox.showinfo("Deleted", f"Deleted:\n{path}")
            self.refresh_tree()
            self.text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}")

    def copy_item(self):
        path = self.get_selected_path()
        if path:
            self.copy_source = path
            messagebox.showinfo("Copy", f"Copied:\n{path}")

    def paste_item(self):
        if not self.copy_source:
            messagebox.showwarning("Warning", "No copied item to paste.")
            return
        dest_folder = self.get_selected_path()
        if not dest_folder or not os.path.isdir(dest_folder):
            messagebox.showwarning("Warning", "Please select a destination folder.")
            return
        name = os.path.basename(self.copy_source)
        base, ext = os.path.splitext(name)
        dest_path = os.path.join(dest_folder, name)
        counter = 1
        while os.path.exists(dest_path):
            if os.path.isdir(self.copy_source):
                dest_path = os.path.join(dest_folder, f"{base}({counter})")
            else:
                dest_path = os.path.join(dest_folder, f"{base}({counter}){ext}")
            counter += 1

        try:
            if os.path.isdir(self.copy_source):
                shutil.copytree(self.copy_source, dest_path)
            else:
                shutil.copy2(self.copy_source, dest_path)
            messagebox.showinfo("Paste", f"Pasted to:\n{dest_path}")
            self.refresh_tree()
            self.copy_source = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste:\n{e}")

    def rename_item(self):
        path = self.get_selected_path()
        if not path:
            return
        new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=os.path.basename(path))
        if not new_name:
            return  # Cancelled or empty
        new_path = os.path.join(os.path.dirname(path), new_name)
        if os.path.exists(new_path):
            messagebox.showerror("Error", "A file or folder with this name already exists.")
            return
        try:
            os.rename(path, new_path)
            messagebox.showinfo("Renamed", f"Renamed to:\n{new_path}")
            self.refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename:\n{e}")

def start_gui():
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()

