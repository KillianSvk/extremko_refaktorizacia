import tkinter as tk
import tkinter.font as font
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import random
import json


class Clovece:
    def __init__(self, loaded=False, save=None):

        board_size = 800

        # Create board
        self.window = tk.Tk()
        self.window.title("Clovece")
        self.window.geometry(f"{board_size}x{board_size}")

        # Create variables
        self.button_font = font.Font(family='Helvetica', size=20, weight=font.BOLD)
        self.board_size = board_size
        self.player_count = 4
        self.dice_animation = True
        self.turn = 1
        self.roll = 6
        self.move = False
        self.mouse_hold = []
        self.grid = []
        self.main_area = []

        self.title_color = ["#00ff00",'#ffff00',"#4040e3","#ff0000"]
        self.g0 = []
        self.g1 = []
        self.g2 = []
        self.g3 = []

        self.player1_figures = []
        self.player2_figures = []
        self.player3_figures = []
        self.player4_figures = []
        self.all_figures = []

        self.player1_finish = []
        self.player2_finish = []
        self.player3_finish = []
        self.player4_finish = []
        self.borders = []
        self.player_colors = ["red","blue","green","yellow"]

        # Figure picture
        # Height 1/16
        # Width (3*(1/16))/5
        # Player 1
        self.player_1_img = tk.PhotoImage(file='red.png')
        # Player 2
        self.player_2_img = tk.PhotoImage(file='blue.png')
        # Player 3
        self.player_3_img = tk.PhotoImage(file='green.png')
        # Player 4
        self.player_4_img = tk.PhotoImage(file='yellow.png')
        

        # Figure position
        # Player 1
        self.figure1_1 = Figure(1, -1, 0)
        self.figure1_2 = Figure(1, -1, 0)
        self.figure1_3 = Figure(1, -1, 0)
        self.figure1_4 = Figure(1, -1, 0)
        # Player 2
        self.figure2_1 = Figure(2, -1, 0)
        self.figure2_2 = Figure(2, -1, 0)
        self.figure2_3 = Figure(2, -1, 0)
        self.figure2_4 = Figure(2, -1, 0)
        # Player 3
        self.figure3_1 = Figure(3, -1, 0)
        self.figure3_2 = Figure(3, -1, 0)
        self.figure3_3 = Figure(3, -1, 0)
        self.figure3_4 = Figure(3, -1, 0)
        # Player 4
        self.figure4_1 = Figure(4, -1, 0)
        self.figure4_2 = Figure(4, -1, 0)
        self.figure4_3 = Figure(4, -1, 0)
        self.figure4_4 = Figure(4, -1, 0)

        self.menu_board = tk.Canvas(self.window, width = self.board_size, height = self.board_size, bg="#d9c59e")
        self.menu_board.pack(fill=tk.BOTH, expand=True)

        self.create_menu()

        if loaded:
            self.save = save
            self.start_game()
            self.load_game()

        self.window.mainloop()

    def create_menu(self):
        # Create the main menu buttons
        play_button = tk.Button(self.menu_board, text="Play", font=("Helvetica", 32), bg="#00ff00", command=self.start_game, activebackground="#00ff00")
        play_button.place(x=(self.board_size//11)*1, y=(self.board_size//11)*5.5, anchor='center')

        settings_button = tk.Button(self.menu_board, text="Settings", font=("Helvetica", 32), bg="#ffff00", command=self.open_setting ,activebackground="#ffff00")
        settings_button.place(x=(self.board_size//11)*3.5, y=(self.board_size//11)*5.5, anchor='center')

        load_button = tk.Button(self.menu_board, text="Load Game", font=("Helvetica", 32), bg="#4040e3", command=self.load_refresh, activebackground="#4040e3")
        load_button.place(x=(self.board_size//11)*7, y=(self.board_size//11)*5.5, anchor='center')

        exit_button = tk.Button(self.menu_board, text="Exit", font=("Helvetica", 32), bg="#ff0000", command=self.exit_game, activebackground="#ff0000")
        exit_button.place(x=(self.board_size//11)*10, y=(self.board_size//11)*5.5, anchor='center')

        # Title Človeče nehnevaj sa
        self.g0.append( self.menu_board.create_text((self.board_size//11)*2, (self.board_size//11)*2.5, text='Č', font=("Helvetica", 100), anchor='center',fill=self.title_color[0]))
        self.g1.append( self.menu_board.create_text((self.board_size//11)*3.2, (self.board_size//11)*2.5, text='L', font=("Helvetica", 100), anchor='center', fill=self.title_color[1]))
        self.g2.append( self.menu_board.create_text((self.board_size//11)*4.4, (self.board_size//11)*2.5, text='O', font=("Helvetica", 100), anchor='center', fill=self.title_color[2]))
        self.g3.append( self.menu_board.create_text((self.board_size//11)*5.6, (self.board_size//11)*2.5, text='V', font=("Helvetica", 100), anchor='center', fill=self.title_color[3]))
        self.g0.append( self.menu_board.create_text((self.board_size//11)*6.8, (self.board_size//11)*2.5, text='E', font=("Helvetica", 100), anchor='center', fill=self.title_color[0]))
        self.g1.append( self.menu_board.create_text((self.board_size//11)*8, (self.board_size//11)*2.5, text='Č', font=("Helvetica", 100), anchor='center', fill=self.title_color[1]))
        self.g2.append( self.menu_board.create_text((self.board_size//11)*9.2, (self.board_size//11)*2.5, text='E', font=("Helvetica", 100), anchor='center', fill=self.title_color[2]))

        self.g3.append( self.menu_board.create_text((self.board_size//11), (self.board_size//11)*8.5, text='N', font=("Helvetica", 80), anchor='center',fill=self.title_color[3]))
        self.g0.append( self.menu_board.create_text((self.board_size//11)*2, (self.board_size//11)*8.5, text='E', font=("Helvetica", 80), anchor='center',fill=self.title_color[0]))
        self.g1.append( self.menu_board.create_text((self.board_size//11)*3, (self.board_size//11)*8.5, text='H', font=("Helvetica", 80), anchor='center',fill=self.title_color[1]))
        self.g2.append( self.menu_board.create_text((self.board_size//11)*4, (self.board_size//11)*8.5, text='N', font=("Helvetica", 80), anchor='center',fill=self.title_color[2]))
        self.g3.append( self.menu_board.create_text((self.board_size//11)*5, (self.board_size//11)*8.5, text='E', font=("Helvetica", 80), anchor='center',fill=self.title_color[3]))
        self.g0.append( self.menu_board.create_text((self.board_size//11)*6, (self.board_size//11)*8.5, text='V', font=("Helvetica", 80), anchor='center',fill=self.title_color[0]))
        self.g1.append( self.menu_board.create_text((self.board_size//11)*7, (self.board_size//11)*8.5, text='A', font=("Helvetica", 80), anchor='center',fill=self.title_color[1]))
        self.g2.append( self.menu_board.create_text((self.board_size//11)*8, (self.board_size//11)*8.5, text='J', font=("Helvetica", 80), anchor='center',fill=self.title_color[2]))

        self.g3.append( self.menu_board.create_text((self.board_size//11)*9.5, (self.board_size//11)*8.5, text='S', font=("Helvetica", 80), anchor='center',fill=self.title_color[3]))
        self.g0.append( self.menu_board.create_text((self.board_size//11)*10.5, (self.board_size//11)*8.5, text='A', font=("Helvetica", 80), anchor='center',fill=self.title_color[0]))

        self.window.bind("<Escape>",self.exit_game)

        self.title_animation_toggle = True
        self.title_animation()

    def title_animation(self,i=4):
        if self.title_animation_toggle:

            i = i%4

            for id in self.g0:
                self.menu_board.itemconfig(id, fill=self.title_color[((3+i%4))%4])

            for id in self.g1:
                self.menu_board.itemconfig(id, fill=self.title_color[((2+i)%4)%4])

            for id in self.g2:
                self.menu_board.itemconfig(id, fill=self.title_color[((1+i)%4)%4])

            for id in self.g3:
                self.menu_board.itemconfig(id, fill=self.title_color[i])

            i += 1
            self.menu_board.update()
            self.menu_board.after(800)
            self.title_animation(i)
            

    def open_setting(self):
        self.menu_board.destroy()
        self.title_animation_toggle = False

        self.settings_canvas = tk.Canvas(self.window, width = self.board_size, height = self.board_size + 200, bg="#d9c59e")
        self.settings_canvas.pack(fill=tk.BOTH, expand=True)

        # Player Buttons
        # Lablel
        players = tk.Label(self.settings_canvas, text= "Players:", bg="#d9c59e", font=("Helvetica", 32), anchor='center')
        players.place(x=(self.board_size//11)*0.5, y=(self.board_size//11)*1.25)

        # Buttons
        self.b_1 = tk.Button(self.settings_canvas, text= "1", bg="#d9c59e", font=("Helvetica", 32), anchor='center', width=3,borderwidth=3, relief="solid", background='#d9c59e', fg='black', command=self.choose_players_1)
        self.b_1.place(x=(self.board_size//11)*0.5 + (self.board_size//11)*2.5, y=(self.board_size//11))
        self.b_2 = tk.Button(self.settings_canvas, text= "2", bg="#d9c59e", font=("Helvetica", 32), anchor='center', width=3,borderwidth=3, relief="solid", background='#d9c59e' ,fg='black', command=self.choose_players_2)
        self.b_2.place(x=(self.board_size//11)*0.5 + (self.board_size//11)*4.5, y=(self.board_size//11))
        self.b_3 = tk.Button(self.settings_canvas, text= "3", bg="#d9c59e", font=("Helvetica", 32), anchor='center', width=3,borderwidth=3, relief="solid", background='#d9c59e', fg='black', command=self.choose_players_3)
        self.b_3.place(x=(self.board_size//11)*0.5 + (self.board_size//11)*6.5, y=(self.board_size//11))
        self.b_4 = tk.Button(self.settings_canvas, text= "4", bg="#d9c59e", font=("Helvetica", 32), anchor='center', width=3,borderwidth=3, relief="solid", background='#d9c59e', fg='black', command=self.choose_players_4)
        self.b_4.place(x=(self.board_size//11)*0.5 + (self.board_size//11)*8.5, y=(self.board_size//11))

        # Dice Animation
        # Lablel
        players = tk.Label(self.settings_canvas, text= "Dice Animation:", bg="#d9c59e", font=("Helvetica", 32), anchor='center')
        players.place(x=(self.board_size//11)*0.5, y=(self.board_size//11)*3)

        # Buttons
        self.dice_on = tk.Button(self.settings_canvas, text= "ON", bg="#d9c59e", font=("Helvetica", 32), anchor='center', width=3,borderwidth=3, relief="solid", background='#d9c59e', fg='black', command=self.animation_on)
        self.dice_on.place(x=(self.board_size//11)*0.5 + (self.board_size//11)*5, y=(self.board_size//11)*3)
        self.dice_off = tk.Button(self.settings_canvas, text= "OFF", bg="#d9c59e", font=("Helvetica", 32), anchor='center', width=3,borderwidth=3, relief="solid", background='#d9c59e' ,fg='black', command=self.animation_off)
        self.dice_off.place(x=(self.board_size//11)*0.5 + (self.board_size//11)*7, y=(self.board_size//11)*3)

        # Set Right Colors
        self.choose_players(self.player_count)
        self.dice_animation_toggle(self.dice_animation)

        # Back to Menu
        menu = tk.Button(self.settings_canvas, text="Back To Menu", font=("Helvetica", 32), bg="red", command=self.back_to_menu_setting, activebackground="red", anchor='center')
        menu.place(x=(self.board_size//11)*3.3, y=(self.board_size/11)*9)

    def animation_on(self):
        self.dice_animation_toggle(True)
    def animation_off(self):
        self.dice_animation_toggle(False)

    def dice_animation_toggle(self, value):
        se_fg = "red"
        se_bg = "grey"
        base_fg = "black"
        base_bg = "#d9c59e"
        self.dice_animation = value

        if value:
            # Selected
            self.dice_on["fg"] = se_fg
            self.dice_on["background"] = se_bg
            # Reset
            self.dice_off["fg"] = base_fg
            self.dice_off["background"] = base_bg

        else:
            # Selected
            self.dice_off["fg"] = se_fg
            self.dice_off["background"] = se_bg
            # Reset
            self.dice_on["fg"] = base_fg
            self.dice_on["background"] = base_bg


    def choose_players_1(self):
        self.choose_players(1)
    def choose_players_2(self):
        self.choose_players(2)
    def choose_players_3(self):
        self.choose_players(3)
    def choose_players_4(self):
        self.choose_players(4)

    def choose_players(self, num):
        se_fg = "red"
        se_bg = "grey"
        base_fg = "black"
        base_bg = "#d9c59e"
        if num == 1:
            # Selected
            self.b_1["fg"] = se_fg
            self.b_1["background"] = se_bg
            self.player_count = 1
            # Reset
            self.b_2["fg"] = base_fg
            self.b_2["background"] = base_bg
            self.b_3["fg"] = base_fg
            self.b_3["background"] = base_bg
            self.b_4["fg"] = base_fg
            self.b_4["background"] = base_bg

        if num == 2:
            # Selected
            self.b_2["fg"] = se_fg
            self.b_2["background"] = se_bg
            self.player_count = 2
            # Reset
            self.b_1["fg"] = base_fg
            self.b_1["background"] = base_bg
            self.b_3["fg"] = base_fg
            self.b_3["background"] = base_bg
            self.b_4["fg"] = base_fg
            self.b_4["background"] = base_bg

        if num == 3:
            # Selected
            self.b_3["fg"] = se_fg
            self.b_3["background"] = se_bg
            self.player_count = 3
            # Reset
            self.b_1["fg"] = base_fg
            self.b_1["background"] = base_bg
            self.b_2["fg"] = base_fg
            self.b_2["background"] = base_bg
            self.b_4["fg"] = base_fg
            self.b_4["background"] = base_bg
        if num == 4:
            # Selected
            self.b_4["fg"] = se_fg
            self.b_4["background"] = se_bg
            self.player_count = 4
            # Reset
            self.b_1["fg"] = base_fg
            self.b_1["background"] = base_bg
            self.b_2["fg"] = base_fg
            self.b_2["background"] = base_bg
            self.b_3["fg"] = base_fg
            self.b_3["background"] = base_bg

    def start_game(self):
        self.board = tk.Canvas(self.window, width = self.board_size, height = self.board_size + 200, bg="#d9c59e")
        self.board.pack(expand=True)

        self.title_animation_toggle = False
        self.menu_board.destroy()

        self.window.geometry(f"{self.board_size + 50}x{self.board_size + 250}")

        # Menu
        # Create Menu
        self.menu_bar = tk.Menu(self.window)
        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_game)
        file_menu.add_command(label="Load", command=self.load_refresh)
        file_menu.add_separator()
        file_menu.add_command(label="Menu", command= self.back_to_menu_game)
        file_menu.add_command(label="Exit", command= self.exit_game)
        self.menu_bar.add_cascade(label="File", menu= file_menu)
        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.help)
        help_menu.add_command(label="About...", command=self.about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.window.config(menu=self.menu_bar)

        # Create playing board
        self.board_setup()

        # Mouse/Keyboard input
        self.board.bind('<Button-1>',self.mouse_click)
        self.board.bind('<B1-Motion>',self.mouse_drag)
        self.board.bind('<ButtonRelease-1>',self.mouse_release)
        self.window.bind('<space>', self.space_action)

    def board_setup(self):

        # Create grid from left to right
        for j in range(2, self.board_size - self.board_size // 11, self.board_size // 11):
            for i in range(2, self.board_size - self.board_size // 11, self.board_size // 11):
                self.grid.append((i, j, i + self.board_size // 11, j + self.board_size // 11))

        # Create whole grid for testing
        # for i in self.grid:
        #     self.board.create_oval(*i,fill="white")

        # Create Player 1
        self.board.create_oval(self.grid[0], fill=self.player_colors[0], width="3")
        self.board.create_oval(self.grid[1], fill=self.player_colors[0], width="3")
        self.board.create_oval(self.grid[11], fill=self.player_colors[0], width="3")
        self.board.create_oval(self.grid[12], fill=self.player_colors[0], width="3")

        # Create Player 2
        self.board.create_oval(self.grid[9], fill=self.player_colors[1], width="3")
        self.board.create_oval(self.grid[10], fill=self.player_colors[1], width="3")
        self.board.create_oval(self.grid[20], fill=self.player_colors[1], width="3")
        self.board.create_oval(self.grid[21], fill=self.player_colors[1], width="3")

        # Create Player 3
        self.board.create_oval(self.grid[108], fill=self.player_colors[2], width="3")
        self.board.create_oval(self.grid[109], fill=self.player_colors[2], width="3")
        self.board.create_oval(self.grid[119], fill=self.player_colors[2], width="3")
        self.board.create_oval(self.grid[120], fill=self.player_colors[2], width="3")

        # Create Player 4
        self.board.create_oval(self.grid[99], fill=self.player_colors[3], width="3")
        self.board.create_oval(self.grid[100], fill=self.player_colors[3], width="3")
        self.board.create_oval(self.grid[110], fill=self.player_colors[3], width="3")
        self.board.create_oval(self.grid[111], fill=self.player_colors[3], width="3")


        # Create main playing area

        # Create Player 1 side
        self.main_area.append(self.grid[44]) # Player 1 Start

        for i in range(45,48 + 1):
            self.main_area.append(self.grid[i])
        for i in reversed(range(4,37 + 1, 11)):
            self.main_area.append(self.grid[i])
        self.main_area.append(self.grid[5])
        # Player 1 finish line
        for i in range(4):
            self.player1_finish.append(self.grid[56 + i])
            self.board.create_oval(self.grid[56 + i], fill=self.player_colors[0], width="0")

        # Create Player 2 side
        self.main_area.append(self.grid[6]) # Player 2 Start

        for i in range(17,40 + 1, 11):
            self.main_area.append(self.grid[i])
        for i in range(50,54 + 1):
            self.main_area.append(self.grid[i])
        self.main_area.append(self.grid[65])
        # Player 2 finish line
        for i in range(0,44,11):
            self.player2_finish.append(self.grid[16+i])
            self.board.create_oval(self.grid[16+i],fill=self.player_colors[1], width="0")

        # Create Player 3 side
        self.main_area.append(self.grid[76]) # Player 3 Start
        for i in range(75,72 - 1, -1):
            self.main_area.append(self.grid[i])
        for i in range(83,116 + 1 ,11):
            self.main_area.append(self.grid[i])
        self.main_area.append(self.grid[115])
        # Player 3 finish line
        for i in range(0,-4,-1):
            self.player3_finish.append(self.grid[64 + i])
            self.board.create_oval(self.grid[64 + i], fill=self.player_colors[2], width="0")

        # Create Player 4 side
        self.main_area.append(self.grid[114]) # Player 4 Start
        for i in range(103,70 - 1, -11):
            self.main_area.append(self.grid[i])
        for i in range(69,66 - 1 , -1):
            self.main_area.append(self.grid[i])
        self.main_area.append(self.grid[55])
        # Player 4 finish line
        for i in range(0,-44,-11):
            self.player4_finish.append(self.grid[16-i])
            self.board.create_oval(self.grid[104+i],fill=self.player_colors[3], width="0")
        
        

        for i in self.main_area:
            if i == self.grid[44]:
                self.board.create_oval(i,fill=self.player_colors[0], width="3")
                self.board
            elif i == self.grid[6]:
                self.board.create_oval(i,fill=self.player_colors[1], width="3")
            elif i == self.grid[76]:
                self.board.create_oval(i,fill=self.player_colors[2], width="3")
            elif i == self.grid[114]:
                self.board.create_oval(i,fill=self.player_colors[3], width="3")
            else:
                self.board.create_oval(i,fill="white", width="3")


        # Placing pieces

        # Player 1 figuers
        self.figure1_1.id = self.board.create_image((self.grid[0][0] + self.grid[0][2])/2,(self.grid[0][1] + self.grid[0][3])/2,image=self.player_1_img, tags='p1')
        self.figure1_2.id = self.board.create_image((self.grid[1][0] + self.grid[1][2])/2,(self.grid[1][1] + self.grid[1][3])/2,image=self.player_1_img, tags='p1')
        self.figure1_3.id = self.board.create_image((self.grid[11][0] + self.grid[11][2])/2,(self.grid[11][1] + self.grid[11][3])/2,image=self.player_1_img, tags='p1')
        self.figure1_4.id = self.board.create_image((self.grid[12][0] + self.grid[12][2])/2,(self.grid[12][1] + self.grid[12][3])/2,image=self.player_1_img, tags='p1')

        self.figure1_1.home = ((self.grid[0][0] + self.grid[0][2])/2,(self.grid[0][1] + self.grid[0][3])/2)
        self.figure1_2.home = ((self.grid[1][0] + self.grid[1][2])/2,(self.grid[1][1] + self.grid[1][3])/2)
        self.figure1_3.home = ((self.grid[11][0] + self.grid[11][2])/2,(self.grid[11][1] + self.grid[11][3])/2)
        self.figure1_4.home = ((self.grid[12][0] + self.grid[12][2])/2,(self.grid[12][1] + self.grid[12][3])/2) 
       
        # Player 2 figuers
        self.figure2_1.id = self.board.create_image((self.grid[9][0] + self.grid[9][2])/2,(self.grid[9][1] + self.grid[9][3])/2,image=self.player_2_img, tags='p2')
        self.figure2_2.id = self.board.create_image((self.grid[10][0] + self.grid[10][2])/2,(self.grid[10][1] + self.grid[10][3])/2,image=self.player_2_img, tags='p2')
        self.figure2_3.id = self.board.create_image((self.grid[20][0] + self.grid[20][2])/2,(self.grid[20][1] + self.grid[20][3])/2,image=self.player_2_img, tags='p2')
        self.figure2_4.id = self.board.create_image((self.grid[21][0] + self.grid[21][2])/2,(self.grid[21][1] + self.grid[21][3])/2,image=self.player_2_img, tags='p2')

        self.figure2_1.home = ((self.grid[9][0] + self.grid[9][2])/2,(self.grid[9][1] + self.grid[9][3])/2)
        self.figure2_2.home = ((self.grid[10][0] + self.grid[10][2])/2,(self.grid[10][1] + self.grid[10][3])/2)
        self.figure2_3.home = ((self.grid[20][0] + self.grid[20][2])/2,(self.grid[20][1] + self.grid[20][3])/2)
        self.figure2_4.home = ((self.grid[21][0] + self.grid[21][2])/2,(self.grid[21][1] + self.grid[21][3])/2)

        # Player 3 figuers
        self.figure3_1.id = self.board.create_image((self.grid[108][0] + self.grid[108][2])/2,(self.grid[108][1] + self.grid[108][3])/2,image=self.player_3_img, tags='p3')
        self.figure3_2.id = self.board.create_image((self.grid[109][0] + self.grid[109][2])/2,(self.grid[109][1] + self.grid[109][3])/2,image=self.player_3_img, tags='p3')
        self.figure3_3.id = self.board.create_image((self.grid[119][0] + self.grid[119][2])/2,(self.grid[119][1] + self.grid[119][3])/2,image=self.player_3_img, tags='p3')
        self.figure3_4.id = self.board.create_image((self.grid[120][0] + self.grid[120][2])/2,(self.grid[120][1] + self.grid[120][3])/2,image=self.player_3_img, tags='p3')

        self.figure3_1.home = ((self.grid[108][0] + self.grid[108][2])/2,(self.grid[108][1] + self.grid[108][3])/2)
        self.figure3_2.home = ((self.grid[109][0] + self.grid[109][2])/2,(self.grid[109][1] + self.grid[109][3])/2)
        self.figure3_3.home = ((self.grid[119][0] + self.grid[119][2])/2,(self.grid[119][1] + self.grid[119][3])/2)
        self.figure3_4.home = ((self.grid[120][0] + self.grid[120][2])/2,(self.grid[120][1] + self.grid[120][3])/2)

        # Player 4 figuers
        self.figure4_1.id = self.board.create_image((self.grid[99][0] + self.grid[99][2])/2,(self.grid[99][1] + self.grid[99][3])/2,image=self.player_4_img, tags='p4')
        self.figure4_2.id = self.board.create_image((self.grid[100][0] + self.grid[100][2])/2,(self.grid[100][1] + self.grid[100][3])/2,image=self.player_4_img, tags='p4')
        self.figure4_3.id = self.board.create_image((self.grid[110][0] + self.grid[110][2])/2,(self.grid[110][1] + self.grid[110][3])/2,image=self.player_4_img, tags='p4')
        self.figure4_4.id = self.board.create_image((self.grid[111][0] + self.grid[111][2])/2,(self.grid[111][1] + self.grid[111][3])/2,image=self.player_4_img, tags='p4')

        self.figure4_1.home = ((self.grid[99][0] + self.grid[99][2])/2,(self.grid[99][1] + self.grid[99][3])/2)
        self.figure4_2.home = ((self.grid[100][0] + self.grid[100][2])/2,(self.grid[100][1] + self.grid[100][3])/2)
        self.figure4_3.home = ((self.grid[110][0] + self.grid[110][2])/2,(self.grid[110][1] + self.grid[110][3])/2)
        self.figure4_4.home = ((self.grid[111][0] + self.grid[111][2])/2,(self.grid[111][1] + self.grid[111][3])/2)


        # Add figures to list
        self.player1_figures.append(self.board.find_withtag('p1'))
        self.player2_figures.append(self.board.find_withtag('p2'))
        self.player3_figures.append(self.board.find_withtag('p3'))
        self.player4_figures.append(self.board.find_withtag('p4'))
        self.all_figures.append(self.player1_figures)
        self.all_figures.append(self.player2_figures)
        self.all_figures.append(self.player3_figures)
        self.all_figures.append(self.player4_figures)
        self.all_figures = self.all_figures[0] + self.all_figures[1] + self.all_figures[2] + self.all_figures[3]

        # Bottom of a playing board

        # Borders
        self.board.create_line(0, self.board_size, self.board_size + self.board_size//11, self.board_size, width="6", fill=self.player_colors[self.turn-1], tags="border")
        self.board.create_line(5, self.board_size, 5, self.board_size + 200, width="6", fill=self.player_colors[self.turn-1], tags="border")
        self.board.create_line(self.board_size, self.board_size, self.board_size, self.board_size + 200, width="6", fill=self.player_colors[self.turn-1], tags="border")
        self.board.create_line(0, self.board_size + 200, self.board_size + self.board_size//11, self.board_size + 200, width="6", fill=self.player_colors[self.turn-1], tags="border")

        self.borders.append(self.board.find_withtag("border"))

        # Dice button
        dice = tk.Button(self.board, text="Roll Dice", command=self.dice_roll)
        dice['font'] = self.button_font
        dice.place(x=self.board_size//11 , y=self.board_size + (self.board_size//11)/2)

        # Dice
        self.dice_img = tk.PhotoImage(file=f'dice/dice_{self.roll}.png')
        self.dice = self.board.create_image((self.board_size//11)*8, self.board_size + (self.board_size//11)*1.5, image = self.dice_img, anchor='center')

        # Skip button
        sikp = tk.Button(self.board, text="Skip Turn", command=self.next_turn)
        sikp['font'] = self.button_font
        sikp.place(x=self.board_size//11 , y=self.board_size + 1.5*self.board_size//11 )

        # WIN button
        dice = tk.Button(self.board, text="WIN", command=self.check_win)
        dice['font'] = self.button_font
        dice.place(x=self.board_size//11 + (self.board_size//11) * 2, y=self.board_size + self.board_size//11)
        

    def dice_roll(self,event=None):
        if self.move == False:

            if self.dice_animation:
                delay = 50
                # Animation for Dice
                for i in range(14):
                    roll = random.randint(1,6)
                    #self.dice_img = f'dice/dice_{roll}.png'
                    dice_img = tk.PhotoImage(file=f'dice/dice_{roll}.png')
                    self.board.itemconfig(self.dice, image=dice_img)
                    self.board.update()
                    self.board.after(delay + i*20)

                # Actual roll
                self.roll = roll
                # Change IMG
                self.dice_img = dice_img
                self.board.update()

            else:
                roll = random.randint(1,6)
                self.roll = roll
                self.dice_img = tk.PhotoImage(file=f'dice/dice_{roll}.png')
                self.board.itemconfig(self.dice, image=self.dice_img)
                self.board.update()

            #print(f'{self.roll}')
            self.move = True

            if roll == 6:
                self.pop_from_home()
        
    def next_turn(self):
        self.turn += 1
        if self.turn == self.player_count + 1:
            self.turn = 1
        self.move = False

        # Next player turn (visual border indicator)
        for id in self.borders[0]:
            self.board.itemconfig(id, fill=self.player_colors[self.turn-1] )

    def pop_from_home(self):
        figure = None
        # Player 1 check
        if self.all_figures[self.turn - 1] == self.player1_figures[0]:
            for id in self.player1_figures[0]:
                if id == self.figure1_1.id:
                    if self.figure1_1.pos == -1:
                        figure = self.figure1_1
                        break
                if id == self.figure1_2.id:
                    if self.figure1_2.pos == -1:
                        figure = self.figure1_2
                        break
                if id == self.figure1_3.id:
                    if self.figure1_3.pos == -1:
                        figure = self.figure1_3
                        break
                if id == self.figure1_4.id:
                    if self.figure1_4.pos == -1:
                        figure = self.figure1_4
                        break

        # Player 2 check
        if self.all_figures[self.turn - 1] == self.player2_figures[0]:
            for id in self.player2_figures[0]:
                if id == self.figure2_1.id:
                    if self.figure2_1.pos == -1:
                        figure = self.figure2_1
                        break
                if id == self.figure2_2.id:
                    if self.figure2_2.pos == -1:
                        figure = self.figure2_2
                        break
                if id == self.figure2_3.id:
                    if self.figure2_3.pos == -1:
                        figure = self.figure2_3
                        break
                if id == self.figure2_4.id:
                    if self.figure2_4.pos == -1:
                        figure = self.figure2_4
                        break
        # Player 3 check
        if self.all_figures[self.turn - 1] == self.player3_figures[0]:
            for id in self.player3_figures[0]:
                if id == self.figure3_1.id:
                    if self.figure1_3.pos == -1:
                        figure = self.figure3_1
                        break
                if id == self.figure3_2.id:
                    if self.figure3_2.pos == -1:
                        figure = self.figure3_2
                        break
                if id == self.figure3_3.id:
                    if self.figure3_3.pos == -1:
                        figure = self.figure3_3
                        break
                if id == self.figure3_4.id:
                    if self.figure3_4.pos == -1:
                        figure = self.figure3_4
                        break
        # Player 4 check
        if self.all_figures[self.turn - 1] == self.player4_figures[0]:
            for id in self.player4_figures[0]:
                if id == self.figure4_1.id:
                    if self.figure4_1.pos == -1:
                        figure = self.figure4_1
                        break
                if id == self.figure4_2.id:
                    if self.figure4_2.pos == -1:
                        figure = self.figure4_2
                        break
                if id == self.figure4_3.id:
                    if self.figure4_3.pos == -1:
                        figure = self.figure4_3
                        break
                if id == self.figure4_4.id:
                    if self.figure4_4.pos == -1:
                        figure = self.figure4_4
                        break

        if figure:
            # Correct position
            pos = 0
            if figure.player == 2:
                pos += 10
            if figure.player == 3:
                pos += 20
            if figure.player == 4:
                pos += 30
            # Move to a starting position
            self.board.coords(figure.id, (self.main_area[pos][0] + self.main_area[pos][2])/2, (self.main_area[pos][1] + self.main_area[pos][3])/2)
            figure.moved = 1
            figure.pos = pos # Update figure position
            self.kick(figure)
            self.move = False
               

    def pop_figure(self,event):
        item = self.mouse_hold[0] # My Figure

        # Player 1 figure select
        if item in self.player1_figures[0]:
            if item == self.figure1_1.id:
                figure = self.figure1_1
            if item == self.figure1_2.id:
                figure = self.figure1_2
            if item == self.figure1_3.id:
                figure = self.figure1_3
            if item == self.figure1_4.id:
                figure = self.figure1_4
        # Player 2 figure select
        if item in self.player2_figures[0]:
            if item == self.figure2_1.id:
                figure = self.figure2_1
            if item == self.figure2_2.id:
                figure = self.figure2_2
            if item == self.figure2_3.id:
                figure = self.figure2_3
            if item == self.figure2_4.id:
                figure = self.figure2_4
        # Player 3 figure select
        if item in self.player3_figures[0]:
            if item == self.figure3_1.id:
                figure = self.figure3_1
            if item == self.figure3_2.id:
                figure = self.figure3_2
            if item == self.figure3_3.id:
                figure = self.figure3_3
            if item == self.figure3_4.id:
                figure = self.figure3_4
        # Player 4 figure select
        if item in self.player4_figures[0]:
            if item == self.figure4_1.id:
                figure = self.figure4_1
            if item == self.figure4_2.id:
                figure = self.figure4_2
            if item == self.figure4_3.id:
                figure = self.figure4_3
            if item == self.figure4_4.id:
                figure = self.figure4_4
        
        if self.move == True and int(figure.pos) != -1: # Time for moving a figure

                # Position
                pos = int(figure.pos) + self.roll
                if pos >= 40:
                    pos -= 40 

                if int(figure.moved) + self.roll > 40:
                    pos = int(figure.moved) + self.roll - 40 - 1

                    # Player 1
                    if figure.id in self.player1_figures[0]:
                        try:
                            if self.empty_finish(figure):
                                if self.player1_finish[pos][0] <= event.x <= self.player1_finish[pos][2] and self.player1_finish[pos][1] <= event.y <= self.player1_finish[pos][3]:
                                    self.board.coords(figure.id, (self.player1_finish[pos][0] + self.player1_finish[pos][2])/2, (self.player1_finish[pos][1] + self.player1_finish[pos][3])/2)
                                    figure.moved = int(figure.moved) + self.roll # Update total moved positions
                                    figure.finished = True
                                    # figure.pos = pos # Update figure position
                                    self.check_win()
                                    if self.roll != 6:
                                        self.next_turn()

                                else:
                                    self.send_back(figure)
                            else:
                                self.send_back(figure)
                        except IndexError: # Going too far, go back
                            if figure.moved > 40:
                                self.board.coords(figure.id, (self.player1_finish[pos - self.roll][0] + self.player1_finish[pos - self.roll][2])/2, (self.player1_finish[pos - self.roll][1] + self.player1_finish[pos - self.roll][3])/2)
                            else:
                                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)
                            pass

                    # Player 2
                    if figure.id in self.player2_figures[0]:
                        try:
                            if self.empty_finish(figure):
                                if self.player2_finish[pos][0] <= event.x <= self.player2_finish[pos][2] and self.player2_finish[pos][1] <= event.y <= self.player2_finish[pos][3]:
                                    self.board.coords(figure.id, (self.player2_finish[pos][0] + self.player2_finish[pos][2])/2, (self.player2_finish[pos][1] + self.player2_finish[pos][3])/2)
                                    figure.moved = int(figure.moved) + self.roll # Update total moved positions
                                    figure.finished = True
                                    # figure.pos = pos # Update figure position
                                    self.check_win()
                                    if self.roll != 6:
                                        self.next_turn()

                                else:
                                    self.send_back(figure)
                            else:
                                self.send_back(figure)
                        except IndexError: # Going too far, go back
                            if figure.moved > 40:
                                self.board.coords(figure.id, (self.player2_finish[pos - self.roll][0] + self.player2_finish[pos - self.roll][2])/2, (self.player2_finish[pos - self.roll][1] + self.player2_finish[pos - self.roll][3])/2)
                            else:
                                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)
                            pass

                    # Player 3
                    if figure.id in self.player3_figures[0]:
                        try:
                            if self.empty_finish(figure):
                                if self.player3_finish[pos][0] <= event.x <= self.player3_finish[pos][2] and self.player3_finish[pos][1] <= event.y <= self.player3_finish[pos][3]:
                                    self.board.coords(figure.id, (self.player3_finish[pos][0] + self.player3_finish[pos][2])/2, (self.player3_finish[pos][1] + self.player3_finish[pos][3])/2)
                                    figure.moved = int(figure.moved) + self.roll # Update total moved positions
                                    figure.finished = True
                                    # figure.pos = pos # Update figure position
                                    self.check_win()
                                    if self.roll != 6:
                                        self.next_turn()

                                else:
                                    self.send_back(figure)
                            else:
                                self.send_back(figure)
                        except IndexError: # Going too far, go back
                            if figure.moved > 40:
                                self.board.coords(figure.id, (self.player3_finish[pos - self.roll][0] + self.player3_finish[pos - self.roll][2])/2, (self.player3_finish[pos - self.roll][1] + self.player3_finish[pos - self.roll][3])/2)
                            else:
                                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)
                            pass

                    # Player 4
                    if figure.id in self.player4_figures[0]:
                        try:
                            if self.empty_finish(figure):
                                if self.player4_finish[pos][0] <= event.x <= self.player4_finish[pos][2] and self.player4_finish[pos][1] <= event.y <= self.player4_finish[pos][3]:
                                    self.board.coords(figure.id, (self.player4_finish[pos][0] + self.player4_finish[pos][2])/2, (self.player4_finish[pos][1] + self.player4_finish[pos][3])/2)
                                    figure.moved = int(figure.moved) + self.roll # Update total moved positions
                                    figure.finished = True
                                    # figure.pos = pos # Update figure position
                                    self.check_win()
                                    if self.roll != 6:
                                        self.next_turn()

                                else:
                                    self.send_back(figure)
                            else:
                                self.send_back(figure)
                        except IndexError: # Going too far, go back
                            if figure.moved > 40:
                                self.board.coords(figure.id, (self.player4_finish[pos - self.roll][0] + self.player4_finish[pos - self.roll][2])/2, (self.player4_finish[pos - self.roll][1] + self.player4_finish[pos - self.roll][3])/2)
                            else:
                                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)
                            pass

                else:
                    if self.main_area[pos][0] <= event.x <= self.main_area[pos][2] and self.main_area[pos][1] <= event.y <= self.main_area[pos][3]:
                        self.board.coords(figure.id, (self.main_area[pos][0] + self.main_area[pos][2])/2, (self.main_area[pos][1] + self.main_area[pos][3])/2)
                        figure.moved = int(figure.moved) + self.roll # Update total moved positions
                        figure.pos = pos # Update figure position
                        if figure.pos >= 40:
                            figure.pos = int(figure.pos) - 40
                        self.kick(figure)
                        if self.roll != 6:
                            self.next_turn()

                    else: # Figure will go back were it was
                        self.send_back(figure)

        else: # Figure will go back were it was
            self.send_back(figure)


    def send_back(self, figure):
        if int(figure.moved) > 40:
            if figure.player == 1:
                self.board.coords(figure.id, (self.player1_finish[figure.moved - 40][0] + self.player1_finish[figure.moved - 40][2])/2, (self.player1_finish[figure.moved - 40][1] + self.player1_finish[figure.moved - 40][3])/2)
            if figure.player == 2:
                self.board.coords(figure.id, (self.player2_finish[figure.moved - 40][0] + self.player2_finish[figure.moved - 40][2])/2, (self.player2_finish[figure.moved - 40][1] + self.player2_finish[figure.moved - 40][3])/2)
            if figure.player == 3:
                self.board.coords(figure.id, (self.player3_finish[figure.moved - 41][0] + self.player3_finish[figure.moved - 41][2])/2, (self.player3_finish[figure.moved - 41][1] + self.player3_finish[figure.moved - 41][3])/2)
            if figure.player == 4:
                self.board.coords(figure.id, (self.player4_finish[figure.moved - 40][0] + self.player4_finish[figure.moved - 40][2])/2, (self.player4_finish[figure.moved - 40][1] + self.player4_finish[figure.moved - 40][3])/2)
        else:
            if figure.pos >= 0:
                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)
            else:
                self.board.coords(figure.id, *figure.home)

    def empty_finish(self, figure):
        # Player 1 check
        if self.mouse_hold[0] in self.player1_figures[0]:    
            if ((self.figure1_1.moved == figure.moved + self.roll and self.figure1_1.id != self.mouse_hold[0])
            or (self.figure1_2.moved == figure.moved + self.roll and self.figure1_2.id != self.mouse_hold[0])
            or (self.figure1_3.moved == figure.moved + self.roll and self.figure1_3.id != self.mouse_hold[0])
            or (self.figure1_4.moved == figure.moved + self.roll and self.figure1_4.id != self.mouse_hold[0])):
                return False
            else:
                return True

        # Player 2
        if self.mouse_hold[0] in self.player2_figures[0]:
            if ((self.figure2_1.moved == figure.moved + self.roll and self.figure2_1.id != self.mouse_hold[0])
            or (self.figure2_2.moved == figure.moved + self.roll and self.figure2_2.id != self.mouse_hold[0])
            or (self.figure2_3.moved == figure.moved + self.roll and self.figure2_3.id != self.mouse_hold[0])
            or (self.figure2_4.moved == figure.moved + self.roll and self.figure2_4.id != self.mouse_hold[0])):
                return False
            else:
                return True

        # Player 3
        if self.mouse_hold[0] in self.player3_figures[0]:
            if ((self.figure3_1.moved == figure.moved + self.roll and self.figure3_1.id != self.mouse_hold[0])
            or (self.figure3_2.moved == figure.moved + self.roll and self.figure3_2.id != self.mouse_hold[0])
            or (self.figure3_3.moved == figure.moved + self.roll and self.figure3_3.id != self.mouse_hold[0])
            or (self.figure3_4.moved == figure.moved + self.roll and self.figure3_4.id != self.mouse_hold[0])):
                return False
            else:
                return True

        # Player 4
        if self.mouse_hold[0] in self.player4_figures[0]:
            if ((self.figure4_1.moved == figure.moved + self.roll and self.figure4_1.id != self.mouse_hold[0])
            or (self.figure4_2.moved == figure.moved + self.roll and self.figure4_2.id != self.mouse_hold[0])
            or (self.figure4_3.moved == figure.moved + self.roll and self.figure4_3.id != self.mouse_hold[0])
            or (self.figure4_4.moved == figure.moved + self.roll and self.figure4_4.id != self.mouse_hold[0])):
                return False
            else:
                return True

    def kick(self,figure):
        # Player 1 check  
        if self.figure1_1.pos == figure.pos and self.figure1_1.id != figure.id and self.figure1_1.finished == False:
            self.board.coords(self.figure1_1.id, *self.figure1_1.home)
            self.figure1_1.pos = -1
            self.figure1_1.moved = 0
        if self.figure1_2.pos == figure.pos and self.figure1_2.id != figure.id and self.figure1_2.finished == False:
            self.board.coords(self.figure1_2.id, *self.figure1_2.home)
            self.figure1_2.pos = -1
            self.figure1_2.moved = 0
        if self.figure1_3.pos == figure.pos and self.figure1_3.id != figure.id and self.figure1_3.finished == False:
            self.board.coords(self.figure1_3.id, *self.figure1_3.home)
            self.figure1_3.pos = -1
            self.figure1_3.moved = 0
        if self.figure1_4.pos == figure.pos and self.figure1_4.id != figure.id and self.figure1_4.finished == False:
            self.board.coords(self.figure1_4.id, *self.figure1_4.home)
            self.figure1_4.pos = -1
            self.figure1_4.moved = 0

        # Player 2 check  
        if self.figure2_1.pos == figure.pos and self.figure2_1.id != figure.id and self.figure2_1.finished == False:
            self.board.coords(self.figure2_1.id, *self.figure2_1.home)
            self.figure2_1.pos = -1
            self.figure2_1.moved = 0
        if self.figure2_2.pos == figure.pos and self.figure2_2.id != figure.id and self.figure2_2.finished == False:
            self.board.coords(self.figure2_2.id, *self.figure2_2.home)
            self.figure2_2.pos = -1
            self.figure2_2.moved = 0
        if self.figure2_3.pos == figure.pos and self.figure2_3.id != figure.id and self.figure2_3.finished == False:
            self.board.coords(self.figure2_3.id, *self.figure2_3.home)
            self.figure2_3.pos = -1
            self.figure2_3.moved = 0
        if self.figure2_4.pos == figure.pos and self.figure2_4.id != figure.id and self.figure2_4.finished == False:
            self.board.coords(self.figure2_4.id, *self.figure2_4.home)
            self.figure2_4.pos = -1
            self.figure2_4.moved = 0

        # Player 3 check  
        if self.figure3_1.pos == figure.pos and self.figure3_1.id != figure.id and self.figure3_1.finished == False:
            self.board.coords(self.figure3_1.id, *self.figure3_1.home)
            self.figure3_1.pos = -1
            self.figure3_1.moved = 0
        if self.figure3_2.pos == figure.pos and self.figure3_2.id != figure.id and self.figure3_2.finished == False:
            self.board.coords(self.figure3_2.id, *self.figure3_2.home)
            self.figure3_2.pos = -1
            self.figure3_2.moved = 0
        if self.figure3_3.pos == figure.pos and self.figure3_3.id != figure.id and self.figure3_3.finished == False:
            self.board.coords(self.figure3_3.id, *self.figure3_3.home)
            self.figure3_3.pos = -1
            self.figure3_3.moved = 0
        if self.figure3_4.pos == figure.pos and self.figure3_4.id != figure.id and self.figure3_4.finished == False:
            self.board.coords(self.figure3_4.id, *self.figure3_4.home)
            self.figure3_4.pos = -1
            self.figure3_4.moved = 0

        # Player 4 check  
        if self.figure4_1.pos == figure.pos and self.figure4_1.id != figure.id and self.figure4_1.finished == False:
            self.board.coords(self.figure4_1.id, *self.figure4_1.home)
            self.figure4_1.pos = -1
            self.figure4_1.moved = 0
        if self.figure4_2.pos == figure.pos and self.figure4_2.id != figure.id and self.figure4_2.finished == False:
            self.board.coords(self.figure4_2.id, *self.figure4_2.home)
            self.figure4_2.pos = -1
            self.figure4_2.moved = 0
        if self.figure4_3.pos == figure.pos and self.figure4_3.id != figure.id and self.figure4_3.finished == False:
            self.board.coords(self.figure4_3.id, *self.figure4_3.home)
            self.figure4_3.pos = -1
            self.figure4_3.moved = 0
        if self.figure4_4.pos == figure.pos and self.figure4_4.id != figure.id and self.figure4_4.finished == False:
            self.board.coords(self.figure4_4.id, *self.figure4_4.home)
            self.figure4_4.pos = -1
            self.figure4_4.moved = 0

    def check_win(self):
        winner = self.turn
        end = False
        if set((self.figure1_1.moved, self.figure1_2.moved, self.figure1_3.moved, self.figure1_4.moved)) == set((44,43,42,41)):
            winner = 1
            end = True
        if set((self.figure2_1.moved, self.figure2_2.moved, self.figure2_3.moved, self.figure2_4.moved)) == set((44,43,42,41)):
            winner = 2
            end = True
        if set((self.figure3_1.moved, self.figure3_2.moved, self.figure3_3.moved, self.figure3_4.moved)) == set((44,43,42,41)):
            winner = 3
            end = True
        if set((self.figure4_1.moved, self.figure4_2.moved, self.figure4_3.moved, self.figure4_4.moved)) == set((44,43,42,41)):
            winner = 4
            end = True

        # WIN window
        if end:
            self.window.destroy()
            self.end_screen = tk.Tk()
            self.end_screen.focus()
            self.end_screen.title("Game Over")
            self.end_screen.geometry(f"{self.board_size}x{self.board_size}")
            self.canvas = tk.Canvas(self.end_screen, width = self.board_size, height = self.board_size, bg="#d9c59e")
            self.canvas.pack(fill=tk.BOTH, expand=True)

            winner_sign_font = font.Font(family='Times', size=40, weight='bold')
            self.winner_text = self.canvas.create_text(self.board_size/2, self.board_size//11, text=f'PLAYER {winner} WON', font=winner_sign_font, fill=self.player_colors[winner - 1])

            # Back to Menu button
            menu = tk.Button(self.canvas, text="Back To Menu", font=("Helvetica", 32), bg=self.player_colors[winner - 1], command=self.back_to_menu, activebackground=self.player_colors[winner - 1], anchor='center')
            menu.place(x=(self.board_size//11)*3.3, y=(self.board_size/11)*9)

            # Trophy Image
            img = tk.PhotoImage(file='trophy.png')
            self.canvas.create_image((self.board_size//11)*5.5, (self.board_size/11)*5.5, image = img, anchor='center')
            self.animation()

    def mouse_click(self, event):
        self.mouse_pos = (event.x, event.y)
        selected = self.board.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)

        # Can move figure from selected player
        for item in selected:
            if item in self.all_figures[self.turn - 1]:
                self.mouse_hold.append(item)

        # for item in selected: # Used for testing
        #     if item in self.all_figures[0] or item in self.all_figures[1] or item in self.all_figures[2] or item in self.all_figures[3] :
        #         self.mouse_hold.append(item)

    def mouse_drag(self,event):
        for id in self.mouse_hold:
            self.board.coords(id, event.x, event.y)

    def mouse_release(self, event):
        try:
            self.pop_figure(event)
            self.mouse_hold.pop()
        except IndexError:
            #print('Mouse realse IndexError')
            pass

    def space_action(self,event):
        if self.move == False: # Roll dice
            self.dice_roll()
        # elif self.move == True: # Move a Figure
        #     self.all_figures[]

    def animation(self):
        frames = []

        for i in range(41): #pocet frameov
            img = tk.PhotoImage(file = f'firework_blue/frame_{i}_delay-0.1s.png')
            frames.append(img)

        img = tk.PhotoImage(file = 'firework_blue/frame_0_delay-0.1s.png')
        id_1 = self.canvas.create_image( (self.board_size//11)*2 , (self.board_size//11)*7, image = img)
        id_2 = self.canvas.create_image( (self.board_size//11)*9 , (self.board_size//11)*7, image = img)
        id_3 = self.canvas.create_image( (self.board_size//11)*2 , (self.board_size//11)*4, image = img)
        id_4 = self.canvas.create_image( (self.board_size//11)*9 , (self.board_size//11)*4, image = img)

        self.firework_animation(id_1,id_2,id_3,id_4,frames)

    def firework_animation(self,id_1,id_2,id_3,id_4,frames):
        while True:
            for i in range(41):
                self.canvas.itemconfig(id_1, image=frames[i] )
                self.canvas.itemconfig(id_2, image=frames[i] )
                self.canvas.itemconfig(id_3, image=frames[i] )
                self.canvas.itemconfig(id_4, image=frames[i] )
                self.canvas.after(75)
                self.canvas.update()

    def back_to_menu(self):
        self.end_screen.destroy()
        Clovece()

    def back_to_menu_setting(self):
        # Close Window
        self.settings_canvas.destroy()

        # Re-open Menu
        self.menu_board = tk.Canvas(self.window, width = self.board_size, height = self.board_size, bg="#d9c59e")
        self.menu_board.pack(fill=tk.BOTH, expand=True)
        self.create_menu()

    def back_to_menu_game(self):
        # Close Window
        self.window.destroy()

        Clovece()

    def save_game(self):
        file = open('save.txt','w')

        save = {
            'figures':{
                'figure1_1': [
                    [self.figure1_1.pos],
                    [self.figure1_1.moved]
                ],
                'figure1_2': [
                    [self.figure1_2.pos],
                    [self.figure1_2.moved]
                ],
                'figure1_3': [
                    [self.figure1_3.pos],
                    [self.figure1_3.moved]
                ],
                'figure1_4': [
                    [self.figure1_4.pos],
                    [self.figure1_4.moved]
                ],
                'figure2_1': [
                    [self.figure2_1.pos],
                    [self.figure2_1.moved]
                ],
                'figure2_2': [
                    [self.figure2_2.pos],
                    [self.figure2_2.moved]
                ],
                'figure2_3': [
                    [self.figure2_3.pos],
                    [self.figure2_3.moved]
                ],
                'figure2_4': [
                    [self.figure2_4.pos],
                    [self.figure2_4.moved]
                ],
                'figure3_1': [
                    [self.figure3_1.pos],
                    [self.figure3_1.moved]
                ],
                'figure3_2': [
                    [self.figure3_2.pos],
                    [self.figure3_2.moved]
                ],
                'figure3_3': [
                    [self.figure3_3.pos],
                    [self.figure3_3.moved]
                ],
                'figure3_4': [
                    [self.figure3_4.pos],
                    [self.figure3_4.moved]
                ],
                'figure4_1': [
                    [self.figure4_1.pos],
                    [self.figure4_1.moved]
                ],
                'figure4_2': [
                    [self.figure4_2.pos],
                    [self.figure4_2.moved]
                ],
                'figure4_3': [
                    [self.figure4_3.pos],
                    [self.figure4_3.moved]
                ],
                'figure4_4': [
                    [self.figure4_4.pos],
                    [self.figure4_4.moved]
                ],  
            },
            'data':[
                {'player_count': self.player_count},
                {'dice_animation': self.dice_animation},
                {'turn': self.turn},
                {'move': self.move},
                {'roll': self.roll}

            ]
        }

        json.dump(save, file)

        file.close()

    def load_refresh(self):
        save = json.load(open('save.txt'))

        self.title_animation_toggle = False
        self.window.destroy()

        Clovece(True,save)

    def load_game(self):
        save = self.save

        # Set Figures
        # Player 1
        self.figure1_1.pos = save['figures']['figure1_1'][0][0]
        self.figure1_1.moved = save['figures']['figure1_1'][1][0]
        self.figure1_2.pos = save['figures']['figure1_2'][0][0]
        self.figure1_2.moved = save['figures']['figure1_2'][1][0]
        self.figure1_3.pos = save['figures']['figure1_3'][0][0]
        self.figure1_3.moved = save['figures']['figure1_3'][1][0]
        self.figure1_4.pos = save['figures']['figure1_4'][0][0]
        self.figure1_4.moved = save['figures']['figure1_4'][1][0]
        # Player 2
        self.figure2_1.pos = save['figures']['figure2_1'][0][0]
        self.figure2_1.moved = save['figures']['figure2_1'][1][0]
        self.figure2_2.pos = save['figures']['figure2_2'][0][0]
        self.figure2_2.moved = save['figures']['figure2_2'][1][0]
        self.figure2_3.pos = save['figures']['figure2_3'][0][0]
        self.figure2_3.moved = save['figures']['figure2_3'][1][0]
        self.figure2_4.pos = save['figures']['figure2_4'][0][0]
        self.figure2_4.moved = save['figures']['figure2_4'][1][0]
        # Player 3
        self.figure3_1.pos = save['figures']['figure3_1'][0][0]
        self.figure3_1.moved = save['figures']['figure3_1'][1][0]
        self.figure3_2.pos = save['figures']['figure3_2'][0][0]
        self.figure3_2.moved = save['figures']['figure3_2'][1][0]
        self.figure3_3.pos = save['figures']['figure3_3'][0][0]
        self.figure3_3.moved = save['figures']['figure3_3'][1][0]
        self.figure3_4.pos = save['figures']['figure3_4'][0][0]
        self.figure3_4.moved = save['figures']['figure3_4'][1][0]
        # Player 4
        self.figure4_1.pos = save['figures']['figure4_1'][0][0]
        self.figure4_1.moved = save['figures']['figure4_1'][1][0]
        self.figure4_2.pos = save['figures']['figure4_2'][0][0]
        self.figure4_2.moved = save['figures']['figure4_2'][1][0]
        self.figure4_3.pos = save['figures']['figure4_3'][0][0]
        self.figure4_3.moved = save['figures']['figure4_3'][1][0]
        self.figure4_4.pos = save['figures']['figure4_4'][0][0]
        self.figure4_4.moved = save['figures']['figure4_4'][1][0]

        # Set Settings and Data
        self.player_count = save['data'][0]['player_count']
        self.dice_animation = save['data'][1]['dice_animation']
        self.turn = save['data'][2]['turn']
        self.move = save['data'][3]['move']
        self.roll = save['data'][4]['roll']

        self.move_after_load()

    def move_after_load(self):
        # Player 1
        for figure in [self.figure1_1,self.figure1_2,self.figure1_3,self.figure1_4]:
            if figure.pos != -1:
                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)

        # Player 2
        for figure in [self.figure2_1,self.figure2_2,self.figure2_3,self.figure2_4]:
            if figure.pos != -1:
                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)

        # Player 3
        for figure in [self.figure3_1,self.figure3_2,self.figure3_3,self.figure3_4]:
            if figure.pos != -1:
                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)

        # Player 4
        for figure in [self.figure4_1,self.figure4_2,self.figure4_3,self.figure4_4]:
            if figure.pos != -1:
                self.board.coords(figure.id, (self.main_area[figure.pos][0] + self.main_area[figure.pos][2])/2, (self.main_area[figure.pos][1] + self.main_area[figure.pos][3])/2)

        # Border Upadte 
        for id in self.borders[0]:
            self.board.itemconfig(id, fill=self.player_colors[self.turn-1] )

        self.board.update()

    def help(self):
        self.help_window = tk.Tk()
        self.help_window.focus()
        self.help_window.title('Help')
        self.help_window.geometry('500x500')
        text = tk.Text(self.help_window)
        text.insert('1.0','Controls: \n')
        text.insert('2.0','Spacebar - Roll The Dice \n')
        text.insert('3.0','Esc - Exit Program \n')
        text.insert('4.0','Mouse - Hold left click and drag a figure to desired position \n')
        text.insert('5.0','\n')
        text.insert('6.0',"The Game won't let you move a figure to a location where it's not supposed to go. \n")
        text.insert('7.0',"If you are unable to move, make sure its your turn and you have'nt moved already. \n")
        text.pack()

        text['state'] = 'disabled'

        self.help_window.mainloop()

    def about(self):
        self.about_window = tk.Tk()
        self.about_window.focus()
        self.about_window.title("About")
        text = tk.Text(self.about_window)
        text.insert('1.0','Game digitalized by: Peter Hozlár \n')
        text.insert('2.0','\n')
        text.insert('3.0','If you wish to know more about original board game copy the link below: \n')
        text.insert('4.0','https://en.wikipedia.org/wiki/Mensch_%C3%A4rgere_Dich_nicht \n')
        text.pack()

        text['state'] = 'disabled'

        self.about_window.mainloop()
        
    def exit_game(self,event=None):
        self.window.destroy()
        self.title_animation_toggle = False

class Figure:
    def __init__(self, player, position, id=None,home=None, moved=0, finish=False):
        self.player = player
        self.pos = position
        self.id = id
        self.home = home
        self.moved = moved
        self.finished = finish

    def __str__(self):
        return f'Player:{self.player} Moved:{self.moved} Position:{self.pos} Id:{self.id}'

    def __add__(self, iny):
        value = self.pos + iny.pos
        self.moved += iny.pos
        return Figure(self.player, value, self.id, self.home, self.moved, self.finished)

    def __sub__(self, iny):
        value = self.pos - iny.pos
        return Figure(self.player, value, self.id, self.home, self.moved, self.finished)   

    def __eq__(self, iny):
        if self.pos == iny.pos:
            return True
        
Clovece()