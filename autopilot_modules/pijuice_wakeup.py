# pijuice import
import json

try:
    from autopilot_modules.pijuice import PiJuice
except ModuleNotFoundError as e:
    from pijuice import PiJuice

pijuice = PiJuice(1, 0x14)

def edit_min_charge(val: str):
    # sudo chmod -R a+rwX /var/lib/pijuice/
    with open('/var/lib/pijuice/pijuice_config.JSON', 'r+') as f:
        data = json.load(f)
        data['system_task']['min_charge']['threshold'] = val
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def debug():
    print(dir(pijuice))
    print('---')
    print(dir(pijuice.rtcAlarm))
    print('---')
    print(pijuice.rtcAlarm.GetControlStatus())
    print(pijuice.rtcAlarm.GetTime())
    print('---')
    print(dir(pijuice.power))
    print(pijuice.power.GetWakeUpOnCharge())
    print('---')
    print(dir(pijuice.config))
    print(pijuice.config.GetBatteryProfile())
    print('---')


if __name__ == "__main__":
    edit_min_charge('50')
