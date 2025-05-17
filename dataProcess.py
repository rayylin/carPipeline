l = """1	3	alfa-romero giulia	gas	std	two	convertible	rwd	front	88.6	168.8	64.1	48.8	2548	dohc	four	130	mpfi	3.47	2.68	9	111	5000	21	27	13495
2	3	alfa-romero stelvio	gas	std	two	convertible	rwd	front	88.6	168.8	64.1	48.8	2548	dohc	four	130	mpfi	3.47	2.68	9	111	5000	21	27	16500
3	1	alfa-romero Quadrifoglio	gas	std	two	hatchback	rwd	front	94.5	171.2	65.5	52.4	2823	ohcv	six	152	mpfi	2.68	3.47	9	154	5000	19	26	16500
4	2	audi 100 ls	gas	std	four	sedan	fwd	front	99.8	176.6	66.2	54.3	2337	ohc	four	109	mpfi	3.19	3.4	10	102	5500	24	30	13950
5	2	audi 100ls	gas	std	four	sedan	4wd	front	99.4	176.6	66.4	54.3	2824	ohc	five	136	mpfi	3.19	3.4	8	115	5500	18	22	17450
"""


def transform_row_Car(row_string):
    fields = row_string.strip().split('\t')
    return (
        int(fields[0]),           # car_ID
        int(fields[1]),           # symboling
        fields[2],                # CarName
        fields[3],                # fueltype
        fields[4],                # aspiration
        fields[5],                # doornumber
        fields[6],                # carbody
        fields[7],                # drivewheel
        fields[8],                # enginelocation
        float(fields[9]),         # wheelbase
        float(fields[10]),        # carlength
        float(fields[11]),        # carwidth
        float(fields[12]),        # carheight
        int(fields[13]),          # curbweight
        fields[14],               # enginetype
        fields[15],               # cylindernumber
        int(fields[16]),          # enginesize
        fields[17],               # fuelsystem
        float(fields[18]),        # boreratio
        float(fields[19]),        # stroke
        float(fields[20]),        # compressionratio
        int(fields[21]),          # horsepower
        int(fields[22]),          # peakrpm
        int(fields[23]),          # citympg
        int(fields[24]),          # highwaympg
        float(fields[25])           # price
    )

# Split the string into lines and transform each line
rows = [transform_row_Car(line) for line in l.strip().split('\n')]

# Output the result
for row in rows:
    print(row)