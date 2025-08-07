# src/api/services/style_drift.py

def detect_style_drift(keypress_events):
    if len(keypress_events) < 2:
        return {
            "flag": False,
            "confidence": 0.1,
            "evidence": "Not enough data"
        }

    speeds = []
    for i in range(1, len(keypress_events)):
        time_diff = keypress_events[i].timestamp - keypress_events[i-1].timestamp
        char_diff = keypress_events[i].char_count - keypress_events[i-1].char_count

        if time_diff > 0:
            speed = char_diff / time_diff
            speeds.append(speed)

    if len(speeds) < 2:
        return {
            "flag": False,
            "confidence": 0.2,
            "evidence": "Minimal typing data"
        }

    avg_speed = sum(speeds) / len(speeds)
    speed_variance = sum((s - avg_speed)**2 for s in speeds) / len(speeds)

    if speed_variance > 10:  # Arbitrary threshold for drift
        return {
            "flag": True,
            "confidence": min(speed_variance / 20, 1.0),
            "evidence": f"Typing speed variance high ({speed_variance:.2f})"
        }

    return {
        "flag": False,
        "confidence": 0.3,
        "evidence": f"Normal typing style (variance: {speed_variance:.2f})"
    }
