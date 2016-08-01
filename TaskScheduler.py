import schedule         # pip install schedule
from tkinter import *
from time import *
import datetime as dt
import threading

weekdict = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
monthdict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}


class MyApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        Tk.title(self, "Task Scheduler")
        Tk.geometry(self, "600x380+0+0")
        days = range(1, 32)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        years = range(2016, 2100)
        hours = range(0, 24)
        minutes = range(0, 60)
        seconds = range(0, 60)
        self.tasks = set()
        self.rb = 0
        self.gap = 0

        Canvas(self, width=596, height=1, bg="#bfbfbf").place(x=0, y=48)
        Canvas(self, width=585, height=1, bg="#bfbfbf").place(x=5, y=65)
        Canvas(self, width=585, height=1, bg="#bfbfbf").place(x=5, y=370)
        Canvas(self, width=1, height=305, bg="#bfbfbf").place(x=5, y=65)
        Canvas(self, width=1, height=305, bg="#bfbfbf").place(x=590, y=65)
        Label(self, text="Task Name").place(x=20, y=15)
        self.entry = Entry(self, width=80)
        self.entry.place(x=85, y=15)

        Label(self, text="Schedule on every:").place(x=20, y=55)
        self.rbvar = IntVar(self)
        Radiobutton(self, text="Once in every:", variable=self.rbvar, value=1, command=self.sel).place(x=20, y=80)
        Label(self, text="Duration:").place(x=140, y=82)
        self.hrvar0 = StringVar(self)
        self.hrvar0.set('hh')
        self.mivar0 = StringVar(self)
        self.mivar0.set('mm')
        self.scvar0 = StringVar(self)
        self.scvar0.set('ss')
        OptionMenu(self, self.hrvar0, *hours).place(x=208, y=77)
        OptionMenu(self, self.mivar0, *minutes).place(x=265, y=77)
        OptionMenu(self, self.scvar0, *seconds).place(x=330, y=77)
        Canvas(self, width=572, height=1, bg="#bfbfbf").place(x=12, y=115)

        Radiobutton(self, text="One time:", variable=self.rbvar, value=2, command=self.sel).place(x=20, y=130)
        Label(self, text="Date:").place(x=140, y=132)
        self.yvar = StringVar(self)
        self.yvar.set('yy')
        self.mvar = StringVar(self)
        self.mvar.set('mm')
        self.dvar = StringVar(self)
        self.dvar.set('dd')
        OptionMenu(self, self.yvar, *years).place(x=180, y=127)
        OptionMenu(self, self.mvar, *months).place(x=235, y=127)
        '''
        yr = int(self.yvar.get())
        mon = self.mvar.get()    # This is happening even before the assignment to self.yvar, self.mvar, self.dvar
        if mon == 'Feb':
            if yr % 4 == 0:
                days = range(1, 30)
            else:
                days = range(1, 29)
        elif mon in ['Apr', 'Jun', 'Sep', 'Nov']:
            days = range(1, 31)
        '''
        OptionMenu(self, self.dvar, *days).place(x=300, y=127)
        Label(self, text="at", padx=10).place(x=357, y=132)
        self.hrvar1 = StringVar(self)
        self.hrvar1.set('hh')
        self.mivar1 = StringVar(self)
        self.mivar1.set('mm')
        self.scvar1 = StringVar(self)
        self.scvar1.set('ss')
        OptionMenu(self, self.hrvar1, *hours).place(x=388, y=127)
        OptionMenu(self, self.mivar1, *minutes).place(x=445, y=127)
        OptionMenu(self, self.scvar1, *seconds).place(x=510, y=127)
        Canvas(self, width=572, height=1, bg="#bfbfbf").place(x=12, y=165)

        Radiobutton(self, text="Day:", variable=self.rbvar, value=3, command=self.sel).place(x=20, y=180)
        Label(self, text="Recur once in every ").place(x=140, y=182)
        self.rdayvar = StringVar(self)
        Entry(self, width=3, textvariable=self.rdayvar).place(x=254, y=185)
        Label(self, text=" days at ").place(x=278, y=182)
        self.hrvar2 = StringVar(self)
        self.hrvar2.set('hh')
        self.mivar2 = StringVar(self)
        self.mivar2.set('mm')
        self.scvar2 = StringVar(self)
        self.scvar2.set('ss')
        OptionMenu(self, self.hrvar2, *hours).place(x=330, y=179)
        OptionMenu(self, self.mivar2, *minutes).place(x=388, y=179)
        OptionMenu(self, self.scvar2, *seconds).place(x=455, y=179)
        Canvas(self, width=572, height=1, bg="#bfbfbf").place(x=12, y=218)

        Radiobutton(self, text="Week:", variable=self.rbvar, value=4, command=self.sel).place(x=20, y=233)
        Label(self, text="Recur every week at").place(x=140, y=235)
        self.hrvar3 = StringVar(self)
        self.hrvar3.set('hh')
        self.mivar3 = StringVar(self)
        self.mivar3.set('mm')
        self.scvar3 = StringVar(self)
        self.scvar3.set('ss')
        OptionMenu(self, self.hrvar3, *hours).place(x=255, y=230)
        OptionMenu(self, self.mivar3, *minutes).place(x=312, y=230)
        OptionMenu(self, self.scvar3, *seconds).place(x=378, y=230)

        self.cbvar = []
        self.cvar1 = IntVar(self)
        self.cvar2 = IntVar(self)
        self.cvar3 = IntVar(self)
        self.cvar4 = IntVar(self)
        self.cvar5 = IntVar(self)
        self.cvar6 = IntVar(self)
        self.cvar7 = IntVar(self)
        Checkbutton(self, text="Monday", variable=self.cvar1).place(x=40, y=280)
        Checkbutton(self, text="Tuesday", variable=self.cvar2).place(x=110, y=280)
        Checkbutton(self, text="Wednesday", variable=self.cvar3).place(x=180, y=280)
        Checkbutton(self, text="Thursday", variable=self.cvar4).place(x=270, y=280)
        Checkbutton(self, text="Friday", variable=self.cvar5).place(x=350, y=280)
        Checkbutton(self, text="Saturday", variable=self.cvar6).place(x=410, y=280)
        Checkbutton(self, text="Sunday", variable=self.cvar7).place(x=485, y=280)
        Canvas(self, width=572, height=1, bg="#bfbfbf").place(x=12, y=320)
        Button(self, text="Add", command=self.add).place(x=365, y=335)
        Button(self, text="Update", command=self.updat).place(x=400, y=335)
        Button(self, text="Delete", command=self.delete).place(x=451, y=335)
        Button(self, text="Load", command=self.load).place(x=498, y=335)

    def sel(self):
        self.rb = self.rbvar.get()

    def recurweeks(self):
        if self.cvar1.get() == 1:
            self.cbvar.append(weekdict[1])
        if self.cvar2.get() == 1:
            self.cbvar.append(weekdict[2])
        if self.cvar3.get() == 1:
            self.cbvar.append(weekdict[3])
        if self.cvar4.get() == 1:
            self.cbvar.append(weekdict[4])
        if self.cvar5.get() == 1:
            self.cbvar.append(weekdict[5])
        if self.cvar6.get() == 1:
            self.cbvar.append(weekdict[6])
        if self.cvar7.get() == 1:
            self.cbvar.append(weekdict[7])

    def wakeat(self):
        task = 'The job'
        sleep(self.gap)
        self.job(task)

    def job(self, task):
        errwin = Tk()
        errwin.title("Error")
        Label(errwin, text='Started Running '+task).pack()
        errwin.after(10000, lambda: errwin.destroy())
        errwin.mainloop()

    def add(self):
        try:
            task = self.entry.get()
            if task == '':
                raise Exception()
            if self.rb == 1:
                self.tasks.add('1:'+task+':'+self.hrvar0.get()+':'+self.mivar0.get()+':'+self.scvar0.get())
                dur = int(self.hrvar0.get())*60+int(self.mivar0.get())
                schedule.every(dur).minutes.do(self.job(task))
            elif self.rb == 2:
                self.tasks.add('2:'+task+':'+self.yvar.get()+':'+self.mvar.get()+':'+self.dvar.get()+':'+self.hrvar1.
                               get()+':'+self.mivar1.get()+':'+self.scvar1.get())
                self.gap = (dt.datetime(int(self.yvar.get()), int([x for x in range(1, 13) if monthdict[x] == self.mvar.
                            get()][0]), int(self.dvar.get()), int(self.hrvar1.get()), int(self.mivar1.get()), int(self.
                            scvar1.get()))-dt.datetime.now()).total_seconds()
                threading.Thread(target=self.wakeat).start()
            elif self.rb == 3:
                self.tasks.add('3:'+task+':'+self.rdayvar.get()+':'+self.hrvar2.get()+':'+self.mivar2.get()+':'+self.
                               scvar2.get())
                schedule.every(int(self.rdayvar.get())).days.at(self.hrvar2.get()+':'+self.mivar2.get()).do(self.job
                                                                                                            (task))
            elif self.rb == 4:
                self.recurweeks()
                strg = ':'.join(self.cbvar)
                tim = self.hrvar3.get()+':'+self.mivar3.get()
                self.tasks.add('4:'+task+':'+strg+':'+tim+':'+self.scvar3.get())
                for e in self.cbvar:
                    if e == weekdict[1]:
                        schedule.every().monday.at(tim).do(self.job(task))
                    elif e == weekdict[2]:
                        schedule.every().tueday.at(tim).do(self.job(task))
                    elif e == weekdict[3]:
                        schedule.every().wednesday.at(tim).do(self.job(task))
                    elif e == weekdict[4]:
                        schedule.every().thursday.at(tim).do(self.job(task))
                    elif e == weekdict[5]:
                        schedule.every().friday.at(tim).do(self.job(task))
                    elif e == weekdict[6]:
                        schedule.every().saturday.at(tim).do(self.job(task))
                    elif e == weekdict[7]:
                        schedule.every().sunday.at(tim).do(self.job(task))
        except (ValueError, Exception):
            self.delete()
            errwin = Tk()
            errwin.title("Error")
            Label(errwin, text='Invalid Input').pack()
            errwin.after(2000, lambda: errwin.destroy())
            errwin.mainloop()

    def delete(self):
        task = self.entry.get()
        for e in self.tasks:
            if task == e.split(':')[1]:
                self.tasks.discard(e)
                schedule.cancel_job(task)
                break

    def updat(self):
        task = self.entry.get()
        for e in self.tasks:
            if task in e:
                self.tasks.discard(e)
                schedule.cancel_job(task)
                self.add()
                break

    def load(self):
        root = Tk()
        root.title('Tasks')
        for e in self.tasks:
            arr = e.split(':')
            if arr[0] == '1':
                text = "'"+arr[1]+"'"+' occurs once in every '+arr[2]+' hr '+arr[3]+' min '+arr[4]+' sec '
            elif arr[0] == '2':
                text = "'"+arr[1]+"'"+' occurs once on '+arr[4]+' '+arr[3]+', '+arr[2]+' at '+arr[-3]+' hr ' \
                       + arr[-2] + ' min '+arr[-1]+' sec '
            elif arr[0] == '3':
                text = "'"+arr[1]+"'"+' occurs once in every '+arr[2]+' days at '+arr[3]+' hr '+arr[4]\
                       + ' min '+arr[5]+' sec '
            else:
                text = "'"+arr[1]+"'"+' occurs every week on '+','.join(arr[2:-3])+' at '+arr[-3]+' hr'\
                       + arr[-2]+' min '+arr[-1]+' sec '
            Label(root, text=text).pack(anchor=W)
        root.mainloop()

    def mainlp(self):
        Tk.mainloop(self)

app = MyApp()
app.mainlp()
