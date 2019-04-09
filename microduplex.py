#Dmitriy Smirnov
from microbit import display, button_a, button_b, sleep
import random

class Particle:
    __max_x_pos = 4
    __max_intensity = 9
    __min_intensity = 1
    __max_fading = 3
    __min_fading = 1


    def reset( self ):
        self.ypos = 4
        self.xpos = random.randint( 0, Particle.__max_x_pos )
        self.intensity = random.randint( Particle.__min_intensity, Particle.__max_intensity )
        self.fading = random.randint( Particle.__min_fading, Particle.__max_fading )
        self.velocity = 0.4 + self.intensity / 10 * random.random()
    def __init__( self, xpos, ypos ):
        self.ypos = ypos
        self.xpos = xpos  # random.randint( 0, Particle.__max_x_pos )
        self.intensity = random.randint( Particle.__min_intensity, Particle.__max_intensity )
        self.fading = random.randint( Particle.__min_fading, Particle.__max_fading )
        self.velocity = 0.4 + self.intensity / 10 * random.random()
    def draw( self ):
        display.set_pixel( self.xpos, int( self.ypos ), int( self.intensity ) )

    def next( self ):
        self.ypos -= self.velocity
        if self.ypos < 0:
            self.ypos = 0

        self.intensity -= 2 / ( 1 + pow( 2.71, -self.fading ) )
        if self.intensity < 0:
            self.intensity = 0

    def hasNext( self ):
        return self.ypos > 0

def fire():
    particles = [ Particle( 0, 0 ), Particle( 1, 0 ), Particle( 2, 0 ), Particle( 3, 0 ), Particle( 4, 0 ),
 #             Particle( 0, 1 ), Particle( 1, 1 ), Particle( 2, 1 ), Particle( 3, 1 ), Particle( 4, 1 ),
              Particle( 0, 2 ), Particle( 1, 2 ), Particle( 2, 2 ), Particle( 3, 2 ), Particle( 4, 2 ) ] 
 #             Particle( 0, 3 ), Particle( 1, 3 ), Particle( 2, 3 ), Particle( 3, 3 ), Particle( 4, 3 ),
 #             Particle( 0, 4 ), Particle( 1, 4 ), Particle( 2, 4 ), Particle( 3, 4 ), Particle( 4, 4 ) ]


    display.clear()
    while not( button_a.was_pressed() or button_b.was_pressed() ):
        for p in particles:
            p.draw()
        for p in particles:
            if p.hasNext():
                p.next()
            else:
                p.reset()
        sleep( 40 )
    return


def compact( rows ):
    result = [];
    for row in rows:
        cnt = len( row )
        if 0 == row.count( get_empty_value() ):
            result.insert( get_empty_value(), [ 0 for i in range( cnt ) ] )
        else:
            result.append( row )
    return result

def get_empty_value():
    return 0

def isempty( col ):
    return col == get_empty_value()

def draw( rows, x = 0, y = 0, empty = True ):
    rowid = y
    for row in rows:
        colid = x
        for col in row:
            if empty or not isempty( col ):
                display.set_pixel( colid, rowid, int( col ) )
            colid += 1
        rowid += 1
    return

def canmove( rows, fugure, x0, y0 ):
    y = y0
    for frow in fugure:
        x = x0
        for fcol in frow:
            if not isempty( fcol ):
                if y >= len( rows ): return False
                elif x >= len( rows[ y ] ): return False
                elif not isempty( rows[ y ][ x ] ): return False
            x += 1
        y += 1
    return True


def merge( rows, fugure, x0, y0, empty = True ):
    y = y0
    for frow in fugure:
        x = x0
        for fcol in frow:
            if empty or not isempty( fcol ):
                rows[ y ][ x ] = fcol
            x += 1
        y += 1
    return rows


def fade():
    l1 = [ [ 9, 9, 9, 9, 9 ], 
           [ 9, 8, 7, 8, 9 ], 
           [ 7, 6, 5, 6, 7 ],
           [ 5, 4, 3, 4, 5 ],
           [ 4, 3, 2, 3, 4 ],
           [ 3, 2, 1, 2, 3 ],
           [ 2, 1, 0, 1, 2 ],
           [ 1, 0, 0, 0, 1 ] ]
    for l in l1:
        draw( [ l,
                l,
                l,
                l,
                l ] )
        sleep( 100 )

brick = 7
duplex =[   [ [ brick ],
              [ brick] ],
            [ [ brick, brick ] ],
            [ [ brick ],
              [ brick ] ],
            [ [ brick, brick ] ],
            [ [ brick ],
              [ brick ] ]

    ]
fire()
figures = []
while True:
    while len( figures ) > 0 and not( button_a.was_pressed() or button_b.was_pressed() ):
        sleep( 20 )
    display.clear()
    figures = duplex
    fade()
    rows = [[ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ]]
    draw( rows )
    score = 0
    total_score = score
    level = 1
    delay = 100
    while True:
        moved = False
        y = -1
        x = 1
        figure = figures[ random.randint( 0, len( figures ) - 1 ) ]
        while canmove( rows, figure, x, y + 1 ):
            moved = True
            y = y + 1
            draw( rows )
            draw( figure, x, y, False )
            for i in range( 10 ):
                sleep( delay )
                if button_a.was_pressed() and x > 0 and canmove( rows, figure, x - 1, y ):
                    x -= 1
                    draw( rows )
                    draw( figure, x, y, False )
                if button_b.was_pressed() and canmove( rows, figure, x + 1, y ):
                    x += 1
                    draw( rows )
                    draw( figure, x, y, False )

        sleep( 200 )
        if not moved:
            break
        else:
            rows = merge( rows, figure, x, y, False )
            rows = compact( rows )
            draw( rows )
            score += 1
            if figures == duplex and score % ( 10 * level ) == 0:
                level += 1
                total_score += score;
                score = 0
                if delay > 10:
                    delay -= 5

    total_score += score;
    display.scroll( "SCORE " + str( total_score ) + " LEVEL " + str( level ) + "  ",
                    delay=80, wait=False, loop=True, monospace = False )

    sleep( 100 )
    button_a.was_pressed()
    button_b.was_pressed()
