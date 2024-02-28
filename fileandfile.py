import os, sys; sys.argc = len(sys.argv)
import curses
from curses import *

def main(fileA, fileB):
    s = initscr()

    
    texta = open(fileA, errors="replace").read().splitlines()
    textb = open(fileB, errors="replace").read().splitlines()

    current_file = fileA

    s.keypad(True)

    oy = 0
    ox = 0

    start_color()
    init_pair(1, COLOR_WHITE, COLOR_RED)   # invaild char
    init_pair(2, COLOR_BLACK, COLOR_WHITE) # selection
    init_pair(3, COLOR_RED, COLOR_WHITE)   # invaild char selection
    curs_set(0)
    noecho()

    cy = 0
    cx = 0

    while 1:

        if current_file == fileA:
            text = texta
            textrev = textb
        elif current_file == fileB: 
            text = textb
            textrev = texta

        my, mx = s.getmaxyx()
        my -= 1

        s.clear()

        s.move(0, 0)
        posx = 0
        posy = 0
        for row in text[oy:oy+my-1]:
            for col in row[ox:ox+mx-1]:
                invaild = False
                try:
                    if textrev[posy+oy][posx+ox] != col:
                        invaild = True
                except IndexError: invaild = True

                if invaild:
                    if cy == posy and cx == posx:
                        s.attron(color_pair(3))
                    else:
                        s.attron(color_pair(1))
                else:
                    if cy == posy and cx == posx:
                        s.attron(color_pair(2))
                
                try:
                    s.addstr(posy, posx, col)
                except ValueError: s.addstr(posy, posx, ' ')

                try:
                    text[cy+oy][cx+ox]
                except IndexError: 
                    s.attroff(color_pair(1))
                    s.attroff(color_pair(2))
                    s.attroff(color_pair(3))
                    s.addstr(cy, cx, ' ', color_pair(2))

                s.attroff(color_pair(1))
                s.attroff(color_pair(2))
                s.attroff(color_pair(3))

                posx += 1
            posy += 1
            posx = 0


        s.addstr(my, 0, f"{fileA} - {fileB} ({current_file})")

        passed = True
        try:
            char = text[cy+oy][cx+ox]
        except IndexError: passed = False

        if passed == True:
            if char == '\n':
                char = "LF"
            elif char == chr(0):
                char = "NUL"
            elif char == chr(1):
                char = "SOH"
            elif char == chr(2):
                char = "STX"
            elif char == chr(3):
                char = "ETX"
            elif char == chr(4):
                char = "EOT"
            elif char == chr(5):
                char = "ENQ"
            elif char == chr(6):
                char = "ACK"
            elif char == chr(7):
                char = "BEL"
            elif char == chr(8):
                char = "BS"
            elif char == chr(9):
                char = "HT"
            elif char == chr(11):
                char = "VT"
            elif char == chr(12):
                char = "FF"
            elif char == chr(13):
                char = "CR"
            elif char == chr(14):
                char = "SO"
            elif char == chr(15):
                char = "SI"
            elif char == chr(16):
                char = "DLE"

        else:
            char = ' '

        try:
            s.addstr(my, mx-1-len(char), char)
        except curses.error: pass

        s.refresh()

        k = s.getch()
        if k == ord('q'):
            break
        elif k == ord('r'):
            if current_file == fileA:
                current_file = fileB
            else: current_file = fileA
        elif k == KEY_UP:
            oy -= 1
            if oy == -1:
                oy = 0
        elif k == KEY_DOWN:
            oy += 1
        elif k == KEY_LEFT:
            ox -= 1
            if ox == -1:
                ox = 0
        elif k == KEY_RIGHT:
            ox += 1
        elif k == ord('k'):
            cy -= 1
            if cy == -1:
                cy = 0
        elif k == ord('j'):
            cy += 1
            if cy == my:
                cy = my-1
        elif k == ord('l'):
            cx += 1
            if cx == mx:
                cx = mx-1
        elif k == ord('h'):
            cx -= 1
            if cx == -1:
                cx = 0

    endwin()

if __name__ == '__main__':
    if sys.argc < 3:
        print(f"usage: {sys.argv[0]} [file A] [file B]")
        print("""
Navigation:
h j k l            - cursor move
up down left right - scroll document
q                  - exit
r                  - change file
""")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
