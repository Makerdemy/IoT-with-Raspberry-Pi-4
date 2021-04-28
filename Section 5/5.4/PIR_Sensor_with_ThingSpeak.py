import paho.mqtt.publish as publish
from gpiozero import MotionSensor

channelID = "XXXXXXX" #enter your channel ID here

apiKey = "YYYYYYYYYYYYYYYYY" #enter the WRITE API key of your channel here

useUnsecuredTCP = False

useUnsecuredWebsockets = False

useSSLWebsockets = True


mqttHost = "mqtt.thingspeak.com"


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

pir = MotionSensor(17)

while(True):
    
    print ("PIR sensor output is", pir.motion_detected)

    tPayload = "field1=" + str(pir.motion_detected)

    # attempt to publish this data to the topic 
    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")


