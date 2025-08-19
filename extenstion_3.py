# ---------------- Extension 3: Unit Conversion ----------------

LIMITS = {
    'temperature': {'min': 0, 'max': 45, 'unit': 'C'},
    'soc': {'min': 20, 'max': 80, 'unit': '%'},
    'charge_rate': {'min': 0, 'max': 0.8, 'unit': 'C-rate'}
}

LOW, HIGH, NORMAL, WARNING_LOW, WARNING_HIGH = 'LOW', 'HIGH', 'NORMAL', 'WARNING_LOW', 'WARNING_HIGH'
TOLERANCE_FACTOR = 0.015
LANG = 'en'

MESSAGES = {
    'temperature': {
        'en': {LOW: "Temp too low", HIGH: "Temp too high",
               WARNING_LOW: "Near hypothermia", WARNING_HIGH: "Near hyperthermia", NORMAL: "Temp OK"}
    }
}

def to_celsius(value, unit):
    return (value - 32) * 5/9 if unit == 'F' else value

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

def battery_is_ok(temp, soc, rate, temp_unit='C', reporter=ConsoleReporter()):
    vitals = {
        'temperature': to_celsius(temp, temp_unit),
        'soc': soc,
        'charge_rate': rate
    }
    status = True
    for vital, val in vitals.items():
        breach = classify_vital(val, LIMITS[vital]['min'], LIMITS[vital]['max'])
        if breach != NORMAL:
            reporter.report(vital, breach)
            if breach in (LOW, HIGH): status = False
    return status

def run_tests():
    assert battery_is_ok(98.6, 70, 0.7, temp_unit='F') == True
    assert battery_is_ok(212, 70, 0.7, temp_unit='F') == False
    print("Extension 3 optimized tests passed.")

if __name__ == "__main__":
    run_tests()
