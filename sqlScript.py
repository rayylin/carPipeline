createStock = """CREATE TABLE stock (
                    id NVARCHAR(20),
                    date DATETIME,
                    start NUMERIC(12,4),
                    [end] NUMERIC(12,4),
                    high NUMERIC(12,4),
                    low NUMERIC(12,4)
                    );"""

insertStock = """
    INSERT INTO stock (id, date, start, [end], high, low)
    VALUES (?, ?, ?, ?, ?, ?)
    """ 
#, ('AAPL', '2025-11-05', 198.53, 198.53, 198.53, 198.53)

selectStock = "SELECT * FROM stock"