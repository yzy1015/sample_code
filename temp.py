from tkinter import *
from tkinter.colorchooser import askcolor


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.draw_button = Button(self.root, text='road', command=self.use_draw)
        self.draw_button.grid(row=0, column=0)

        self.intersection_button = Button(self.root, text='interaction', command=self.use_interaction)
        self.intersection_button.grid(row=0, column=1)

        self.rotation_button = Button(self.root, text='undo', command=self.undo)
        self.rotation_button.grid(row=0, column=2)

        self.clear_button = Button(self.root, text='clear', command=self.use_erase)
        self.clear_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)
        
        self.generate_button = Button(self.root, text='generate', command=self.use_generate)
        self.generate_button.grid(row=0, column=5)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan = 5)
        
        self.c2 = Canvas(self.root, bg='white', width=600, height=600)
        self.c2.grid(row=1, column=6)

        self.dummy = 1
        self.delete_queue = []
        
        self.stack_draw = []
        self.stack_op = []
        
        self.road_pos = []
        self.intersection_pos = []

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.intersection = False
        self.active_button = self.draw_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_draw(self):
        self.activate_button(self.draw_button)

    def use_interaction(self, width = 5):
        self.activate_button(self.intersection_button, intersection=True)

    def undo(self):
        if self.stack_op.pop():
            self.c.after(1, self.c.delete, self.stack_draw.pop())
            self.intersection_pos.pop()
        
        else:
            self.c.after(1, self.c.delete, self.stack_draw.pop())
            self.c.after(1, self.c.delete, self.stack_draw.pop())
            self.road_pos.pop()
            
        print('remove element')
        print(self.road_pos)
        print(self.intersection_pos)

    def use_generate(self):
        '''
            process self.road_pos, self.intersection_pos
        '''
        image1 = PhotoImage(file = "app_gui.gif")
        self.c2.create_image(0,0,anchor='nw',image=image1)
        self.c2.image = image1

    def use_erase(self):
        self.c.delete("all")
        self.c2.delete("all")


    def activate_button(self, some_button, intersection=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.intersection = intersection

    def draw_element(self,event, temp = True, width = 20):
        width = self.choose_size_button.get()*5
        self.line_width = 3
        paint_color = self.color
        if self.intersection==False:
            if self.old_x and self.old_y and self.dummy==0:
            
                canvas_id1 = self.c.create_line(self.old_x, self.old_y, 
                                            event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            
                canvas_id2 = self.c.create_line(self.old_x+width, self.old_y+width, 
                                            event.x+width, event.y+width,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            
                self.delete_queue.append(canvas_id1)
                self.delete_queue.append(canvas_id2)
            
            while len(self.delete_queue)>2:
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))
        else:
            id_rect = self.c.create_rectangle(event.x, event.y, 
                                            event.x+width, event.y+width, width=self.line_width)

            self.delete_queue.append(id_rect)
            while len(self.delete_queue)>1:
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))


    def paint(self, event):        
        if self.dummy == 1:
            self.old_x = event.x
            self.old_y = event.y
            self.dummy = 0
            
        self.draw_element(event)
        

    def reset(self, event): 
        self.draw_element(event, temp = False)
        self.stack_draw = self.stack_draw + self.delete_queue
        self.delete_queue = []
        if self.intersection==False:
            self.road_pos.append((self.old_x, self.old_y, event.x, event.y))
        else:
            self.intersection_pos.append((event.x, event.y))
        
        self.stack_op = self.stack_op + [self.intersection]
        
        print('add element')
        print(self.road_pos)
        print(self.intersection_pos)
        self.old_x, self.old_y = None, None
        self.dummy = 1

if __name__ == '__main__':
    ge = Paint()