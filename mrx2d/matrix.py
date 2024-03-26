from abc import abstractmethod, ABC
import warnings
import multiprocessing as mulproc


class matrix_observator(ABC):
    @abstractmethod
    def update(self, point: tuple) -> None:
        pass

    # @abstractmethod
    # def update(self) -> None:
    #     pass


class observable_matrix:
    def __init__(self, dimensions=2, data={}) -> None:
        super().__init__()
        self.__lock = mulproc.Lock()
        self.__data = data
        self.__subs = []
        self.__dim = (
            list(data.keys())[0].__len__()
            if data.values().__len__() > 0
            else dimensions
        )

    def __iter__(self):
        return self.__data.__iter__()

    @staticmethod
    def __dig_matrix(matrix_data: dict, coords: tuple):
        result = {}
        keys = list(
            filter(
                (None).__ne__,
                map(
                    lambda x: None
                    if any(coord != x[idx] for idx, coord in enumerate(coords))
                    else x,
                    matrix_data.keys(),
                ),
            )
        )
        begin = list(matrix_data.keys())[0].__len__() - coords.__len__()
        for key in keys:
            result[key[begin - 1:]] = matrix_data[key]
        return observable_matrix(data=result)

    def set_raw_data(self, data):
        if self.__dim == list(data.keys())[0].__len__():
            self.__data = data
            self.__notify(None)
            
    def get_raw_data(self):
        return self.__data

    def __setitem__(self, idx: tuple, value):
        if idx.__len__() != self.__dim:
            raise TypeError("Provided " + idx.__len__().__str__() + 
            "D coordinates for " + self.__dim.__str__() + "D matrix")
        self.__data[idx] = value
        self.__notify(idx)

    def __getitem__(self, idx: tuple):
        if idx.__len__() == self.__dim:
            return self.__data[idx]
        else:
            return observable_matrix.__dig_matrix(self.__data, idx)

    def subscribe(self, subscriber: matrix_observator):
        self.__subs.append(subscriber)

    def __next__(self):
        return self.__data.__next__()

    def __notify(self, point: tuple):
        for sub in self.__subs:
            sub.update(point)
