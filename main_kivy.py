import numpy as np
import scipy as sp
import scipy.optimize

from kivy.app import(App)
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.logger import Logger

import Nodes
import Elements

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
Logger.info('Solve for deformed configuration')
u0 = node_.u[dof_index].copy()
res = sp.optimize.minimize(elem_.U_pot, u0, args=(dof_index))
node_.u[dof_index] = res.x

# Visualization using Kivy
Logger.info('Create Kivy Widget')
class MyWidget(Widget):
    def __init(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

    def init_spheres(self,pos_list,offset=(0,0),scale=1.0,radius=20):
        with self.canvas:
            Color(0.6, 0.6, 0.6, 1.0,mode='rgba')
            Rectangle(size=self.size, pos=self.pos)
            texture = CoreImage('SphereAda_512x512.png').texture
            Color(0.7, 0.7, 1.0, 1.0,mode='rgba')
            for i in range(pos_list.shape[0]):
                Ellipse(texture=texture,pos=(offset[0]+pos_list[i,0]*scale-radius,offset[1]+pos_list[i,1]*scale-radius), size=(radius*2,radius*2))

class MainApp(App):
    def build(self):
        self.r = MyWidget()
        return self.r

    def on_start(self, **kwargs):
        self.r.init_spheres(node_.u,offset=(100,50),scale=25,radius=15)

if __name__ == '__main__':
    MainApp().run()
