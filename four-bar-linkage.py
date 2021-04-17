import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set windows
window = Tk()
window.geometry("800x800")
window.title("Four bar linkage Mechanism")


class App:
    def __init__(self, master):
        # Plot Settings
        self.fig = plt.figure(1)
        # Graph params for link
        self.link,   = plt.plot([], [], 'r-', linewidth=4)
        # Graph params for joint
        self.joints, = plt.plot([], [], marker='o', ls="", markersize=10)
        # 1)Create a plot
        self.plot1 = FigureCanvasTkAgg(self.fig, master=window).get_tk_widget()
        # 2)Input fields
        self.entry1 = IntVar()
        self.entry2 = IntVar()
        self.entry3 = IntVar()
        self.entry4 = IntVar()
        self.input1 = Entry(window, textvariable=self.entry1)
        self.input2 = Entry(window, textvariable=self.entry2)
        self.input3 = Entry(window, textvariable=self.entry3)
        self.input4 = Entry(window, textvariable=self.entry4)
        # 3)Button:
        self.button1 = Button(window, text="START", command=self.start)
        self.button2 = Button(window, text="STOP", command=self.stop)
        # 4)Label:
        self.output1 = Label(window, text="Longest:")
        self.output2 = Label(window, text="Smallest:")
        self.output3 = Label(window, text="L3:")
        self.output4 = Label(window, text="L4:")
        self.warning = Label(window, text="")
        self.label = Label(
            window, text="Done by group 10")
        # Locations
        self.plot1.place(x=0, y=0, height=500, width=800)
        self.output1.place(x=0, y=500, height=20, width=100)
        self.input1.place(x=100, y=500, height=20, width=100)
        self.output2.place(x=200, y=500, height=20, width=100)
        self.input2.place(x=300, y=500, height=20, width=100)
        self.output3.place(x=400, y=500, height=20, width=100)
        self.input3.place(x=500, y=500, height=20, width=100)
        self.output4.place(x=600, y=500, height=20, width=100)
        self.input4.place(x=700, y=500, height=20, width=100)
        self.warning.place(x=100, y=550, height=20, width=600)
        self.label.place(x=550, y=660, height=20, width=300)
        self.button1.place(x=100, y=600, height=30, width=200)
        self.button2.place(x=500, y=600, height=30, width=200)
        # 5)Mechanism Animation
        self.anim = animation.FuncAnimation(self.fig, self.animate, np.arange(
            0, 2*np.pi, 0.01), interval=10, blit=False)
        # Start and stop Animation
        self.k = 0  # (0, 1) :: (stop, start).

# Calc variables based on theta2:
    def calculate(self, theta2):
        L1 = self.L1
        L2 = self.L2
        L3 = self.L3
        L4 = self.L4
        BD = np.sqrt(L1**2+L2**2-2*L1*L2*np.cos(theta2))
        alfa = np.arccos((L3**2+L4**2-BD**2)/(2*L3*L4))
        theta3 = 2*np.arctan((-L2*np.sin(theta2)+L4*np.sin(alfa)) /
                             (L1+L3-L2*np.cos(theta2)-L4*np.cos(alfa)))
        theta4 = 2*np.arctan((L2*np.sin(theta2)-L3*np.sin(alfa)) /
                             (L4-L1+L2*np.cos(theta2)-L3*np.cos(alfa)))
        # (x, y) of A, B, C, D
        A = [0, 0]
        B = [L2*np.cos(theta2), L2*np.sin(theta2)]
        C = [L2*np.cos(theta2)+L3*np.cos(theta3), L2 *
             np.sin(theta2)+L3*np.sin(theta3)]
        D = [L1, 0]
        return BD, alfa, theta3, theta4, A, B, C, D

# Automatic Axis adjuster
    def axis_setter(self):
        L1 = self.L1  # from constructor.
        t2 = np.arange(0, 2*np.pi, 0.01)
        BD, alfa, theta3, theta4, A, B, C, D = self.calculate(t2)
        B = np.array(B)
        C = np.array(C)
        K = C.max(axis=1)
        M = C.min(axis=1)
        Cx_max = K[0]
        Cy_max = K[1]
        Cx_min = M[0]
        Cy_min = M[1]
        F = [np.amin(B), M[0]]
        G = [np.amin(B), M[1]]
        upper_x = L1 + abs(Cx_max-L1) + 0.5
        lower_x = np.amin(F) - 0.5
        upper_y = Cy_max + 0.5
        lower_y = np.amin(G) - 0.5
        del BD, alfa, theta3, theta4, A, B, C, D, t2
        return upper_x, lower_x, upper_y, lower_y
# --------------------------------------------------------------
# When Started:

    def start(self):  # Since variable k is registered in self, it is enough to input self, not self.k!
        self.L1 = self.entry1.get()
        self.L2 = self.entry2.get()
        self.L3 = self.entry3.get()
        self.L4 = self.entry4.get()
        try:
            upper_x, lower_x, upper_y, lower_y = self.axis_setter()
            plt.axis([lower_x, upper_x, lower_y, upper_y])  # Set Axis
            plt.gca().set_aspect('equal', adjustable='box')
            self.k = 1
            self.anim.event_source.start()  # Animation loop
            self.warning.config(text="", background="white")
        except:
            self.warning.config(
                text="Error in link lengths.", background="red", font=("Courier", 14))
            self.stop()
        return self.k
# When the stop button is pressed:

    def stop(self):
        self.k = 0  # Stop animation
        return self.k
# Animation part theta2 = 0: 0.01: 2pi

    def animate(self, theta2):
        if (self.k == 0):
            self.anim.event_source.stop()  # exit animate loop\
        else:
            # Instantaneous parameter values ​​of the mechanism
            BD, alfa, theta3, theta4, A, B, C, D = self.calculate(theta2)
            x = [A[0], B[0], C[0], D[0]]  # X of joint
            y = [A[1], B[1], C[1], D[1]]  # Y of joint
            self.link.set_data(x, y)  # Instant location of links plotted
            # The instantaneous location of the joints has been plotted.
            self.joints.set_data(x, y)
        return self.link, self.joints


App(window)  # App is active
mainloop()  # Window is always open in loop
