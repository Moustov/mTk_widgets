from functools import partial
from tkinter import Tk, Button
from tkinter.constants import *
from tkinter.ttk import Treeview, Entry


# see https://www.youtube.com/watch?v=n5gItcGgIkk

class mtkEditTable(Treeview):
    def __init__(self, master, **kwargs):
        self.columns = kwargs["columns"]
        self.column_titles = None
        self.cells = None
        if "column_titles" in kwargs.keys():
            self.column_titles = kwargs["column_titles"]
            del kwargs["column_titles"]
        if "cells" in kwargs.keys():
            self.cells = kwargs["cells"]
            del kwargs["cells"]
        super().__init__(master, **kwargs)
        self.debug = False
        self.bind("<Double-1>", self._on_double_click)
        if self.column_titles:
            self.column("#0", width=0, stretch=NO)
            for (col_id, t) in zip(kwargs["columns"], self.column_titles):
                self.column(col_id, anchor=W, width=30)
                self.heading(col_id, text=t, anchor=CENTER)
        if self.cells:
            index = 0
            for row in self.cells:
                values = []
                for c in row:
                    values.append(row[c])
                self.insert(parent="", index='end', iid=index, text="", values=tuple(values))
                index += 1

    def get_data(self):
        res = []
        for i in self.get_children():
            data = self.item(i)['values']
            json = {}
            for c in self.columns:
                for r in data:
                    json[c] = r
            res.append(json)
        return res

    def _on_double_click(self, event):
        if self.debug:
            print("dc")
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked == "cell":
            col_index = self.identify_column(event.x)
            selected_row_iid = self.focus()
            selected_values = self.item(selected_row_iid)
            values = selected_values.get("values")
            col_number = int(col_index[1:]) - 1
            cell_value = values[col_number]
            cell_box = self.bbox(selected_row_iid, col_number)
            edit_entry = Entry(self.master, width=cell_box[2])
            # values recorded for _on_return_pressed
            edit_entry.editing_column_index = col_number
            edit_entry.editing_item_iid = selected_row_iid
            # only cells are editable / not the tree part
            if col_number > -1:
                edit_entry.place(x=cell_box[0], y=cell_box[1], w=cell_box[2], h=cell_box[3])
                edit_entry.insert(0, cell_value)
                edit_entry.select_range(0, END)
                edit_entry.focus()
                edit_entry.bind("<FocusOut>", self._on_focus_out)
                edit_entry.bind("<Return>", self._on_return_pressed)

    def _on_focus_out(self, event):
        event.widget.destroy()

    def _on_return_pressed(self, event):
        new_text = event.widget.get()
        col_index = event.widget.editing_column_index
        selected_row_iid = event.widget.editing_item_iid
        selected_values = self.item(selected_row_iid)
        if col_index > -1:
            values = selected_values.get("values")
            values[col_index] = new_text
            self.item(selected_row_iid, values=values)
        else:
            self.item(selected_row_iid, text=new_text)
        event.widget.destroy()


def do_extract(met):
    j = met.get_data()
    print(j)


if __name__ == "__main__":
    root = Tk()
    col_ids = ("A", "B", "C")
    col_titles = ("col A", "col B", "col C")
    data = [{"A": "ZER", "B": "TYU", "C": "IOP"},
            {"A": "QSD", "B": "FGH", "C": "JKL"}
            ]
    met = mtkEditTable(root, columns=col_ids, column_titles=col_titles, cells=data)
    met.pack(fill=BOTH, expand=True)
    extract = Button(root, text='Extract to file', command=partial(do_extract, met))
    extract.pack()
    root.mainloop()
