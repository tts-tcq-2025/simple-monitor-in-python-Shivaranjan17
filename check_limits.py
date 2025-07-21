# Threshold definition
LIMITS = {
    'temperature': {'min': 0, 'max': 45},
    'soc': {'min': 20, 'max': 80},
    'charge_rate': {'min': 0, 'max': 0.8}
}

# Breach types
LOW = 'LOW'
HIGH = 'HIGH'
NORMAL = 'NORMAL'

# Reporter interface
class Reporter:
    def report(self, vital_name, breach_type):
        pass

# Default reporter: prints to console
class ConsoleReporter(Reporter):
    def report(self, vital_name, breach_type):
        print(f"{vital_name} is {breach_type}!")

# Generic checker
def check_breach(value, vital_limits):
    if value < vital_limits['min']:
        return LOW
    elif value > vital_limits['max']:
        return HIGH
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
            status = False
    return status

# -----------------------
# Unit tests
# -----------------------
def run_tests():
    assert battery_is_ok(25, 70, 0.7) == True  # All normal

    assert battery_is_ok(-1, 70, 0.7) == False  # Temperature LOW
    assert battery_is_ok(46, 70, 0.7) == False  # Temperature HIGH

    assert battery_is_ok(25, 19, 0.7) == False  # SOC LOW
    assert battery_is_ok(25, 81, 0.7) == False  # SOC HIGH

    assert battery_is_ok(25, 70, 0.9) == False  # Charge Rate HIGH

    # Boundary tests
    assert battery_is_ok(0, 20, 0.8) == True    # Lower boundary
    assert battery_is_ok(45, 80, 0.8) == True   # Upper boundary

    print("All tests passed.")

if __name__ == '__main__':
    run_tests()

