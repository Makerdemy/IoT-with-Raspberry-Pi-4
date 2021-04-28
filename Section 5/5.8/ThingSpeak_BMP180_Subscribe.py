import paho.mqtt.client as mqttClient
import random
import i2c_lcd
import time
import json

lcd_display = i2c_lcd.lcd()

def on_connect(client, userdata, flags, rc):  
    if rc == 0: 
        print("Connected to broker") 
        global Connected            	
        Connected = True            	  
    else:  
        print("Connection failed")
  
def on_message(client, userdata, message):  
    data = json.loads(message.payload)    
    temp = float(data['field1'])
    print(temp) 
    lcd_display.lcd_display_string("Temperature:" + str(temp), 1)
          
Connected = False   
  
broker_address= "mqtt.thingspeak.com"  #Broker address
port = 1883                            #Broker port
user = "pi_lcd"                	#Connection username
password = "XITGLH8YE2Z1D0H6"   #Connection password - Use your MQTT API key here
client_id = f'subscribe-{random.randint(0, 100)}'
channelID = "1304227"                           #Use your Channel ID here
READapiKey = "OTGP1BJBV3QK0FB9"                 #Use your Read API key here

client = mqttClient.Client(client_id)           #create new instance
client.username_pw_set(user, password=password)	#set username and password
client.on_connect= on_connect                  	#attach function to callback
client.on_message= on_message                  	#attach function to callback  
client.connect(broker_address, port=port)      	#connect to broker  
client.loop_start()    	                        #start the loop
  
while Connected != True:	                #Wait for connection
    time.sleep(0.1)
   
topic = "channels/" + channelID + "/subscribe/json/" + READapiKey

try:
    client.subscribe(topic, qos=0)

    while True:    
        time.sleep(1)
        
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()


