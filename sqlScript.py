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


createCar = """CREATE TABLE Cars (
    car_ID INT PRIMARY KEY,
    symboling INT,
    CarName VARCHAR(100),
    fueltype VARCHAR(10),
    aspiration VARCHAR(10),
    doornumber VARCHAR(10),
    carbody VARCHAR(20),
    drivewheel VARCHAR(10),
    enginelocation VARCHAR(10),
    wheelbase FLOAT,
    carlength FLOAT,
    carwidth FLOAT,
    carheight FLOAT,
    curbweight INT,
    enginetype VARCHAR(20),
    cylindernumber VARCHAR(10),
    enginesize INT,
    fuelsystem VARCHAR(20),
    boreratio FLOAT,
    stroke FLOAT,
    compressionratio FLOAT,
    horsepower INT,
    peakrpm INT,
    citympg INT,
    highwaympg INT,
    price DECIMAL(10,2)
);"""