import obd

connection = obd.OBD("/dev/ttyUSB0", baudrate=9600) # auto-connects to USB or RF port

i = 1
while True:
    cmd = obd.commands.SPEED # select an OBD command (sensor)
    response = connection.query(cmd) # send the command, and parse the response
    print(response.value) # returns unit-bearing values thanks to Pint
    i = i + 1
    print(i)


#print(response.value.to("kph")) # user-friendly unit conversions

