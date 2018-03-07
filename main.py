from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.base        import runTouchApp
from kivy.config      import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang        import Builder
from kivy.utils       import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import SlideTransition
import json
from threading import Thread
from kivy.garden.graph import MeshLinePlot, SmoothLinePlot
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, ListProperty
import socket
import time
import paho.mqtt.client as paho
from kivy.utils import get_color_from_hex
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.garden.androidtabs import *
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
import datetime
from kivy.lib import osc
from kivy.utils import platform



broker='106.201.235.43'

global levels_temp
global levels_humidity
global number_of_reactors
global temp_t
global humidity_t


number_of_reactors = 4
temp = [30,30,30,30]

temp_t = []
humidity_t = []
levels_temp = [[30],[30],[30],[30]]
levels_humidity = [[40],[40],[40],[40]]
tempchg = 0
humchg = 0


# def get_data():
#     global s
#     global data
#     global temp
#     global netstatus
#     global netstatus_color
#     global port
#     global dataRecv
#     global levels_temp
#     global levels_humidity
#     time_counter = 0.0
#     global tempchg
#     global humchg
#
#     t = 0
#     time.sleep(0.2)
#     client= paho.Client("banas") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
#     ######Bind function to callback
#     client.on_message=on_message
#     #####
#     # client.username_pw_set("Rahul_1408","650adecd1c964f988aaffbe35fe11766")
#     # print("connecting to broker ",broker)
#     client.connect(broker)#connect
#     client.loop_start() #start loop to process received messages
#     # print("subscribing ")
#     client.subscribe("sensdata")#subscribe
#
#         #c, addr = s.accept()
#
#     while True:
#         data = []
#         olddat = temp
#         tempchg = 0
#         try:
#             arr = json.loads(dataRecv)
#             # print arr
#             for a in arr:
#                 data.append(float(a))
#             temp = data
#
#             if abs(olddat[1] - temp[1]) > 0.25:
#                 tempchg = 1
#             else:
#                 tempchg = 0
#
#             if abs(olddat[0] - temp[0]) > 0.2:
#                 humchg = 1
#             else:
#                 humchg = 0
#
#             for i in range(0,number_of_reactors):
#                 levels_temp[i].append(temp[1])
#                 levels_humidity[i].append(temp[0])
#                 if len(levels_temp[i]) > 7201:
#                     levels_humidity[i].pop(0)
#                     levels_temp[i].pop(0)
#
#
#             # print time_counter/3600
#
#             # print levels
#             netstatus_color = get_color_from_hex('#009B72')
#             netstatus = 'Online'
#             time_counter = time_counter + 1
#
#             # print levels_temp
#         except:
#
#             netstatus = 'No Internet Connection'
#             netstatus_color =  get_color_from_hex('#AF2A3C')
#             temp = [0,0,0,0]
#
#
#
#         time.sleep(0.2)


# # Sets the screen size on computer for development
if platform not in ('android', 'ios'):
    Config.set('graphics', 'resizable', '0')
    Window.size = (414, 736)

# if platform not in ('android', 'ios'):
#   Config.set('graphics', 'resizable', '0')
#   Window.size = (768, 1024)

class RTabs(BoxLayout,AndroidTabsBase):
    pass


class RangeSlider(Slider):
    pass

class TransBox(BoxLayout):
    pass

class RSli(BoxLayout):
    pass
    # def __init__(self,**kwargs):
    #     super(RSli, self).__init__(**kwargs)
    #     self.ids.slival.text = str(self.ids.v)



class Reactabs(AndroidTabs):
    pass
# Internet Status Bar
class NetLab(BoxLayout):
    def __init__(self,**kwargs):
        super(NetLab, self).__init__(**kwargs)

class CanvasCustom(BoxLayout):
    temp_value = NumericProperty(None)
    temp_angle = NumericProperty(None)
    temp_strval = StringProperty(None)
    humidity_value = NumericProperty(None)
    humidity_angle = NumericProperty(None)
    humidity_strval = StringProperty(None)
    sen_color_humidity = ListProperty([])
    main_header_color = ListProperty([])
    sen_color_temp = ListProperty([])
    title = StringProperty(None)

    def __init__(self,**kwargs):
        super(CanvasCustom, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1,0.5)



