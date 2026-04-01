def calculate_risk(condition):

    if condition == "Normal":
        return 10   # SAFE

    elif condition == "Hemolyzed":
        return 35   # Moderate

    elif condition == "Severely Degraded":
        return 55   # Still not extreme

    else:
        return 25