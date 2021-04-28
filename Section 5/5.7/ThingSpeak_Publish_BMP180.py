import paho.mqtt.publish as publish
from bmp180 import bmp180
import smbus


channelID = "XXXXX"  #Enter your Channel ID here

apiKey = "YYYYYYYYYYYYY"  #Enter your WriteAPI key here

mqttHost = "mqtt.thingspeak.com"

useUnsecuredTCP = False

useUnsecuredWebsockets = False

useSSLWebsockets = True


if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
topic = "channels/" + channelID + "/publish/" + apiKey


sensor = bmp180(0x77)

temp = ""
pressure = ""

while(True):
    
    temp = sensor.get_temp()
    pressure = sensor.get_pressure()
    
    print (" Temperature =",temp ,"   Pressure =", pressure)

    tPayload = "field1=" + str(temp) + "&field2=" + str(pressure)

    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")