# Main Screen contaning a grid of reactors
class MenuScreen(Screen):

    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.tempvalue = NumericProperty(levels_temp[0][0])
        Clock.schedule_once(self._finish_init)


    def _finish_init(self, dt):
        if Window.size[0] > 500:
            self.ratio = 5
        else:
            self.ratio = 3



    ######  Transaction functions for on click event for each reactor ########

    # Reactor 1
    def one(self):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current='reactor1'

    # Reactor 2
    def two(self):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current='reactor2'

    # Reactor 3
    def three(self):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current='reactor3'

    def four(self):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current='reactor4'

    def updicon(self):

        if levels_temp[0][0] == 30:
            print levels_temp[0]
            self.ids.reactorlabel1.ids.img_temp_status.source = 'Vectors_img/thermometerred.png'




# Adding button behaviour to each reactor
class BoxButton(ButtonBehavior,BoxLayout):
    pass



############    Main Reactor Screen    ##############

### All the reactor screens are children of this widget

class ReactorScreen(Screen):


    def back(self):
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'main'



#############      Children Screen for each reactor  ############swswwWd##

# Contact = 0
# temp_alert_min = 0
# temp_alert_max = 0
# hum_alert_min = 0
# hum_alert_max = 0
# time_duration = 0
# y_axis_min = 0
# y_axis_max = 0
rangedict = [['No Notification', '', '','down2.png'],['No Notification', '', '','down2.png'],['No Notification', '', '','down2.png']]
# Reactor 1
class ReactorScreen1(ReactorScreen):

    def __init__(self,**kwargs):
        super(ReactorScreen1, self).__init__(**kwargs)
        self.name = "reactor1"
        global rangedict
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 0.7)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('00FCC6'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('00BFFF'))
        self.rangedict = ['No not', '12/10/1', '24']
        self.y_axis_min = 0
        self.y_axis_max = 100
        self.time_duration = 2


    def UpdValues(self):
        # global temp_alert_min
        # global Contact
        # global temp_alert_min
        # global temp_alert_max
        # global hum_alert_min
        # global hum_alert_max
        # global time_duration
        # global y_axis_min
        # global y_axis_max
        Contact = self.ids.Contact.text
        temp_alert_min= self.ids.TempAlMin.v
        temp_alert_max= self.ids.TempAlMax.v
        hum_alert_min= self.ids.HumAlMin.v
        hum_alert_max= self.ids.HumAlMax.v
        self.time_duration = int(self.ids.TimeDuration.v)
        self.ids.graph_temp.xmin= -1* int(self.ids.TimeDuration.v)
        self.ids.graph_temp.xmax = 0
        self.ids.graph_temp.ymin= int(self.ids.YAxisMin.v)
        self.ids.graph_temp.ymax = int(self.ids.YAxisMax.v)
        settings = [temp_alert_min,temp_alert_max,hum_alert_min,hum_alert_max]
        osc.sendMsg('/settings_data', settings , port=3000)





    def _finish_init(self, dt):
        self.ids.main_label.text = "[b]Production[/b]"
        if Window.size[0] > 500:
            self.ratio = 6
            self.ratio_high = 0.010
        else:
            self.ratio = 3
            self.ratio_high = 0.015





    def get_value(self,dt):
        # global temp_alert_min
        # global rangedict
        # global temp
        # global temp_alert_max
        # global hum_alert_min
        # global hum_alert_max
        # global time_duration
        # global y_axis_min
        # global y_axis_max
        # global tempchg
        # global humchg
        global rangedict
        global temp
        global levels_humidity
        global levels_temp
        self.ids.Not1des.text = rangedict[-1][0]
        self.ids.Not1time.text = rangedict[-1][1]
        self.ids.Not1Val.text = rangedict[-1][2]
        self.ids.Not1IndPic.source = rangedict[-1][3]
        self.ids.Not2des.text = rangedict[-2][0]
        self.ids.Not2time.text = rangedict[-2][1]
        self.ids.Not2Val.text = rangedict[-2][2]
        self.ids.Not2IndPic.source = rangedict[-2][3]
        self.ids.Not3des.text = rangedict[-3][0]
        self.ids.Not3time.text = rangedict[-3][1]
        self.ids.Not3Val.text = rangedict[-3][2]
        self.ids.Not3IndPic.source = rangedict[-3][3]

        # if tempchg == 1:
        #
        #     if temp[1] < temp_alert_min:
        #
        #         t = str(datetime.datetime.now())
        #         v = str(temp[1])
        #         l = ["Low Temperature", t, v,'down3.png']
        #         rangedict[-3] = rangedict[-2]
        #         rangedict[-2] = rangedict[-1]
        #         rangedict[-1] = l
        #         print rangedict
        #
        #
        #
        #     if temp[1] > temp_alert_max:
        #         t = str(datetime.datetime.now())
        #         v = str(temp[1])
        #         l = ["High Temperature", t, v, 'up.png']
        #         rangedict[-3] = rangedict[-2]
        #         rangedict[-2] = rangedict[-1]
        #         rangedict[-1] = l
        #         self.rangedict = rangedict[0]
        #         print rangedict
        #
        #
        # if humchg == 1:
        #
        #     if temp[0] < hum_alert_min:
        #         t = str(datetime.datetime.now())
        #         v = str(temp[0])
        #         l = ["Low Humidity", t, v, 'down3.png']
        #         rangedict[-3] = rangedict[-2]
        #         rangedict[-2] = rangedict[-1]
        #         rangedict[-1] = l
        #         self.rangedict = rangedict[0]
        #         print rangedict
        #
        #
        #
        #
        #
        #     if temp[0] > hum_alert_max:
        #         t = str(datetime.datetime.now())
        #         v = str(temp[0])
        #         l = ["High Humidity", t, v, 'up.png']
        #         rangedict[-3] = rangedict[-2]
        #         rangedict[-2] = rangedict[-1]
        #         rangedict[-1] = l
        #         self.rangedict = rangedict[0]
        #         print rangedict
        #


        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp)
        self.ids.graph_temp.add_plot(self.plot_humidity)
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.ids.net1.netstattxt = netstatus
        self.ids.net1.netstatuscolor = netstatus_color

        self.plot_temp.points = [((i/3600.00)-int(self.time_duration),j) for i,j in enumerate(levels_temp[0])]
        self.plot_humidity.points = [((i/3600.00)-int(self.time_duration),j) for i,j in enumerate(levels_humidity[0])]
        # print self.plot.points
        print temp
        self.temp_value = temp[1]
        self.humidity_value = temp[0]
        self.temp_angle = 1.8*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 1.8*self.humidity_value
        self.sen_color_temp = get_color_from_hex('#23C48E');
        self.sen_color_humidity = get_color_from_hex('#04C0F8');





