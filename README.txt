pijuice apis here https://github.com/PiSupply/PiJuice/tree/master/Software#command-abstraction-layer

```
#!/usr/bin/python3
from pijuice import PiJuice # Import pijuice module
pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object
print(pijuice.status.GetStatus()) # Read PiJuice status.

{'data':{
'isFault':is_fault,
'isButton':is_button,
'battery':battery_status,
'powerInput':power_input_status,
'powerInput5vIo':5v_power_input_status
}}
```
