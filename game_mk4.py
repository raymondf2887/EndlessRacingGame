# feinschliff
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


import random


edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)


surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

def tex_coord(x, y, n=4):
    # Return the bounding vertices of the texture square.

    m = 4.0 / n # use 4 for the whole texture
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    # Return a list of the texture squares for the top, bottom and side.

    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = [
        (top),
        (bottom),
        (side),
        (side),
        (side),
        (side),
    ]
    return result


# block type names and location on template go here (doesnt define resolution of texture)
# xy of back side of cube, xy of bottom side of cube, 2x xy of all other sides
BLOCK1 = tex_coords((0, 0), (0, 0), (50, 50))


def verts(x, y, z, n):
    vertices = (
        (1 + (2 * x), -1 + (2 * y), -1 + (2 * z)),
        (1 + (2 * x), 1 + (2 * y), -1 + (2 * z)),
        (-1 + (2 * x), 1 + (2 * y), -1 + (2 * z)),
        (-1 + (2 * x), -1 + (2 * y), -1 + (2 * z)),
        (1 + (2 * x), -1 + (2 * y), 1 + (2 * z)),
        (1 + (2 * x), 1 + (2 * y), 1 + (2 * z)),
        (-1 + (2 * x), -1 + (2 * y), 1 + (2 * z)),
        (-1 + (2 * x), 1 + (2 * y), 1 + (2 * z))
    )
    return (vertices)



forced = False


