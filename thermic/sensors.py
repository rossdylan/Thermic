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
    def __init__(self, root, sid):
        self.root = root
        self.sid = sid

        self.input_path = os.path.join(self.root, "{0}_input".format(self.sid))
        self.label_path = os.path.join(self.root, "{0}_label".format(self.sid))
        self.lowest_path = os.path.join(self.root, "{0}_lowest".format(self.sid))
        self.highest_path = os.path.join(self.root, "{0}_highest".format(self.sid))

    @classmethod
    def _to_celcius(cls, temp):
        if temp is None:
            return None
        else:
            return temp / 1000.0

    @classmethod
    def _to_fahrenheit(cls, temp):
        if temp is None:
            return None
        else:
            return (temp * 1.8) + 32.0

    @property
    def label(self):
        try:
            with open(self.label_path, 'r') as f:
                label_data = f.read()
        except:
            with open(os.path.join(self.root, "name"), 'r') as f:
                label_data = f.read()
        return label_data.strip()

    @property
    def raw(self):
        with open(self.input_path, 'r') as f:
            temp = float(f.read())
        return temp

    @property
    def tempc(self):
        temp = self.raw
        return temp / 1000.0  # change for millidegrees to degrees

    @property
    def tempf(self):
        return (self.tempc * 1.8) + 32.0

    @property
    def highest(self):
        try:
            with open(self.highest_path, 'r') as f:
                temp = float(f.read())
            return temp
        except:
            return None

    @property
    def highestc(self):
        return Sensor._to_celcius(self.highest)

    @property
    def highestf(self):
        return Sensor._to_fahrenheit(self.highestc)

    @property
    def lowest(self):
        try:
            with open(self.lowest_path, 'r') as f:
                temp = float(f.read())
            return temp
        except:
            return None

    @property
    def lowestc(self):
        return Sensor._to_celcius(self.lowest)

    @property
    def lowestf(self):
        return Sensor._to_fahrenheit(self.lowestc)

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
            sensors.append(Sensor(root, _id))
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
            if 'device' in dirs and any(map(lambda f: f.startswith('temp'), files)):
                dirs.remove('device')
            temperature_things = filter(lambda f: f.startswith('temp'), files)
            sensor_ids = set(map(
                lambda f: f.split("_")[0], temperature_things))
            sensors.extend(Sensor.from_ids(root, sensor_ids))
    return sensors
