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

ax = plt.axes()
ax.set_facecolor("green")

plt.xlim([s.MIN_XLIM, s.MAX_XLIM])
plt.ylim([s.MIN_YLIM, s.MAX_YLIM])
plt.xticks(np.arange(s.MIN_XLIM, s.MAX_XLIM, 1))

flower_scat = plt.scatter([], [], s=100)

steps = s.STEPS
lines = [plt.scatter([b.pos[0]], [b.pos[1]], s=20) for b in bees]

SNAPSHOT_X = []
SNAPSHOT_Y = []

def animate(t):
    global lim, SNAPSHOT_X, SNAPSHOT_Y
    for j, b in enumerate(bees):
        b.take_step(flowers)
        x, y = b.pos
        #oldx, oldy = lines[j].get_data(orig=False)
        old_off = lines[j].get_offsets()
        oldx, oldy = zip(*old_off)
            
        newx = np.concatenate([oldx[-s.MEMORY:], [x]])
        newy = np.concatenate([oldy[-s.MEMORY:], [y]])

        if len(newx) > 100:
            SNAPSHOT_X = newx
            SNAPSHOT_Y = newy

        #lines[j].set_xdata(newx)
        new_offsets = np.array(list(list(p) for p in zip(newx, newy)))
        lines[j].set_offsets(new_offsets)
        #lines[j].set_ydata(newy)
        trail_size = len(new_offsets)
        cols = []
        if trail_size > 4:
            ones = np.ones(trail_size-4)
            cols += list(zip(ones, ones, ones, np.linspace(0.1, 1, trail_size-4)**10))
        cols += ["black", "yellow", "yellow", "black"]
        lines[j].set_color(cols)
        lines[j].set_sizes([1] * (trail_size-4) + [20] * 4)
        
    
    if flowers:
        flower_data = (np.array([f.pos for f in flowers]))
        flower_cols = np.array([f.col for f in flowers])
        flower_scat.set_offsets(flower_data)
        flower_scat.set_color(flower_cols)
        #flower_scat.set_offsets(np.vstack([flower_data[0], flower_data[1]]))
        #flower_scat.set_colors(flower_data[2])
    plt.title(f"T={t}")


def spawn_flower(event):
    global flowers
    flowers += [flower.new_flower(flower.ROSE, event.xdata, event.ydata)]

cid = plt.gcf().canvas.mpl_connect('button_press_event', spawn_flower)
anim = animation.FuncAnimation(plt.gcf(), animate, interval=1)
plt.show()