# Reactor 2
class ReactorScreen2(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen2, self).__init__(**kwargs)
        self.name = "reactor2"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#23C48E'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#04C0F8'))
        self.rangedict = ['No not', '12/10/1', '24']
        self.y_axis_min = 0
        self.y_axis_max = 100
        self.time_duration = 2


    def UpdValues(self):
        # global temp_alert_min
        # global Contact
        # global temp_alert_min
        # global temp_alert_max
        # global hum_alert_min
        # global hum_alert_max
        # global time_duration
        # global y_axis_min
        # global y_axis_max
        Contact = self.ids.Contact.text
        temp_alert_min= self.ids.TempAlMin.v
        temp_alert_max= self.ids.TempAlMax.v
        hum_alert_min= self.ids.HumAlMin.v
        hum_alert_max= self.ids.HumAlMax.v
        self.time_duration= self.ids.TimeDuration.v
        self.y_axis_min= self.ids.YAxisMin.v
        self.y_axis_max= self.ids.YAxisMax.v
        settings = [temp_alert_min,temp_alert_max,hum_alert_min,hum_alert_max]


    def _finish_init(self, dt):

        self.ids.main_label.text = "PACKAGING"
        if Window.size[0] > 500:
            self.ratio = 6
            self.ratio_high = 0.010
        else:
            self.ratio = 3
            self.ratio_high = 0.015



    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_temp.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [((i/3600.00)-self.time_duration,j) for i,j in enumerate(levels_temp[1])]
        self.plot_humidity.points = [((i/3600.00)-self.time_duration,j) for i,j in enumerate(levels_humidity[1])]
        # print self.plot.points
        self.temp_value = temp[1]
        self.humidity_value = temp[0]
        self.temp_angle = 1.8*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 1.8*self.humidity_value

        self.sen_color_temp = get_color_from_hex('#23C48E');
        self.sen_color_humidity = get_color_from_hex('#04C0F8');

