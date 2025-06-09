from src.backend.database import db, User

def check_lux_warning(lux, low_threshold, high_threshold):
    if lux < low_threshold:
        return "Warning: Lux level is too low!"
    elif lux > high_threshold:
        return "Warning: Lux level is too high!"
    else:
        return "Lux level is within the normal range."

def set_thresholds(user_id, low, high):
    user = User.query.get(user_id)
    if user:
        user.low_threshold = low
        user.high_threshold = high
        db.session.commit()
        return True
    return False

def get_thresholds(user_id):
    user = User.query.get(user_id)
    if user:
        return user.low_threshold, user.high_threshold
    return None, None