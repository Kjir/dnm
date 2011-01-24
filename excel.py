import xlrd

def importfile( file ):
    wb = xlrd.open_workbook( file );
    s = wb.sheet_by_index(0)
    data = []
    for r in range(s.nrows):
        if r == 0:
            continue
        row = []
        for c in s.row(r):
            row.append(c.value)
        row = convert_to_db(row)
        data.append(tuple(row))

    return data

def convert_to_db(row):
    r = []
    r.append(row[7])
    r.append(row[0])
    r.append(row[1])
    (bdate, place) = row[2].split(",")
    r.append( convert_birth_date(bdate.strip()) )
    (bplace, bprov) = place.rsplit(" ", 1)
    r.append(bplace.strip())
    r.append(bprov.strip())
    (address, city) = row[3].split(",")
    r.append(address.strip())
    (city, prov) = city.split("(")
    r.append(city.strip())
    r.append(prov.strip().rstrip(")").strip())
    r.append(row[4])
    r.append(row[6])
    r.append(row[5])
    r.append(row[9])
    r.append(row[12])
    r.append(row[14])
    r.append( convert_cert_date(row[13] + " " + row[11]) )

    return r

def convert_cert_date(date):
    str_to_month = {
            "gennaio":  "01",
            "febbraio": "02",
            "marzo":    "03",
            "aprile":   "04",
            "maggio":   "05",
            "giugno":   "06",
            "luglio":   "07",
            "agosto":   "08",
            "settembre":"09",
            "ottobre":  "10",
            "novembre": "11",
            "dicembre": "12"
            }
    (year, month, day) = date.split(" ")
    if month not in str_to_month:
        month="01"
    else:
        month = str_to_month[month]
    return "-".join((year,month,day))

def convert_birth_date(date):
    (day, month, year) = date.split("-")
    return "-".join((year,month,day))
