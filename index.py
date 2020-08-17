from tkinter import ttk
from tkinter import *
import sqlite3
import os
import sys

appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

class Product:

    db_name='database.db'


    def __init__(self, window):

        self.wind=window
        self.wind.title('Products Application')

        #creating a frame container to show all ttk features
        frame = LabelFrame(self.wind, text="Register A New Product")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #name input
        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name= Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #price input
        Label(frame, text="Price: ").grid(row=2, column=0)
        self.price=Entry(frame)
        self.price.grid(row=2, column=1)
        
        #button add product
        ttk.Button(frame, text="Save Product",  command=self.add_products).grid(row=3, columnspan=2, sticky=W+E)

        #output messages
        self.message=Label(text="", fg="red")
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)

        #create table
        self.tree=ttk.Treeview(height=10, column=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text="Name", anchor=CENTER)
        self.tree.heading("#1", text="Price", anchor=CENTER)
        #buttons
        ttk.Button(text="Delete", command=self.delete_product).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text="Edit", command=self.edit_product).grid(row=5, column=1, sticky=W+E)

        #fill all products
        self.get_products()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(os.path.join(appdir, self.db_name)) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records=self.tree.get_children()
        for record in records:
            self.tree.delete(record)
        query='Select * From product order by name desc'
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[1], value=row[2])

    def validation(self):
        return len(self.name.get())!=0 and len(self.price.get())!=0


    def add_products(self):
        if self.validation():
            query='insert into product values(null,?,?)'
            parameters=(self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text']="Product {} has been saved".format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)

        else:
            self.message['text']="Name and price are requiered"
        self.get_products()

    def edit_product(self):
        self.message['text']=" "
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']="Please select a record"
            return
        name=self.tree.item(self.tree.selection())['text']
        old_price=self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind=Toplevel()
        self.edit_wind.title="Edit Product"

        #old name
        Label(self.edit_wind,text="Old Name: ").grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly').grid(row=0,column=2)

        #new name
        Label(self.edit_wind, text="New Name: ").grid(row=1, column=1)
        new_name=Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #old price
        Label(self.edit_wind, text="Old Price: ").grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)
        #new price
        Label(self.edit_wind, text="New Price: ").grid(row=3, column=1)
        new_price=Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text="Update", command=lambda:self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)


    def edit_records(self, new_name, name, new_price, old_price):
        query='update product set name=?, price=? where name=? and price=?'
        parameters=(new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text']="Record {} has been updated".format(name)
        self.get_products()


    def delete_product(self):
        self.message['text']=" "
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']="Please select a record"
            return
        self.message['text']=" "    
        name=self.tree.item(self.tree.selection())['text']    
        query='delete from product where name=?'
        self.run_query(query, (name, ))
        self.message['text']="Record {} deleted".format(name)
        self.get_products()



if __name__=="__main__":
    window=Tk()
    application=Product(window)
    window.mainloop()


