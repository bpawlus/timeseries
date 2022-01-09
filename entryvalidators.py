def validate_floatentries(val):
    """Checks if values in text entries are positive float value.

    :param val: Value to check.
    :returns: If val is positive float. Rollbacks operation if false.
    """
    try:
        fval = float(val)
        if fval < 0:
            return False
    except:
        return False
    return True

def validate_digit(val):
    """Checks if values in text entries are positive integer value.

    :param val: Value to check.
    :returns: If val is positive int. Rollbacks operation if false.
    """
    if str.isdigit(val):
        if int(val) > 0:
            return True
        else:
            return False
    else:
        return False