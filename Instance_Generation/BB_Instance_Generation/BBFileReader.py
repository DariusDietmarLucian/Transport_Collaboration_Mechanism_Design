from Models.Location import Location


class BBFileReader:

    def __init__(self, r101_filename):
        self.r101_filename = r101_filename

        self.locations = None

    """
    *************
    ***PRIVATE***
    *************
    """

    @staticmethod
    def __read_string(data_string):
        data_array = data_string.split()

        if len(data_array) >= 3:
            id = int(data_array[0]) - 1
            x = int(float(data_array[1]))
            y = int(float(data_array[2]))
            location = Location(id=id, x=x, y=y)
            return location

        else:
            return None

    @staticmethod
    def __read_file(filename):
        locations = []
        file_text = open(filename, "r")

        for data_string in file_text.readlines():
            location = BBFileReader.__read_string(data_string=data_string)
            locations.append(location)

        return locations

    """
    *************
    ***GETTERS***
    *************
    """

    def get_locations(self):
        if self.locations is None:
            filename = self.get_filename()
            self.locations = self.__read_file(filename=filename)

        return self.locations

    def get_filename(self):
        return self.r101_filename
