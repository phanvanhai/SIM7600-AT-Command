import sys
import sim
import time

URL = 'http://httpbin.org/post'
ContentType = 'application/json'
body = '{"Temperature(oC)":29.0,"Humidity(%)":74.5,"PM2.5(ug_m3)":30.0}'

HTTP_CONNECT_TIMEOUT = 20   #s
HTTP_RESPONSE_TIMEOUT = 5   #s

SIM_SERIAL_PORT = '/dev/ttyUSB0'
SIM_SERIAL_BAUD = 115200
POWER_KEY = 6

# ---------------------- MAIN ---------------------
# init SIM
sim.power_on(POWER_KEY)
ok = sim.at_init(SIM_SERIAL_PORT, SIM_SERIAL_BAUD, False)
if not ok:
    print('SIM AT init error')
    sys.exit(1)

main_is_run = True

sim.gps_start()
# loop
try:
    while main_is_run:
        time.sleep(2)
        # Get Time
        time_sim = sim.time_get()
        if time_sim != '':
            print('Time:' + time_sim)
        
        # time.sleep(2)
        # Get GPS    
        count = count + 1        
        gps, ok = sim.gps_get_data()
        if ok:            
            print('Time:' + str(count) + ' GPS:' + gps)
        else:
            print('Time:' + str(count) + ' GPS not ready')
        # time.sleep(2)
        # POST HTTP        
        print('Send data to Server:' + URL)
        print(body)
        ok = sim.http_post(URL, ContentType, body, '',HTTP_CONNECT_TIMEOUT, HTTP_RESPONSE_TIMEOUT)
        if not ok:
            print('Error send data to Server')        
    
except KeyboardInterrupt:
    main_is_run = False
    sim.gps_stop()
    sim.at_close()
    sim.power_down(POWER_KEY)