def add_to_tables():
    conn = connect_db()
    c = conn.cursor()
    #c.execute("UPDATE rezerwacje SET DataStartuPobytu=? WHERE NrRezerwacji=?", ("25.01.2023", 4))
    c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (1234, 0, 20, "30.12.2023"))
    #c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (1111, 0, 20, "30.12.2023"))
    c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (2222, 0, 20, "30.12.2023"))
    c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (3333, 0, 20, "30.12.2023"))
    c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (4444, 0, 20, "30.12.2023"))
    conn.commit()
    conn.close()
    return 'Success'