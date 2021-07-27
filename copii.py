import tkinter
from database import Database


if __name__ == '__main__':
    db = Database()
    # db.get_all_tags('secrets')
    db.delete_data('token')
    # db.insert_data('token', 'i3i4bj3bj')
    db.get_all_tags('secrets')
