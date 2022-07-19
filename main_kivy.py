import numpy as np
import scipy as sp
import scipy.optimize

from kivy.app import(App)
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.core.image import Image as CoreImage

import Nodes
import Elements

### Initial setting: Spring element case

node_ = Nodes.Nodes();
elem_ = Elements.Elements(node_);
bc_index = range(node_.nc,node_.n-node_.nc);

class MyWidget(Widget):
    def __init(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

    def init_spheres(self,pos_list,offset=(0,0),scale=1.0,radius=20):
        with self.canvas:
            texture = CoreImage('SphereAda_512x512.png').texture
            Color(1.0,1.0,1.0,1.0,mode='rgba')
            for i in range(pos_list.shape[0]):
                Ellipse(texture=texture,pos=(offset[0]+pos_list[i,0]*scale-radius,offset[1]+pos_list[i,1]*scale-radius), size=(radius*2,radius*2))

class MainApp(App):
    def build(self):
        self.r = MyWidget()
        return self.r

    def on_start(self, **kwargs):
        self.r.init_spheres(node_.u,offset=(100,100),scale=80,radius=40)

if __name__ == '__main__':
    MainApp().run()
