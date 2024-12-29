import tkinter as tk
import serial.tools.list_ports
import serial as ser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def data_validation(data):
       if data.count(":") != 2: return False#Verify 2 :, valid only to orientation mode 
       x = data.split(":")
       if len(x) != 3: return False#valid only in orientation mode
       for i in x:
              try:
                     float(i)
              except:
                     return False
       return True
def read_serial(): 
       if s.is_open:
              data = s.readline().strip().decode("utf-8",errors = "ignore")#clear \n\r and decode to string
              print(data)
              if data_validation(data): 
                     rot(data)
                     s.reset_input_buffer()
              bt1.after(20,read_serial)#good approximation to 60 fps 
def desconnect():
       s.close()
       bt1["fg"] = "red"
def connect():
       s.baudrate = int(sel2.get())
       p = sel1.get().split(" ")
       s.port = p[0]
       if not s.is_open:
              s.open()
              s.reset_input_buffer()
              bt1["fg"] = "green"
              bt1.after(10,read_serial)#bt1 choosed to use in after method
def RotMat(angs):
       g = angs[0] #gamma
       b = angs[1] #beta
       a = angs[2] #alpha
       sa = np.sin(a)
       ca = np.cos(a)
       sb = np.sin(b)
       cb = np.cos(b)
       sg = np.sin(g)
       cg = np.cos(g)
       m = np.zeros((3,3))
       m[0][0] = ca*cb
       m[0][1] = ca*sb*sg - sa*cg
       m[0][2] = ca*sb*cg + sa*sg
       m[1][0] = sa*cb
       m[1][1] = sa*sb*sg + ca*cg
       m[1][2] = sa*sb*cg - ca*sg
       m[2][0] = -sb
       m[2][1] = cb*sg
       m[2][2] = cb*cg
       return m
       
def rot(line):
       angles = [float(i) for i in line.split(":")]
       R = RotMat(angles)#Rotation Matrix

       xn = [ np.dot(i,x_init_vector) for i in R]
       yn = [ np.dot(i,x_init_vector) for i in R]
       zn = [ np.dot(i,x_init_vector) for i in R]

       for i in range(0,3):
              xn[i] = np.dot(R[i],x_init_vector)
              yn[i] = np.dot(R[i],y_init_vector)
              zn[i] = np.dot(R[i],z_init_vector)

       xplot.set_data_3d([0,xn[0]],[0,xn[1]],[0,xn[2]])
       yplot.set_data_3d([0,yn[0]],[0,yn[1]],[0,yn[2]])
       zplot.set_data_3d([0,zn[0]],[0,zn[1]],[0,zn[2]])
       canvas.draw()

def update():
       rot(e.get())

#Var
root = tk.Tk()
s = ser.Serial()
x_init_vector = np.array([1,0,0])
y_init_vector = np.array([0,1,0])
z_init_vector = np.array([0,0,1])

#Options to OptionMenus
ports = serial.tools.list_ports.comports()
list_ports = [i.device + " " + str(i.manufacturer) for i in ports]
list_baudrates = ["300","1200","2400","4800","9600","19200","38400","57600","74880","115200"]
sel1 = tk.StringVar()
sel1.set(list_ports[-1])
sel2 = tk.StringVar()
sel2.set(list_baudrates[4])
#Option Bar
option_bar = tk.Frame(root)
op1 = tk.OptionMenu(option_bar,sel1,*list_ports)
op2 = tk.OptionMenu(option_bar,sel2,*list_baudrates)
bt1 = tk.Button(option_bar,text = "Connect",command = connect)
bt2 = tk.Button(option_bar,text = "Desconnect",command = desconnect)
ckbt1 = tk.Checkbutton(option_bar,text = "Orientation")
ckbt2 = tk.Checkbutton(option_bar,text = "Position")

#Temp
e = tk.Entry(option_bar)
e.grid(row = 6,column = 0)
e.insert(0,"Pitch:Row:Yaw")
b = tk.Button(option_bar,text = "enviar",command = update)
b.grid(row = 6,column = 1)

#Location of gadgets
op1.grid(row = 0,column = 0)
op2.grid(row = 1,column = 0)
bt1.grid(row = 2,column = 0)
bt2.grid(row = 3,column = 0)
ckbt1.grid(row = 4,column = 0)
ckbt2.grid(row = 5,column = 0)
option_bar.grid(row = 0,column = 0)
#graphs

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
xplot, = ax.plot([0,1], [0,0], [0,0],color = 'r')
yplot, = ax.plot([0,0], [0,1], [0,0],color = 'b')
zplot, = ax.plot([0,0], [0,0], [0,1],color = 'g')
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)
ax.set(xticklabels=[],
       yticklabels=[],
       zticklabels=[])
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(row = 0,column = 1)

root.mainloop()