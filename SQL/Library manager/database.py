import sqlite3


db1 = sqlite3.connect("test.db")
d = db1.cursor()

# --------ADD values to table--------------

# d.execute("INSERT INTO test (name,year,pages) VALUES ('Atom', 2011, 300),('Art', 2021, 340),('King', 2026, 145)")

# ----------Update all values by id-------------

# data = d.execute("SELECT rowid, * FROM test").fetchall()
# for item in data:
#     random_number = random.randint(0,9999)
#     row_id = item[0]
#     if item[1] != random_number:
#         d.execute("UPDATE test SET id = ? WHERE rowid = ?", (random_number, row_id))

# -----------------Delete values from table------------------

# Delete all values
# d.execute("DELETE FROM test")

# Delete value by some info
# d.execute("DELETE FROM test WHERE rowid == 2")
# for item in data:
#     rowid = item[0]
#     print(f"data rowid: {rowid}")

# new_data = d.execute("SELECT test.* , authors.name FROM test JOIN authors ON test.id = authors.user_id" ).fetchall()
# print(data)



def get_all_books():
   return d.execute("SELECT * FROM test").fetchall()

def get_book_by_year(year):
    if isinstance(year,int):
        data = d.execute("Select name FROM test WHERE year = ?",(year,)).fetchall()
    else: 
        raise ValueError
    
    if not data:
        print("Книг такого года не найдено")

    return data

def find_by_id(id):
    return d.execute("SELECT * FROM test WHERE id = ?",(id,)).fetchone()

def delete_book(id):
    data_for_delete = find_by_id(id)
    if data_for_delete:
        print(f"Книга с id {id} была удалена из списка!")
        d.execute("DELETE FROM test WHERE id = ?", (id,))
        db1.commit()
    else:
        print(f"Книги с таким id: {id} не существует")

def update_book(id,new_pages):
    data = find_by_id(id)
    if data:
        if new_pages > 0:
            d.execute("UPDATE test SET pages = ? WHERE id = ?",(new_pages,id,))
            db1.commit()
        else:
            print("Количество страниц должно быть больше 0")
    else:
        print(f"Книги с таким id: {id} не существует")
    

def search_books(title_part):
    search_param = f"%{title_part}%"
    data = d.execute("SELECT * FROM test WHERE name LIKE ?",(search_param,)).fetchall()
    if data:
        print(f"По даному запросу было найдено: {len(data)} книг")
        return data
    else:
        print("Книг по даному запросу не было найдено")

def get_library_stats():
    res = d.execute("SELECT COUNT(*), SUM(pages), MIN(year) FROM test").fetchone()
    if res and res[0] > 0:
        stats = {
            "total_books": res[0],
            "total_pages": res[1],
            "oldest_year": res[2]
        }
        return stats
    else:
        return None
    
def get_books_with_authors():
    authors = d.execute("SELECT * FROM authors").fetchone()
    test = d.execute("SELECT * FROM test").fetchone()

    if not any([authors,test]):
        print("Оба списка должны иметь какие-то данные")
        return 
    
    return d.execute("SELECT test.*,authors.name FROM test JOIN authors ON test.id = authors.user_id").fetchall()


# db1.commit()
# db1.close()