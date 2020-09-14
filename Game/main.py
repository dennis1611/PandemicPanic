

import pygame as pg
import numpy as np


# Colours
black = (0, 0, 0)
white = (255, 255, 255)
bgcolour = black

# Set up pygame window
pg.init()
xmax = 1344
ymax = 756
res = (xmax, ymax)
scr = pg.display.set_mode(res)

# Load bitmaps
# ballimg = pg.image.load("ball.gif")
# ballrect = ballimg.get_rect()


# Init model
# x = 0.
# v = 0.


# Set up loop & timing
tlast = pg.time.get_ticks() * 0.001
running = True

# Main loop
while running:

    # Get time step
    t = pg.time.get_ticks() * 0.001
    dt = min(0.01, t - tlast)
    tlast = t

    # get key input
    keys = pg.key.get_pressed()

    # Model: calculate forces & accelerations

    # Integrate
    # v = v + a*dt
    # x = x + v*dt

    # Clear screen
    scr.fill(bgcolour)
    # ballrect.center = int(x),int(y)
    # scr.blit(ballimg,ballrect)

    # Show frame
    pg.display.flip()

    # check for quit event (closing window)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # escape key check: also quit
    if keys[pg.K_ESCAPE]:
        running = False

    # event pump, prevent freeze
    pg.event.pump()

    # ---end of main loop

# Close window
pg.quit()

print("Normal end.")



