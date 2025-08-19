# ---------------- Extension 1: Early Warning ----------------

LIMITS = {
    'temperature': {'min': 0, 'max': 45},
    'soc': {'min': 20, 'max': 80},
    'charge_rate': {'min': 0, 'max': 0.8}
}

LOW, HIGH, NORMAL, WARNING_LOW, WARNING_HIGH = 'LOW', 'HIGH', 'NORMAL', 'WARNING_LOW', 'WARNING_HIGH'
TOLERANCE_FACTOR = 0.015  # 1.5% of upper limit

class ConsoleReporter:
    def report(self, vital_name, message):
        print(f"{vital_name}: {message}")

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

# ✅ Tests
def run_tests():
    assert battery_is_ok(25, 70, 0.7) == True
    assert battery_is_ok(-1, 70, 0.7) == False
    assert battery_is_ok(46, 70, 0.7) == False
    assert battery_is_ok(25, 19, 0.7) == False
    assert battery_is_ok(25, 81, 0.7) == False
    assert battery_is_ok(25, 70, 0.9) == False
    print("Extension 1 optimized tests passed.")

if __name__ == "__main__":
    run_tests()


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
