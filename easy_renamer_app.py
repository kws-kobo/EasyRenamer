import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

class EasyRenamerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Easy Renamer")
        self.geometry("800x550")

        # --- ファイルリスト ---
        self.file_list_frame = ttk.LabelFrame(self, text="対象ファイル")
        self.file_list_frame.pack(padx=10, pady=10, fill="x")

        self.list_control_frame = ttk.Frame(self.file_list_frame)
        self.list_control_frame.pack(padx=5, pady=5)

        self.file_listbox = tk.Listbox(self.list_control_frame, width=110, height=10, selectmode=tk.EXTENDED) # 複数選択を許可
        self.file_listbox.pack(side="left")

        self.sort_button_frame = ttk.Frame(self.list_control_frame)
        self.sort_button_frame.pack(side="left", padx=5)

        self.up_button = ttk.Button(self.sort_button_frame, text="▲", command=lambda: self.move_item("up"), width=3)
        self.up_button.pack(pady=2)
        self.down_button = ttk.Button(self.sort_button_frame, text="▼", command=lambda: self.move_item("down"), width=3)
        self.down_button.pack(pady=2)
        self.sort_asc_button = ttk.Button(self.sort_button_frame, text="A-Z", command=lambda: self.sort_items(False), width=3)
        self.sort_asc_button.pack(pady=2)
        self.sort_desc_button = ttk.Button(self.sort_button_frame, text="Z-A", command=lambda: self.sort_items(True), width=3)
        self.sort_desc_button.pack(pady=2)
        self.remove_button = ttk.Button(self.sort_button_frame, text="削除", command=self.remove_items, width=3)
        self.remove_button.pack(pady=10)

        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)

        self.file_paths = []
        self.is_first_drop = True

        # --- 操作パネル ---
        self.control_panel_frame = ttk.LabelFrame(self, text="リネーム設定")
        self.control_panel_frame.pack(padx=10, pady=5, fill="x")
        self.rename_mode = tk.StringVar(value="replace")
        self.rename_mode.trace_add("write", self.update_panels)
        self.replace_radio = ttk.Radiobutton(self.control_panel_frame, text="置換", variable=self.rename_mode, value="replace")
        self.sequence_radio = ttk.Radiobutton(self.control_panel_frame, text="連番", variable=self.rename_mode, value="sequence")
        self.replace_radio.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sequence_radio.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.replace_frame = ttk.Frame(self.control_panel_frame)
        ttk.Label(self.replace_frame, text="元の文字列:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.old_str_entry = ttk.Entry(self.replace_frame, width=30)
        self.old_str_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(self.replace_frame, text="新しい文字列:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.new_str_entry = ttk.Entry(self.replace_frame, width=30)
        self.new_str_entry.grid(row=1, column=1, padx=5, pady=2)
        self.sequence_frame = ttk.Frame(self.control_panel_frame)
        ttk.Label(self.sequence_frame, text="接頭辞:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.prefix_entry = ttk.Entry(self.sequence_frame, width=20)
        self.prefix_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(self.sequence_frame, text="開始番号:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.start_num_entry = ttk.Entry(self.sequence_frame, width=10)
        self.start_num_entry.insert(0, "1")
        self.start_num_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(self.sequence_frame, text="桁数:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.digits_entry = ttk.Entry(self.sequence_frame, width=10)
        self.digits_entry.insert(0, "3")
        self.digits_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)
        self.execute_button = ttk.Button(self.button_frame, text="リネーム実行", command=self.execute_rename)
        self.clear_button = ttk.Button(self.button_frame, text="クリア", command=self.clear_list)
        self.execute_button.pack(side="left", padx=10)
        self.clear_button.pack(side="left", padx=10)
        self.update_panels()
        self.clear_list()

    def update_panels(self, *args):
        if self.rename_mode.get() == "replace":
            self.replace_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
            self.sequence_frame.grid_remove()
        else:
            self.sequence_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
            self.replace_frame.grid_remove()

    def on_drop(self, event):
        if self.is_first_drop:
            self.file_listbox.delete(0, tk.END)
            self.file_paths.clear()
            self.is_first_drop = False
        paths = self.tk.splitlist(event.data)
        for path in paths:
            if os.path.isdir(path):
                for sub_path in os.listdir(path):
                    full_path = os.path.join(path, sub_path)
                    if os.path.isfile(full_path):
                        self.file_listbox.insert(tk.END, full_path)
                        self.file_paths.append(full_path)
            else:
                self.file_listbox.insert(tk.END, path)
                self.file_paths.append(path)

    def clear_list(self):
        self.file_listbox.delete(0, tk.END)
        self.file_paths.clear()
        self.is_first_drop = True
        self.file_listbox.insert(0, "ここにファイルをドラッグ＆ドロップしてください")

    def move_item(self, direction):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices: return
        # For simplicity, move only the first selected item
        idx = selected_indices[0]

        if direction == "up" and idx > 0:
            new_idx = idx - 1
        elif direction == "down" and idx < len(self.file_paths) - 1:
            new_idx = idx + 1
        else:
            return

        self.file_paths[idx], self.file_paths[new_idx] = self.file_paths[new_idx], self.file_paths[idx]
        self.update_listbox()
        self.file_listbox.selection_set(new_idx)
        self.file_listbox.activate(new_idx)

    def sort_items(self, reverse):
        self.file_paths.sort(key=lambda x: x.lower(), reverse=reverse)
        self.update_listbox()

    def remove_items(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices: return
        
        # Remove from back to front to avoid index shifting issues
        for idx in sorted(selected_indices, reverse=True):
            self.file_listbox.delete(idx)
            self.file_paths.pop(idx)

    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for path in self.file_paths:
            self.file_listbox.insert(tk.END, path)

    def execute_rename(self):
        if not self.file_paths or self.is_first_drop:
            messagebox.showwarning("警告", "対象ファイルがありません。")
            return

        mode = self.rename_mode.get()
        renamed_count = 0
        error_count = 0

        try:
            paths_to_rename = list(self.file_paths)
            if mode == "replace":
                old_str = self.old_str_entry.get()
                new_str = self.new_str_entry.get()
                if not old_str:
                    messagebox.showwarning("警告", "元の文字列を入力してください。")
                    return
                
                for path in paths_to_rename:
                    dir_name = os.path.dirname(path)
                    file_name = os.path.basename(path)
                    if old_str in file_name:
                        new_file_name = file_name.replace(old_str, new_str)
                        new_path = os.path.join(dir_name, new_file_name)
                        os.rename(path, new_path)
                        renamed_count += 1

            elif mode == "sequence":
                prefix = self.prefix_entry.get()
                start_num = int(self.start_num_entry.get())
                digits = int(self.digits_entry.get())

                for i, path in enumerate(paths_to_rename):
                    dir_name = os.path.dirname(path)
                    _, ext = os.path.splitext(path)
                    new_num = str(start_num + i).zfill(digits)
                    new_file_name = f"{prefix}{new_num}{ext}"
                    new_path = os.path.join(dir_name, new_file_name)
                    os.rename(path, new_path)
                    renamed_count += 1

        except ValueError:
            messagebox.showerror("エラー", "開始番号や桁数には数値を入力してください。")
            error_count = len(paths_to_rename) - renamed_count
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました:\n{e}")
            error_count = len(paths_to_rename) - renamed_count
        
        messagebox.showinfo("完了", f"リネーム処理が完了しました。\n成功: {renamed_count}件, 失敗: {error_count}件")
        self.clear_list()

if __name__ == "__main__":
    app = EasyRenamerApp()
    app.mainloop()
