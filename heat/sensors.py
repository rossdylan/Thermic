import os


class Sensor(object):
    """
    Take in a root path, and the paths to the input and label files
    Provides a simple interface to accessing temperature data from a sensor

    :param root: root directory of this sensor
    :type root: str

    :param input_path: path to the sensor data file
    :type input_path: str

    :param label_path: path to the label for this sensor
    :type label_path: str
    """
    def __init__(self, root, input_path, label_path):
        self.root = root
        self.input_path = input_path
        self.label_path = label_path

    @property
    def label(self):
        try:
            with open(self.label_path,'r') as f:
                label_data = f.read()
        except:
            with open(os.path.join(self.root,"name"), 'r') as f:
                label_data = f.read()
        return label_data.strip()

    @property
    def raw(self):
        with open(self.input_path,'r') as f:
            temp = float(f.read())
        return temp

    @property
    def tempc(self):
        temp = self.raw
        return temp / 1000.0 # change for millidegrees to degrees

    @property
    def tempf(self):
        return (self.tempc * 1.8) + 32.0

    def __repr__(self):
        return self.label

    @classmethod
    def from_ids(cls, root, ids):
        """
        Take in a list of sensor ids, and the root directory they are in
        then make a list of sensors out of them

        :param root: root directory of these sensors
        :type root: str

        :param ids: list of sensor ids to turn into sensor objs
        :type ids: [str]

        :returns [Sensor]
        """
        sensors = []
        for _id in ids:
            label_f = os.path.join(root, "{0}_label".format(_id))
            input_f = os.path.join(root, "{0}_input".format(_id))
            sensors.append(Sensor(root, input_f, label_f))
        return sensors


def find_sensors():
    """
    Find all temperature sensors on the machine
    """
    locations = [
        '/proc/acpi/thermal_zone',
        '/sys/class/hwmon']
    sensors = []
    for loc in locations:
        for root, dirs, files in os.walk(loc, followlinks=True):
            if 'subsystem' in dirs:
                dirs.remove('subsystem')
            if 'power' in dirs:
                dirs.remove('power')
            if 'driver' in dirs:
                dirs.remove('driver')
            if 'hwmon' in dirs:
                dirs.remove('hwmon')
            temperature_things = filter(lambda f: "temp" in f, files)
            sensor_ids = set(map(lambda f: f.split("_")[0], temperature_things))
            sensors.extend(Sensor.from_ids(root, sensor_ids))
    return sensors
