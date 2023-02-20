import numpy as np
import style as s, flower, bee
from matplotlib import pyplot as plt, animation

Bee = bee.Bee
ETA = s.ETA
GAMMA = s.GAMMA
BETA = s.BETA
DELTA = s.DELTA
bee_count = s.BEE_COUNT

bees = [Bee(np.zeros(2), np.random.random() * 2 * np.pi, ETA, GAMMA, BETA, DELTA) for _ in range(bee_count)]
#flowers = [flower.new_flower(flower.ROSE, x, y) for x in range(s.MIN_XLIM, s.MAX_XLIM, 3)
        #for y in range(s.MIN_YLIM, s.MAX_YLIM, 3)]
flowers = []
flower_scat = plt.scatter([], [], s=100)

steps = s.STEPS
lines = [plt.plot([b.pos[0]], [b.pos[1]], s.LINE_STYLE, markersize=3)[0] for b in bees]

def animate(t):
    global lim
    for j, b in enumerate(bees):
        b.take_step(flowers)
        x, y = b.pos
        oldx, oldy = lines[j].get_data(orig=False)
            
        newx = np.concatenate([oldx[-s.MEMORY:], [x]])
        newy = np.concatenate([oldy[-s.MEMORY:], [y]])

        lines[j].set_xdata(newx)
        lines[j].set_ydata(newy)
    
    if flowers:
        flower_data = (np.array([f.pos for f in flowers]))
        flower_cols = np.array([f.col for f in flowers])
        flower_scat.set_offsets(flower_data)
        flower_scat.set_color(flower_cols)
        #flower_scat.set_offsets(np.vstack([flower_data[0], flower_data[1]]))
        #flower_scat.set_colors(flower_data[2])


size = 10
plt.xlim([s.MIN_XLIM, s.MAX_XLIM])
plt.ylim([s.MIN_YLIM, s.MAX_YLIM])

def spawn_flower(event):
    global flowers
    flowers += [flower.new_flower(flower.ROSE, event.xdata, event.ydata)]

cid = plt.gcf().canvas.mpl_connect('button_press_event', spawn_flower)

anim = animation.FuncAnimation(plt.gcf(), animate, interval=1)
plt.show()


