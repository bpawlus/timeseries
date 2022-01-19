def validate_float_pos_zero(val):
    """Checks if value is positive (or zero) float value.

    :param val: Value to check.
    :returns: If val meets requirements. Rollbacks operation if false.
    """
    try:
        fval = float(val)
        if fval >= 0:
            return True
    except:
        return False
    return False

def validate_float(val):
    """Checks if value is float value.

    :param val: Value to check.
    :returns: If val meets requirements. Rollbacks operation if false.
    """
    try:
        fval = float(val)
    except:
        return False
    return True

def validate_float_pos(val):
    """Checks if value is positive float value.

    :param val: Value to check.
    :returns: If val meets requirements. Rollbacks operation if false.
    """
    try:
        fval = float(val)
        if fval > 0:
            return True
    except:
        return False
    return False

def validate_int_pos(val):
    """Checks 0
    
    :param val: Value to check.
    :returns: If val meets requirements. Rollbacks operation if false.
    """
    if str.isdigit(val):
        if int(val) > 0:
            return True
        else:
            return False
    else:
        return False