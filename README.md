# Heat
## Pure Python interface to linux temperature sensors

* MIT Licensed
* Simple to Use
* Pure python

```python
from heat import find_sensors
sensors = find_sensors()
print(sensors[0].label) # Name of the sensor
print(sensors[0].tempc) # temperature in Celcius
print(sensors[0].tempf) # Temperature in Farenheit
print(sensors[0].raw)   # temperature in MilliDegrees Celcius
```
