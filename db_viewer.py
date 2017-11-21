from tkinter import *
from tkinter import ttk
from db import DBManager

class DBViewer:
    def __init__(self, master):
        # Main window
        self.master = master
        self.master.title('Simple DB viewer')
        self.master.minsize(width=640, height=480)

        menubar = Menu(self.master)

        menu = Menu(self.master, tearoff=0)
        menu.add_command(label='Создать базу данных')
        menu.add_command(label='Открыть базу данных')
        menu.add_separator()
        menu.add_command(label='Выход')
        menubar.add_cascade(label='Файл', menu=menu)

        menu = Menu(self.master, tearoff=0)
        menu.add_command(label='Записать изменения')
        menu.add_command(label='Удалить изменения')
        menubar.add_cascade(label='База данных', menu=menu)

        self.master.config(menu=menubar)


        tree_frame = ttk.Frame(self.master)
        btns_frame = ttk.Frame(self.master)

        # Connect to DB
        self.db = DBManager('db-name')

        # Combobox with select of table
        self.combo = ttk.Combobox(btns_frame)
        self.combo['values'] = ()
        for row in self.db.get_tables_names():
            self.combo['values'] += row
        self.combo.current(0)
        self.combo.bind('<<ComboboxSelected>>', self._combo_update)

        self.tree = ttk.Treeview(tree_frame, selectmode='extended')
        tree_x_scroll = ttk.Scrollbar(tree_frame, orient='hor', command=self.tree.xview)
        tree_y_scroll = ttk.Scrollbar(tree_frame, orient='vert', command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_y_scroll.set)
        self.tree.configure(xscrollcommand=tree_x_scroll.set)

        tree_y_scroll.pack(side='right', fill='y')
        self.tree.pack(side='top', fill='both', expand=True)
        tree_x_scroll.pack(side='bottom', fill='x')

        self._combo_update()

        # Buttons
        add = ttk.Button(btns_frame, text='Добавить запись')
        rm = ttk.Button(btns_frame, text='Удалить запись')
        run_sql = ttk.Button(btns_frame, text='Выполнить SQL')

        # Packs all elements
        tree_frame.pack(side='top', fill='both', expand=True)
        btns_frame.pack(side='bottom', fill='both')
        self.combo.pack(side='left', padx=5, pady=5)
        add.pack(side='left', padx=5, pady=5)
        rm.pack(side='left', padx=5, pady=5)
        run_sql.pack(side='left', padx=5, pady=5)

    def _combo_update(self, _event=0):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree['show'] = 'headings'
        columns = self.db.get_columns_names(self.combo.get())
        self.tree['columns'] = tuple(columns)
        for col in columns:
            self.tree.column(col, stretch=False, width=100)
            self.tree.heading(col, text=col)

        for row in self.db.get_rows(self.combo.get()):
            self.tree.insert('', 'end', values=row)

root = Tk()
db_viewer = DBViewer(root)
root.mainloop()
