from abc import ABC, ABCMeta, abstractmethod
from mrx2d.matrix import observable_matrix as matrix, matrix_observator as observator
import threading
from queue import Queue


def colorise(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


class Tile:
    pass


class Drawer(observator, metaclass=ABCMeta):  # ADD START/STOP METHODS
    def __init__(self, matrix: matrix) -> None:
        super().__init__()
        self._data = matrix
        self._data.subscribe(self)
        self._working_thread = threading.Thread(target=self.__thread_worker)
        self.__is_active = False
        self.__update_point = ()
        self.__updated_event = threading.Event()
        self.__update_event = threading.Event()
    
    def __thread_worker(self):
        while 1:
            self.__update_event.wait()
            self.__update_event.clear()
            self.draw(self.__update_point)
            self.__updated_event.set()
            if not self.__is_active:
                break


    def start(self):
        self._working_thread.start()
        self.__is_active = True

    def stop(self):
        self.__is_active = False
        self.__update_event.set()
        self._working_thread.join()

    @abstractmethod
    def drawAll(self) -> None:
        pass

    @abstractmethod
    def draw(self, point: tuple) -> None:
        pass

    def update(self, point: tuple) -> None:
        self.__update_point = point
        self.__update_event.set()
        self.__updated_event.wait()
        self.__updated_event.clear()
        #self.draw(point)
        # ADD MULTITHREADING


class console_drawer(Drawer):
    def __init__(self, matrix: matrix) -> None:
        super().__init__(matrix)

    def drawAll(self) -> None:
            print(flush=True)
            m = n = 255  # WRITE MAX ELEMENT FINDER
            matrix = self._data.get_raw_data()
            out_str = ""
            for x in [(a, b) for a in range(0, n, 5) for b in range(0, m, 5)]:
                out_str += matrix[x]
                if x[1] == 0:
                    out_str += "\n"
            print(out_str)

    def draw(self, point: tuple) -> None:
        self.drawAll()