def Cube(vx, vy, vz, block):
    if not forced:
        glBegin(GL_QUADS)
        y = 0
        for surface in surfaces:
            x = 0
            y += 1
            for vertex in surface:
                x += 1
                glTexCoord2f(block[y - 1][2 * (x - 1)], block[y - 1][(2 * x) - 1])
                glVertex3fv(verts(vx, vy, vz, 1)[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(verts(vx, vy, vz, 1)[vertex])
        glEnd()
    else:
        texX = 0
        texY = 0
        glBegin(GL_QUADS)
        glTexCoord2f(0.0 + texX, 0.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(0.25 + texX, 0.0)
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(0.25 + texX, 0.25)
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0 + texX, 0.25)
        glVertex3f(-1.0, 1.0, 1.0)
        glEnd()


def loadTexture(filename):
    textureSurface = pygame.image.load(filename)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1) #convert image data to opengl friendly data
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glColor3f(1, 1, 1)
    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid
    glDisable(GL_TEXTURE_2D)


def drawText(x, y, Color, text):
    textSurface = font.render(text, True, (Color)).convert_alpha()
    # textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255)) # for text with background
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def plane(starposition, length, width,  wert):
    glBegin(GL_QUADS)

    # xyz coords of each corner
    glVertex3f( -(width/2), (0 + starposition + wert), 0)
    glVertex3f( (width/2), (0 + starposition + wert), 0)
    glVertex3f( (width/2), (length + starposition + wert), 0)
    glVertex3f( -(width/2), (length + starposition + wert), 0)

    glEnd()


def obstacle0(Block, wert):
    glColor4f(1, 0, 0, 1) # rgb + alpha
    glEnable(GL_TEXTURE_2D)

    Cube(-2, 8 + wert, 0.5, Block) # (3x x y z coords + 1x template variables)
    Cube(2, 8 + wert, 0.5, Block)
    Cube(0.01, 0 + wert, 0.5, Block)

    glDisable(GL_TEXTURE_2D) # stop loading textures for future objects

    x_box = [-2       , 2      , 0.01    ]
    y_box = [8 + wert, 8 + wert, 0 + wert]
    return x_box, y_box


def obstacle1(Block, wert):
    glColor4f(1, 0, 0, 1) # rgb + alpha
    glEnable(GL_TEXTURE_2D)

    Cube(-2, 8 + wert, 0.5, Block) # (3x x y z coords + 1x template variables)
    Cube(-1, 8 + wert, 0.5, Block)
    Cube(1, 0 + wert, 0.5, Block)
    Cube(2, 0 + wert, 0.5, Block)

    glDisable(GL_TEXTURE_2D) # stop loading textures for future objects

    x_box = [-2, -1, 1, 2]
    y_box = [8 + wert, 8 + wert, 0 + wert, 0 + wert]
    return x_box, y_box


def obstacle2(Block, wert):
    glColor4f(1, 0, 0, 1) # rgb + alpha
    glEnable(GL_TEXTURE_2D)

    Cube(-1, 3 + wert, 0.5, Block) # (3x x y z coords + 1x template variables)
    Cube(-1, 2 + wert, 0.5, Block)
    Cube(-1, 1 + wert, 0.5, Block)
    Cube(-1, 0 + wert, 0.5, Block)

    Cube(2, 3 + wert, 0.5, Block)
    Cube(2, 2 + wert, 0.5, Block)
    Cube(2, 1 + wert, 0.5, Block)
    Cube(2, 0 + wert, 0.5, Block)

    Cube(-2, 0 + wert, 0.5, Block)

    glDisable(GL_TEXTURE_2D) # stop loading textures for future objects

    x_box = [-1, -1, -1, -1, 2, 2, 2, 2, -2]
    y_box = [3 + wert, 2 + wert, 1 + wert, 0 + wert, 3 + wert, 2 + wert, 1 + wert, 0 + wert, 0 + wert]
    return x_box, y_box

def obstacle3(Block, wert):
    glColor4f(1, 0, 0, 1) # rgb + alpha
    glEnable(GL_TEXTURE_2D)

    Cube(-2, 0 + wert, 0.5, Block) # (3x x y z coords + 1x template variables)
    Cube(-0.01, 5 + wert, 0.5, Block)
    Cube(2, 10 + wert, 0.5, Block)

    glDisable(GL_TEXTURE_2D) # stop loading textures for future objects

    x_box = [-2, -0.01, 2]
    y_box = [0 + wert, 5 + wert, 10 + wert]
    return x_box, y_box


once = True
def speedboost(Block, wert, acceleration, once, speed, score):
    glColor4f(0, 1, 1, 1)  # rgb + alpha
    glEnable(GL_TEXTURE_2D)

    Cube(-2, 3 + wert, -0.4, Block)  # (3x x y z coords + 1x template variables)
    Cube(-1, 3 + wert, -0.4, Block)
    Cube(0, 3 + wert, -0.4, Block)
    Cube(1, 3 + wert, -0.4, Block)
    Cube(2, 3 + wert, -0.4, Block)

    glDisable(GL_TEXTURE_2D)  # stop loading textures for future objects

    if once == True:
        if round(3 + wert) < 0:
            speed += acceleration
            once = False
    elif once == False:
        if round(3 + wert) > 0:
            once = True
    return speed, score, once


def randomobstacle(Block, lenght, width, wert, a):
    if   a == 0:
        glColor4f(1, 1, 1, 1)  # rgb + alpha
        plane(0, lenght, width, wert)
        x_box = [10]
        y_box = [10]
    elif a == 1:
        glColor4f(0, 1, 0, 1)  # rgb + alpha
        plane(0, lenght, width, wert)
        x_box, y_box = obstacle1(Block, wert / 2)
    elif a == 2:
        glColor4f(0, 0, 1, 1)  # rgb + alpha
        plane(0, lenght, width, wert)
        x_box, y_box = obstacle2(Block, wert / 2)
    elif a == 3:
        glColor4f(1, 0, 0, 1)  # rgb + alpha
        plane(0, lenght, width, wert)
        x_box, y_box = obstacle0(Block, wert / 2)
    elif a == 4:
        glColor4f(0.5, 0.5, 0.5, 1)  # rgb + alpha
        plane(0, lenght, width, wert)
        x_box, y_box = obstacle3(Block, wert / 2)

    return x_box, y_box


def collisiontest(x_sphere, y_sphere, x_box, y_box):
    crash = False
    for i in range(len(x_box)):
        if x_box[i] < x_sphere < x_box[i]+1 or x_box[i] < x_sphere+1 < x_box[i]+1:
            if y_box[i] < y_sphere < y_box[i]+1 or y_box[i] < y_sphere+1 < y_box[i]+1:
                crash = True
    return crash



# initate pygame, opengl and the windowscreen
pygame.init()
display = (1200, 800)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Game")

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# to enable drawing text with alpha background
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# lighting settings
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])


sphere = gluNewQuadric()

# player sphere coords
x_sphere = 0
y_sphere = 2
z_sphere = 1

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 120.0) #(fov |  aspect ratio of fov | nearest render distance | farthest render distance)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -9, 4, 0, 0, 4, 0, 0, 1) # xyz coords of camera, xyz coords of viewpoint, xyz coords of up point
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()
x_camera = 0

# initate mouse movement and center mouse on screen
displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)


loadTexture('_file_assets/tx_lines.png')

# set up text variables
Greentxt = (0, 255, 0, 255)
Redtxt = (255, 0, 0, 255)
Yellowtxt = (255, 255, 0, 255)
font = pygame.font.SysFont('arial', 64)
score = 0

# set up various variables
up_down_angle = 0.0
paused = False
run = True
crash = False
sphere_angle = 0

acceleration = 0.05
speed = 0.4
lenght = 50 # lenght
width = 10 #  width of each plane

wert = 0
wert1 = lenght
wert2 = lenght*2
wert3 = lenght*3
max = (lenght * 3)- speed*2

