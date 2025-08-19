# ---------------- Extension 2: Multi-language ----------------

LIMITS = {
    'temperature': {'min': 0, 'max': 45},
    'soc': {'min': 20, 'max': 80},
    'charge_rate': {'min': 0, 'max': 0.8}
}

LOW, HIGH, NORMAL, WARNING_LOW, WARNING_HIGH = 'LOW', 'HIGH', 'NORMAL', 'WARNING_LOW', 'WARNING_HIGH'
TOLERANCE_FACTOR = 0.015
LANG = 'en'

MESSAGES = {
    'temperature': {
        'en': {LOW: "Temperature too low!", HIGH: "Temperature too high!",
               WARNING_LOW: "Approaching hypothermia", WARNING_HIGH: "Approaching hyperthermia",
               NORMAL: "Temperature normal"},
        'de': {LOW: "Temperatur zu niedrig!", HIGH: "Temperatur zu hoch!",
               WARNING_LOW: "Annäherung an Unterkühlung", WARNING_HIGH: "Annäherung an Überhitzung",
               NORMAL: "Temperatur normal"}
    }
}

class ConsoleReporter:
    def report(self, vital, breach):
        print(MESSAGES.get(vital, MESSAGES['temperature'])[LANG][breach])

def classify_vital(value, vmin, vmax):
    tol = vmax * TOLERANCE_FACTOR
    if value < vmin: return LOW
    if value > vmax: return HIGH
    if value <= vmin + tol: return WARNING_LOW
    if value >= vmax - tol: return WARNING_HIGH
    return NORMAL

def battery_is_ok(temperature, soc, charge_rate, reporter=ConsoleReporter()):
    vitals = {'temperature': temperature, 'soc': soc, 'charge_rate': charge_rate}
    status = True
    for vital, val in vitals.items():
        breach = classify_vital(val, LIMITS[vital]['min'], LIMITS[vital]['max'])
        if breach != NORMAL:
            reporter.report(vital, breach)
            if breach in (LOW, HIGH): status = False
    return status

def run_tests():
    global LANG
    LANG = 'en'
    assert battery_is_ok(25, 70, 0.7) == True
    LANG = 'de'
    assert battery_is_ok(46, 70, 0.7) == False
    print("Extension 2 optimized tests passed.")

if __name__ == "__main__":
    run_tests()
