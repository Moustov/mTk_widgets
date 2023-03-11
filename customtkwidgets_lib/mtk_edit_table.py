from functools import partial
from tkinter import Tk, Button
from tkinter.constants import *
from tkinter.ttk import Treeview, Entry


# see https://www.youtube.com/watch?v=n5gItcGgIkk

class mtkEditTable(Treeview):
    """
    Editable table based on a TreeView => all Treeview features can be used

    * set self.debug to True for debugging
    * kwargs["columns"]: ex = ("A", "B", "C")
    * kwargs["column_titles"]: ex = ("col A", "col B", "col C")
    * kwargs["cells"]: ex = [{"A": "ZER", "B": "TYU", "C": "IOP"},
                            {"A": "QSD", "B": "FGH", "C": "JKL"}
                            ]
    """
    def __init__(self, master, **kwargs):
        self.debug = False
        self.columns = kwargs["columns"]
        self.column_titles = None
        self.cells = None
        # handling extra params
        if "column_titles" in kwargs.keys():
            self.column_titles = kwargs["column_titles"]
            del kwargs["column_titles"]
        if "cells" in kwargs.keys():
            self.cells = kwargs["cells"]
            del kwargs["cells"]
        #
        super().__init__(master, **kwargs)
        # events
        self.bind("<Double-1>", self._on_double_click)
        # set layout
        if self.column_titles:
            self.column("#0", width=0, stretch=NO)
            for (col_id, t) in zip(kwargs["columns"], self.column_titles):
                self.column(col_id, anchor=W, width=30)
                self.heading(col_id, text=t, anchor=CENTER)
        # set data
        if self.cells:
            index = 0
            for row in self.cells:
                values = []
                for c in row:
                    values.append(row[c])
                self.insert(parent="", index='end', iid=str(index), text="", values=tuple(values))
                index += 1

    def get_data(self) -> dict:
        """
        :return: a dict from the content
        """
        res = {}
        for i in self.get_children():
            data = self.item(i)['values']
            row = []
            res[i] = data
        return res

    def _on_double_click(self, event):
        """
        displays an entry field on top of the double-clicked cell
        :param event:
        :return:
        """
        region_clicked = self.identify_region(event.x, event.y)
        if self.debug:
            print("region_clicked", region_clicked, event)
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
        """
        when focus is lost, the entry box is discarded
        :param event:
        :return:
        """
        event.widget.destroy()

    def _on_return_pressed(self, event):
        """
        when RETURN the cell is replaced by the entry
        :param event:
        :return:
        """
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


def __do_test_extract(a_met: mtkEditTable):
    """
    only for test purpose on met.get_data()
    :param a_met: 
    :return: 
    """
    j = a_met.get_data()
    print(j)


if __name__ == "__main__":
    print("mtkEditTable demo")
    root = Tk()
    col_ids = ("A", "B", "C")
    col_titles = ("col A", "col B", "col C")
    data = [{"A": "ZER", "B": "TYU", "C": "IOP"},
            {"A": "QSD", "B": "FGH", "C": "JKL"}
            ]
    met = mtkEditTable(root, columns=col_ids, column_titles=col_titles, cells=data)
    met.debug = True
    met.pack(fill=BOTH, expand=True)
    extract = Button(root, text='Extract to file', command=partial(__do_test_extract, met))
    extract.pack()
    root.mainloop()
