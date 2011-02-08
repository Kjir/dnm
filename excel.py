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
    '''Convert Excel data format to a format suitable to the database'''
    r = []
    r.append(None) # ID, automatically generated
    if row[7].strip() == "no": # Member number
        r.append(None)
    else:
        r.append(row[7])
    r.append(row[1]) # First name
    r.append(row[0]) # Last name
    bdate = ""
    place = ""
    if row[2].find(",") == -1:
        bdate = row[2]
    else:
        (bdate, place) = row[2].split(",", 1)
    r.append( convert_birth_date(bdate.strip()) ) # Birth date
    place = place.split("(") # Place of birth
    if len(place) == 1:
        r.append(place[0].strip()) # City of birth
        r.append(None) # Province of birth
    else:
        r.append(place[0].strip()) # City of birth
        r.append( place[1].strip().rstrip(")").strip() ) # Province of birth
    address = ""
    city = ""
    if row[3].find(",") == -1:
        city = row[3]
    else:
        (address, city) = row[3].rsplit(",", 1)
    r.append(address.strip()) # Address
    place = city.split("(")
    if len(place) == 1:
        r.append(place[0].strip()) # City
        r.append(None) # Province
    else:
        r.append(place[0].strip()) # City
        r.append( place[1].strip().rstrip(")").strip() ) # Province
    r.append(row[4] + " - " + row[6]) # Activity
    m = row[5].split(" ")
    if len(m) < 2:
        r.append(None)
        r.append(None)
    else:
        r.append(m[0]) # Member Type
        r.append(m[1]) # Member Year
    r.append(row[9]) # Telephone
    r.append(row[12]) # Mobile
    r.append(row[14]) # E-mail
    r.append( convert_cert_date(row[13] + " " + row[11]) ) # Certificate validity date

    return r

def convert_cert_date(date):
    '''Convert the date for the certificate in the right format'''
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

    if len(date.strip()) == 0:
        return None

    d = date.strip().split(" ")

    if len(d) == 1:
        d.append("01")
    
    if len(d) == 2:
        d.append("01")

    if not d[2].isdigit() and d[1].isdigit():
        tmp = d[1]
        d[1] = d[2]
        d[2] = tmp

    if d[1] not in str_to_month:
        d[1] ="01"
    else:
        d[1] = str_to_month[d[1]]

    if len(d) > 3:
        print "Data sbagliata? " + date

    d1 = [x.strip() for x in d]
    return "-".join(d1)

def convert_birth_date(date):
    '''Convert the birth date in the right format'''
    d = date.split("-")
    if len(d) == 1:
        d = date.split("/")
    if len(d) != 3:
        print "Data incompleta: " + date
    d1 = [x.strip() for x in d]
    d1.reverse()
    return "-".join(d1)
