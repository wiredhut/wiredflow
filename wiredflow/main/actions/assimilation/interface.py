from abc import abstractmethod


class ProxyStage:
    """
    Class for converting configuration parameters into desired Stage objects
    """

    @abstractmethod
    def compile(self):
        """ Generate object of Stage """
        raise NotImplementedError()
