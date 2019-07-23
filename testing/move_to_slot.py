

def move_to_slot(pos=0, absolute=True, storage=True):
    """Move the storage rack to the specified position

    Args: int pos - default 0 - accepts -ve value if using relative positioning system
          boolean abs - default True - to use absolute positioning
                                False - relative positioning
          boolean storage - defualt True - determines weather storing or retrieving
                                    False - retrieval
    Returns: None
    """
    offset_storage = 127.5 #config.getint('ANGLE', "offset_storage")
    direction = 1
    offset_retrieval = 90 + offset_storage #offset in degrees
    carousel_pitch = 3 #config.getint('ANGLE', "carousel_pitch")
    global carousel_curr_pos

    rev = 0
    abs_pos = 0
    if storage:
        # move slot no. given by pos to storage operation
        logger.info("Moving to slot {} for storage".format(pos))
        abs_pos = (offset_storage + carousel_pitch*pos)/360
    else:
        # move slot no. given by pos to retrieval operation
        logger.info("Moving to slot {} for retrieval".format(pos))
        abs_pos = (offset_retrieval + carousel_pitch*pos)/360

    rev = carousel_curr_pos - abs_pos
    carousel_curr_pos = abs_pos
    if rev > 0:
        direction = 0
    else:
        direction = 1

    m1.drive_motor(revolutions=abs(rev), direction=direction)
    return rev
