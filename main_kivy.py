import numpy as np
import scipy as sp
import scipy.optimize

from kivy.app import(App)
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.logger import Logger

import Nodes
import Elements

do_relax = True

### Initial setting: Spring element case

Logger.info('Load initial nodes and elements')
node_ = Nodes.Nodes(20, crack=(8, 10))
elem_ = Elements.Elements(node_)

# Set up boundary condition (Degrees of freedom)
dof_index = np.zeros_like(node_.u, dtype=bool)
interior_node_index = np.isin(np.arange(node_.n), np.arange(node_.nx, node_.n - node_.nx))
dof_index[interior_node_index, :2] = True                   # all interior nodes are DOFs (x, y coords)
dof_index[np.logical_not(interior_node_index), 0] = True    # all boundary nodes x are allowed to move
dof_index[0, 0] = False                                     # anchor point at the lower left

# Set up initial condition
ey = -0.1
node_.u[np.logical_not(interior_node_index), 1] *= (1-ey)

# Solve for deformed configuration
if do_relax:
    Logger.info('Solve for deformed configuration (this can take a few seconds...)')
    u0 = node_.u[dof_index].copy()
    res = sp.optimize.minimize(elem_.U_pot, u0, args=(dof_index))
    node_.u[dof_index] = res.x

# Visualization using Kivy
Logger.info('Create Kivy Widget')
class MySample(Layout):
    def __init(self, **kwargs):
        super(MySample, self).__init__(**kwargs)

    def init_spheres(self,pos_list,offset=(0,0),scale=1.0,radius=20):
        with self.canvas:
            texture = CoreImage('SphereAda_512x512.png').texture
            Color(0.7, 0.7, 1.0, 1.0, mode='rgba')
            for i in range(pos_list.shape[0]):
                Ellipse(texture=texture,pos=(offset[0]+pos_list[i,0]*scale-radius,offset[1]+pos_list[i,1]*scale-radius), size=(radius*2,radius*2))

class WidgetContainer(GridLayout):

    def __init__(self, **kwargs):
        super(WidgetContainer, self).__init__(**kwargs)

        # 3 columns in grid layout
        self.cols = 2

        # title
        self.add_widget(Label(text='Sample', font_size='30sp', bold=True, color=[55/255,13/255,191/255,1], size_hint=(0.8,0.1)))

        # title
        self.add_widget(Label(text='Force', font_size='30sp', bold=True, color=[75/255,204/255,201/255,1], size_hint=(0.2,0.1)))

        # the sample being deformed
        self.sample = MySample(size_hint=(0.8,0.9))
        self.add_widget(self.sample)

        # declaring the slider and adding some effects to it
        self.forceControl = Slider(min = 0, max = 100, value = 40, orientation='vertical', size_hint=(0.2,0.9))
        self.add_widget(self.forceControl)

        # On the slider object Attach a callback
        # for the attribute named value
        #self.forceControl.bind(value = self.on_value)

    # Adding functionality behind the slider
    # i.e when pressed increase the value
    #def on_value(self, instance, force):
    #    self.forceValue.text = "% d"% force

class MainApp(App):
    def build(self):
        self.r = root = WidgetContainer()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0.6, 0.6, 0.6, 1.0, mode='rgba')
            self.rect = Rectangle(size=root.size, pos=root.pos)

        return self.r

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_start(self, **kwargs):
        self.r.sample.init_spheres(node_.u,offset=(100,50),scale=25,radius=15)


#class MainApp(App):
#    def build(self):
#        self.r = MyWidget()
#        return self.r
#
#    def on_start(self, **kwargs):
#        self.r.init_spheres(node_.u,offset=(100,50),scale=25,radius=15)

if __name__ == '__main__':
    MainApp().run()
