from datetime import datetime

def parse_datetime(datestring, timestring):
    year = 2024

    datetime_string = datestring + ' ' + str(year) + ' ' + convert24(timestring)
    
    dt = datetime.strptime(datetime_string, '%A, %B %d %Y %H:%M:%S')

    if dt.month < 7: dt = dt.replace(year=year+1)

    return dt

def parse_time(timestring):
    checksplit = timestring.split(' ')

    if(len(checksplit) > 3):
        raise ValueError("Incorrect format for timestring")
    time, halfday, timezone = timestring.split(' ', 2)

    return time + ' ' + halfday

def convert24(time):
    # Parse the time string into a datetime object
    t = datetime.strptime(time, '%I:%M %p')
    # Format the datetime object into a 24-hour time string
    return t.strftime('%H:%M:%S')