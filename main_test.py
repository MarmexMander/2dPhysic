import sys
import time
from multiprocessing import Process
from mrx2d.matrix import observable_matrix as matrix
from mrx2d.output.drawers import console_drawer as Drawer
def main():
    t_start = time.time()
    def colored(r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)
    _outMatrix = matrix()
    _3DMatrix = matrix(3)
    _outMatrix = matrix()
    drawer = Drawer(_outMatrix)
    drawer.start()
    t_inited = time.time()
    for x in [
        (a, b, c)
        for a in range(0, 255, 5)
        for b in range(0, 255, 5)
        for c in range(0, 255, 5)
    ]:
        _3DMatrix[x] = colored(x[0], x[1], x[2], "#")
    t_gened = time.time()
    print()
    print("Initializing: " + (t_inited-t_start).__str__())
    print("Generation: " + (t_gened-t_inited).__str__())
    time.sleep(3)
    t_start_anim = time.time()
    ts_redraw = []
    for i in range(0, 255, 5):
        t_start_redraw = time.time()
        _outMatrix.set_raw_data(_3DMatrix[tuple([i])].get_raw_data())
        t_redrawed = time.time()
        #print("Redraw: " + (t_redrawed-t_start_redraw).__str__())
        ts_redraw += [t_redrawed-t_start_redraw]
        #time.sleep(0.05)
    drawer.stop()
    t_anim_end = time.time()
    print("Initializing: " + (t_inited-t_start).__str__())
    print("Min/Max/Avg redraw: " + str(round(min(ts_redraw),4)) + "/" + str(round(max(ts_redraw),4)) + "/" + str(round(sum(ts_redraw) / len(ts_redraw),4)))
    print("FPS: " + (len(ts_redraw)/(t_anim_end-t_start_anim)).__str__())
    #Move colored to tile class. In all matrix must have tiles as elements. Rewrite Drawer for it


if __name__ == "__main__":
    main()