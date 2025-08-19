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

# Global language setting
LANG = 'en'  # 'en' or 'de'

# Messages for reporting
MESSAGES = {
    'temperature': {
        'en': {
            LOW: "Temperature too low! Hypothermia risk.",
            HIGH: "Temperature too high! Hyperthermia risk.",
            WARNING_LOW: "Warning: Approaching hypothermia.",
            WARNING_HIGH: "Warning: Approaching hyperthermia.",
            NORMAL: "Temperature normal."
        },
        'de': {
            LOW: "Temperatur zu niedrig! Unterkühlungsgefahr.",
            HIGH: "Temperatur zu hoch! Hitzschlaggefahr.",
            WARNING_LOW: "Warnung: Annäherung an Unterkühlung.",
            WARNING_HIGH: "Warnung: Annäherung an Überhitzung.",
            NORMAL: "Temperatur normal."
        }
    },
    'soc': {
        'en': {
            LOW: "State of Charge too low!",
            HIGH: "State of Charge too high!",
            WARNING_LOW: "Warning: SOC approaching lower limit.",
            WARNING_HIGH: "Warning: SOC approaching upper limit.",
            NORMAL: "SOC normal."
        },
        'de': {
            LOW: "Ladezustand zu niedrig!",
            HIGH: "Ladezustand zu hoch!",
            WARNING_LOW: "Warnung: SOC nähert sich dem unteren Grenzwert.",
            WARNING_HIGH: "Warnung: SOC nähert sich dem oberen Grenzwert.",
            NORMAL: "SOC normal."
        }
    },
    'charge_rate': {
        'en': {
            LOW: "Charge rate too low!",
            HIGH: "Charge rate too high!",
            WARNING_LOW: "Warning: Charge rate approaching minimum.",
            WARNING_HIGH: "Warning: Charge rate approaching maximum.",
            NORMAL: "Charge rate normal."
        },
        'de': {
            LOW: "Laderate zu niedrig!",
            HIGH: "Laderate zu hoch!",
            WARNING_LOW: "Warnung: Laderate nähert sich dem Minimum.",
            WARNING_HIGH: "Warnung: Laderate nähert sich dem Maximum.",
            NORMAL: "Laderate normal."
        }
    }
}

# Reporter interface
class Reporter:
    def report(self, vital_name, breach_type):
        pass

# Default reporter: prints to console
class ConsoleReporter(Reporter):
    def report(self, vital_name, breach_type):
        print(MESSAGES[vital_name][LANG][breach_type])

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
    global LANG

    # English tests
    LANG = 'en'
    assert battery_is_ok(25, 70, 0.7) == True  # All normal
    assert battery_is_ok(-1, 70, 0.7) == False  # Temperature LOW

    # German tests
    LANG = 'de'
    assert battery_is_ok(25, 81, 0.7) == False  # SOC HIGH in German
    assert battery_is_ok(25, 70, 0.8 - (LIMITS['charge_rate']['max'] * TOLERANCE_FACTOR)/2) == True  # Warning in German

    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
