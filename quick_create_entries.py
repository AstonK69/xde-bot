from sqlite3 import connect

path = f"{__file__}".replace("\\", "/")
path = path.replace("quick_create_entries.py", "src/data/sauce_market.db")

con = connect(path)
cur = con.cursor()

# '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'
times = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

for i in times:
    cur.execute(f"insert into Sauces(Date, Time) values ('2023-12-22', '{i}:00:00')")

con.commit()
con.close()