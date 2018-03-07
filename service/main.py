import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lib import osc
import paho.mqtt.client as paho
import time
import json 
import datetime
from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2





class NotificationDemo(App):
	def __init__(self,**kwargs):
		super(NotificationDemo, self).__init__(**kwargs)
		self.temp = [0,0,0,0]
		self.tempchg = None
		self.humchg = None
		self.dataRecv = '[0,0,0,0]'
		self.broker='106.201.235.43'
		self.service = 3000
		osc.init()
		self.oscid = osc.listen(ipAddr='127.0.0.1', port=3000)
		osc.bind(self.oscid, self.settings_data, '/settings_data')
		self.alert_settings = [20,40,20,50]
		self.notifications_received = ObjectProperty(None)
		self.notification_title = ObjectProperty(None)
		self.notification_text = ObjectProperty(None)
		self.olddat = [0,0,0,0]
		self.notification_msg = ['No Notification', '', '','down2.png']
		self.a = 0
				

	
	

	def settings_data(self, message, *args):
		# print("got a message! %s" % message)
		for i in range(2,6):
			self.alert_settings[i-2] = message[i]

	def send_data(self):
		osc.sendMsg('/sensordata',self.temp,port=3002)

	def send_notification(self):
		# print self.notification_msg
		# print self.notification_msg
		osc.sendMsg('/notification',self.notification_msg,port=3002)


	def on_message(self, client, userdata, message):
		time.sleep(0.2)
		self.dataRecv = str(message.payload.decode("utf-8"))
		# print self.dataRecv


	def do_notify(self,title,message):
		if PY2:
			title = title.decode('utf8')
			message = message.decode('utf8')
		kwargs = {'title': title, 'message': message, 'ticker': 10, 'app_name': 'WHTT','timeout': 10}
		notification.notify(**kwargs)

        # if mode == 'fancy':
        #     kwargs['app_name'] = "Plyer Notification Example"
        #     if platform == "win":
        #         kwargs['app_icon'] = join(dirname(realpath(__file__)),
        #                                   'plyer-icon.ico')
        #         kwargs['timeout'] = 4
        #     else:
        #         kwargs['app_icon'] = join(dirname(realpath(__file__)),
        #                                   'plyer-icon.png')


	def get_data(self):
		try:
		   
			client= paho.Client("banas1") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
			######Bind function to callback
			client.on_message=self.on_message
			#####
			# client.username_pw_set("Rahul_1408","650adecd1c964f988aaffbe35fe11766")
			# print("connecting to broker ",broker)
			client.connect(self.broker)#connect
			client.loop_start() #start loop to process received messages
			# print("subscribing ")
			client.subscribe("sensdata")#subscribe  

		except:
			print 'false'
			#c, addr = s.accept()s

		while True:
			try:
				data = []
				self.olddat = self.temp
				self.tempchg = 0
				# print self.dataRecv

				arr = json.loads(self.dataRecv)
				# print arr
				for a in arr:
					data.append(float(a))
				self.temp = data
				self.send_data()

				if self.a  > 10:
					if self.temp[1] < self.alert_settings[0]:
						self.a = 0
						self.do_notify('Low Temp', 'Low Temperature Observed'+' :'+str(self.temp[1]))
						t = str(datetime.datetime.now())
						v = str(self.temp[1])
						l = ["Low Temperature", t, v,'down3.png']
						self.notification_msg = l
						self.send_notification()
					if self.temp[1] > self.alert_settings[1]:
						self.do_notify('High Temp', 'High Temperature Observed'+' :'+str(self.temp[1]))
						t = str(datetime.datetime.now())
						v = str(self.temp[1])
						l = ["High Temperature", t, v,'up.png']
						self.notification_msg = l
						self.send_notification()
						
					

				if abs(self.olddat[0] - self.temp[0]) > 0.04:
					if self.temp[0] < self.alert_settings[2]:
						self.do_notify('Low Temp', 'Low Humidity Observed'+' :'+str(self.temp[0]))
						t = str(datetime.datetime.now())
						v = str(self.temp[0])
						l = ["Low Humidity", t, v,'down3.png']
						# self.notification_msg[-3] = self.notification_msg[-2]
						# self.notification_msg[-2] = self.notification_msg[-1]
						self.notification_msg = l
						self.send_notification()
					if self.temp[0] > self.alert_settings[3]:
						self.do_notify('High Humidity', 'High Humidity Observed'+' :'+str(self.temp[0]))
						t = str(datetime.datetime.now())
						v = str(self.temp[0])
						l = ["High Humidity", t, v,'up.png']
						# self.notification_msg[-3] = self.notification_msg[-2]
						# self.notification_msg[-2] = self.notification_msg[-1]
						self.notification_msg = l
						self.send_notification()

				osc.readQueue(self.oscid)
				time.sleep(0.7)
				self.a = self.a + 1
			except:
				print 'yes'
        
            

	            

	        	



class NotificationDemoApp(App):
	def build(self):
		n = NotificationDemo()
		n.get_data()
		

if __name__ == '__main__':
	NotificationDemoApp().run()