# Reactor 3
class ReactorScreen3(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen3, self).__init__(**kwargs)
        self.name = "reactor3"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#23C48E'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#04C0F8'))
        self.rangedict = ['No not', '12/10/1', '24']
        self.y_axis_min = 0
        self.y_axis_max = 100
        self.time_duration = 2


    def UpdValues(self):
        # global temp_alert_min
        # global Contact
        # global temp_alert_min
        # global temp_alert_max
        # global hum_alert_min
        # global hum_alert_max
        # global time_duration
        # global y_axis_min
        # global y_axis_max
        Contact = self.ids.Contact.text
        temp_alert_min= self.ids.TempAlMin.v
        temp_alert_max= self.ids.TempAlMax.v
        hum_alert_min= self.ids.HumAlMin.v
        hum_alert_max= self.ids.HumAlMax.v
        self.time_duration= self.ids.TimeDuration.v
        self.y_axis_min= self.ids.YAxisMin.v
        self.y_axis_max= self.ids.YAxisMax.v
        settings = [temp_alert_min,temp_alert_max,hum_alert_min,hum_alert_max]


    def _finish_init(self, dt):
        self.ids.main_label.text = "STORAGE"
        if Window.size[0] > 500:
            self.ratio = 6
            self.ratio_high = 0.010
        else:
            self.ratio = 3
            self.ratio_high = 0.015



    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_temp.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [((i/3600.00)-2.00,j) for i,j in enumerate(levels_temp[2])]
        self.plot_humidity.points = [((i/3600.00)-2.00,j) for i,j in enumerate(levels_humidity[2])]
        # print self.plot.points
        self.temp_value = temp[1]
        self.humidity_value = temp[0]
        self.temp_angle = 1.8*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 1.8*self.humidity_value
        self.sen_color_temp = get_color_from_hex('#23C48E');
        self.sen_color_humidity = get_color_from_hex('#04C0F8');

class ReactorScreen4(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen4, self).__init__(**kwargs)
        self.name = "reactor4"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#23C48E'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#04C0F8'))
        self.rangedict = ['No not', '12/10/1', '24']
        self.y_axis_min = 0
        self.y_axis_max = 100
        self.time_duration = 2


    def UpdValues(self):
        Contact = self.ids.Contact.text
        temp_alert_min= self.ids.TempAlMin.v
        temp_alert_max= self.ids.TempAlMax.v
        hum_alert_min= self.ids.HumAlMin.v
        hum_alert_max= self.ids.HumAlMax.v
        self.time_duration= self.ids.TimeDuration.v
        self.y_axis_min= self.ids.YAxisMin.v
        self.y_axis_max= self.ids.YAxisMax.v
        settings = [temp_alert_min,temp_alert_max,hum_alert_min,hum_alert_max]


    def _finish_init(self, dt):
        self.ids.main_label.text = "SENSOR 4"
        if Window.size[0] > 500:
            self.ratio = 6
            self.ratio_high = 0.010
        else:
            self.ratio = 3
            self.ratio_high = 0.015



    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_temp.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [(i/3600.0-2.0,j) for i,j in enumerate(levels_temp[3])]
        self.plot_humidity.points = [((i/3600.00)-2.00,j) for i,j in enumerate(levels_humidity[3])]
        self.temp_value = temp[1]
        self.humidity_value = temp[0]
        self.temp_angle = 1.8*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 1.8*self.humidity_value
        self.sen_color_temp = get_color_from_hex('#23C48E');
        self.sen_color_humidity = get_color_from_hex('#04C0F8');



class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("MyApp.kv")

class MyApp(App):

    def temp_data(self, message, *args):
        global temp
        global levels_temp
        global levels_humidity
        global netstatus
        global netstatus_color
        try:
            temp = [message[2],message[3],message[4],message[5]]
            for i in range(0,number_of_reactors):
                # tupdattemp = (time_counter/3600-2.0,temp[1])
                # tupdathum = (time_counter/3600-2.0,temp[0])
                levels_temp[i].append(temp[1])
                levels_humidity[i].append(temp[0])
                if len(levels_temp[i]) > 7201:
                    levels_humidity[i].pop(0)
                    levels_temp[i].pop(0)
            netstatus_color = get_color_from_hex('#009B72')
            netstatus = 'Online'

        except:
            netstatus = 'No Internet Connection'
            netstatus_color =  get_color_from_hex('#AF2A3C')
            temp = [0,0,0,0]

    def notification_data(self, message, *args):
        global rangedict
        try:
            rangedictp = [message[2],message[3],message[4],message[5]]
            rangedict[-3] = rangedict[-2]
            rangedict[-2] = rangedict[-1]
            rangedict[-1] = rangedictp

        except:
            print 'failed'


    def start_service(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('my data service', 'running')
            service.start('service started')
            self.service = service

    def build(self):
        self.service = None
        self.start_service()
        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=3002)
        osc.bind(oscid, self.temp_data, '/sensordata')
        osc.bind(oscid, self.notification_data, '/notification')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0.7)
        return presentation


if __name__ == '__main__':
    data = []
    print platform
    temp = [30,80,30,30]
    dataRecv = ''
    netstatus = 'Waiting for Network...'
    netstatus_color = get_color_from_hex('#F26430')
    MyApp().run()