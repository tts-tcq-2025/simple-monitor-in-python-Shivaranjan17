# Threshold definition with tolerance support
LIMITS = {
    'temperature': {'min': 0, 'max': 45},
    'soc': {'min': 20, 'max': 80},
    'charge_rate': {'min': 0, 'max': 0.8}
}

# Breach types
LOW = 'LOW'
HIGH = 'HIGH'
NORMAL = 'NORMAL'
WARNING_LOW = 'WARNING_LOW'
WARNING_HIGH = 'WARNING_HIGH'

TOLERANCE_FACTOR = 0.015  # 1.5%

# Messages for reporting
MESSAGES = {
    'temperature': {
        LOW: "Temperature too low! Hypothermia risk.",
        HIGH: "Temperature too high! Hyperthermia risk.",
        WARNING_LOW: "Warning: Approaching hypothermia.",
        WARNING_HIGH: "Warning: Approaching hyperthermia.",
        NORMAL: "Temperature normal."
    },
    'soc': {
        LOW: "State of Charge too low!",
        HIGH: "State of Charge too high!",
        WARNING_LOW: "Warning: SOC approaching lower limit.",
        WARNING_HIGH: "Warning: SOC approaching upper limit.",
        NORMAL: "SOC normal."
    },
    'charge_rate': {
        LOW: "Charge rate too low!",
        HIGH: "Charge rate too high!",
        WARNING_LOW: "Warning: Charge rate approaching minimum.",
        WARNING_HIGH: "Warning: Charge rate approaching maximum.",
        NORMAL: "Charge rate normal."
    }
}

# Reporter interface
class Reporter:
    def report(self, vital_name, breach_type):
        pass

# Default reporter: prints to console
class ConsoleReporter(Reporter):
    def report(self, vital_name, breach_type):
        print(MESSAGES[vital_name][breach_type])

# Generic checker with warning zones
def check_breach(value, vital_limits):
    tolerance = vital_limits['max'] * TOLERANCE_FACTOR

    if value < vital_limits['min']:
        return LOW
    elif value > vital_limits['max']:
        return HIGH
    elif vital_limits['min'] <= value <= vital_limits['min'] + tolerance:
        return WARNING_LOW
    elif vital_limits['max'] - tolerance <= value <= vital_limits['max']:
        return WARNING_HIGH
    return NORMAL

# Battery check function
def battery_is_ok(temperature, soc, charge_rate, reporter=ConsoleReporter()):
    vitals = {
        'temperature': temperature,
        'soc': soc,
        'charge_rate': charge_rate
    }
    status = True
    for vital_name, value in vitals.items():
        breach = check_breach(value, LIMITS[vital_name])
        if breach != NORMAL:
            reporter.report(vital_name, breach)
            if breach in (LOW, HIGH):
                status = False  # hard failure only if out of range
    return status

# -----------------------
# Unit tests
# -----------------------
def run_tests():
    assert battery_is_ok(25, 70, 0.7) == True  # All normal

    # Hard breaches
    assert battery_is_ok(-1, 70, 0.7) == False  # Temperature LOW
    assert battery_is_ok(46, 70, 0.7) == False  # Temperature HIGH
    assert battery_is_ok(25, 19, 0.7) == False  # SOC LOW
    assert battery_is_ok(25, 81, 0.7) == False  # SOC HIGH
    assert battery_is_ok(25, 70, 0.9) == False  # Charge Rate HIGH

    # Boundary exact values
    assert battery_is_ok(0, 20, 0.8) == True    # Lower boundary
    assert battery_is_ok(45, 80, 0.8) == True   # Upper boundary

    # Warning zones
    tolerance_temp = LIMITS['temperature']['max'] * TOLERANCE_FACTOR
    tolerance_soc = LIMITS['soc']['max'] * TOLERANCE_FACTOR
    tolerance_charge = LIMITS['charge_rate']['max'] * TOLERANCE_FACTOR

    assert battery_is_ok(0 + tolerance_temp/2, 70, 0.7) == True   # Near LOW temp (warning only)
    assert battery_is_ok(45 - tolerance_temp/2, 70, 0.7) == True  # Near HIGH temp (warning only)

    assert battery_is_ok(25, 20 + tolerance_soc/2, 0.7) == True   # Near LOW SOC warning
    assert battery_is_ok(25, 80 - tolerance_soc/2, 0.7) == True   # Near HIGH SOC warning

    assert battery_is_ok(25, 70, 0.8 - tolerance_charge/2) == True  # Near HIGH charge rate warning

    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