a = 0
b = random.randint(1,4)
c = random.randint(0,4)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                drawText(450, 500, Yellowtxt, f"Game Paused")
                pygame.display.flip()
                paused = not paused
                print(paused)
                pygame.mouse.set_pos(displayCenter)
                pygame.mouse.set_visible(True)
        if not paused:
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)

    if not paused:
        pygame.mouse.set_visible(False)
        # get keys
        keypress = pygame.key.get_pressed()
        # mouseMove = pygame.mouse.get_rel()

        # init model view matrix
        glLoadIdentity()

        # # apply the look up and down
        # up_down_angle += mouseMove[1] * 0.1
        # glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        if x_camera > -3.2:
            if keypress[pygame.K_d] or keypress[pygame.K_RIGHT]:
                glTranslatef(-0.125, 0, 0)
                x_camera -= 0.1
        if x_camera < 3.2:
            if keypress[pygame.K_a] or keypress[pygame.K_LEFT]:
                glTranslatef(0.125, 0, 0)
                x_camera += 0.1



        # # apply the left and right rotation
        # glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)

        # multiply the current matrix by the get the new view matrix and store the final view matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)


        # clear the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        # define current position of planes & obstacles
        if wert > -lenght:
            wert -= speed
        else :
            wert = max
            a = random.randint(0, 4)
            score += 1

        if wert1 > -lenght:
            wert1 -= speed
        else :
            wert1 = wert + lenght
            b = random.randint(0, 4)
            score += 1

        if wert2 > -lenght:
            wert2 -= speed
        else :
            wert2 = wert1 + lenght
            c = random.randint(0, 4)
            score += 1

        if wert3 > -lenght:
            wert3 -= speed
        else :
            wert3 = wert2 + lenght
            score += 1




        # render obstacles & planes
        glPushMatrix()
        x_boxa, y_boxa = randomobstacle(BLOCK1, lenght, width, wert, a)
        glPopMatrix()

        glPushMatrix()
        x_boxb, y_boxb = randomobstacle(BLOCK1, lenght, width, wert1, b)
        glPopMatrix()

        glPushMatrix()
        x_boxc, y_boxc = randomobstacle(BLOCK1, lenght, width, wert2, c)
        glPopMatrix()

        glPushMatrix()
        glColor4f(0, 1, 1, 1)  # rgb + alpha
        plane(0, lenght, width, wert3) # (starposition, length, width,  wert):
        speed, score, once = speedboost(BLOCK1, wert3/2, acceleration, once, speed, score)
        glPopMatrix()


        if sphere_angle < 360:
            sphere_angle += speed * (lenght / 4)
        else :
            sphere_angle = 0

        # initial player sphere
        glPushMatrix() # restart matrix to move only player
        glEnable(GL_TEXTURE_2D)
        gluQuadricTexture(sphere, GL_TRUE)
        if x_sphere < 4:
            if keypress[pygame.K_d] or keypress[pygame.K_RIGHT]:
                x_sphere=x_sphere + 0.125
        if x_sphere > -4:
            if keypress[pygame.K_a] or keypress[pygame.K_LEFT]:
                x_sphere=x_sphere - 0.125
        glTranslatef(x_sphere, y_sphere, z_sphere)

        # rotate player spher for visual
        if keypress[pygame.K_d] or keypress[pygame.K_RIGHT]:
            glRotatef(-sphere_angle, 1, -0.5, 0)
        elif keypress[pygame.K_a] or keypress[pygame.K_LEFT]:
            glRotatef(-sphere_angle, 1, 0.5, 0)
        else:
            glRotatef(-sphere_angle, 1, 0, 0)
        glColor4f(1, 1, 0, 1) # rgb + alpha
        gluSphere(sphere, 1.0, 20, 20) # (context | radius | slices along the sphere's equator | stacks along the sphere's height)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


        # add text for the score
        drawText(585, 650, Greentxt, f"{round(score)}")

        glColor3f(0, 0, 1) # rgb color for cubes without textures

        # checking for collisions
        crash = collisiontest(x_sphere/2, y_sphere/2, x_boxa, y_boxa)
        if crash == False:
            crash = collisiontest(x_sphere/2, y_sphere/2, x_boxb, y_boxb)
            if crash == False:
                crash = collisiontest(x_sphere/2, y_sphere/2, x_boxc, y_boxc)

        # intro text
        if score < 3:
            drawText(740, 700, Greentxt, f"steer with a and d")
            drawText(750, 650, Greentxt, f"press p to pause")

        if score == 3:
            drawText(20, 600, (155, 255, 255, 255), f"Blue lines give speed boosts!")

        # update screen
        pygame.display.flip()
        pygame.time.wait(10)

        # testing for collisions
        if crash == True:
            drawText(450, 400, Redtxt, f"Game Over")
            pygame.display.flip()
            paused = not paused
            pygame.mouse.set_pos(displayCenter)
            pygame.mouse.set_visible(True)
            pygame.time.wait(1500)
            run = False

pygame.quit()
