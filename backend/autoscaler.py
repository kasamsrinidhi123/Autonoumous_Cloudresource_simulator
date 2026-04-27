import time
import math
from datetime import datetime
from backend.metrics import calculate_cpu, calculate_memory

SCALE_OUT_THRESHOLD = 70
SCALE_IN_THRESHOLD = 30
COOLDOWN = 2  # seconds
MAX_INSTANCES = 10
MIN_INSTANCES = 1

def apply_autoscaling(state):
    """
    Runs the full autoscaling loop — scales up/down AND recalculates metrics
    until the system stabilizes. This simulates what happens in real AWS
    where CloudWatch + ASG continuously adjust.
    """
    now = time.time()

    if now - state.last_scaled_time < COOLDOWN:
        return

    # Run up to 10 adjustment rounds in a single tick to fully stabilize
    for _ in range(10):
        # Recalculate metrics with current instance count
        state.cpu_usage = calculate_cpu(state.active_users, state.instances)
        state.memory_usage = calculate_memory(state.active_users, state.instances)

        scaled = False

        # ── Scale OUT ──
        if state.cpu_usage > SCALE_OUT_THRESHOLD and state.instances < MAX_INSTANCES:
            old = state.instances
            # Calculate how many instances we actually need to reach ~50% CPU
            total_load = (state.cpu_usage / 100) * state.instances
            desired = math.ceil(total_load / 0.5)
            new_count = max(old + 1, desired)
            new_count = min(new_count, MAX_INSTANCES)
            state.instances = new_count
            state.total_scale_outs += 1

            _log_event(state, "SCALE OUT", "up", old, state.instances,
                       f"CPU {state.cpu_usage:.1f}% > {SCALE_OUT_THRESHOLD}% → added {state.instances - old} instance(s)")
            scaled = True

        # ── Scale IN ──
        elif state.cpu_usage < SCALE_IN_THRESHOLD and state.instances > MIN_INSTANCES:
            old = state.instances

            if state.cpu_usage < 5 and state.active_users == 0:
                new_count = MIN_INSTANCES
            elif state.cpu_usage < 15:
                new_count = max(MIN_INSTANCES, old // 2)
            else:
                total_load = (state.cpu_usage / 100) * state.instances
                desired = math.ceil(total_load / 0.5)
                new_count = max(MIN_INSTANCES, min(desired, old - 1))

            if new_count < old:
                state.instances = new_count
                state.total_scale_ins += 1
                removed = old - new_count

                _log_event(state, "SCALE IN", "down", old, state.instances,
                           f"CPU {state.cpu_usage:.1f}% < {SCALE_IN_THRESHOLD}% → removed {removed} instance(s)")
                scaled = True

        if not scaled:
            break

        # Recalculate after scaling to see the effect
        state.cpu_usage = calculate_cpu(state.active_users, state.instances)
        state.memory_usage = calculate_memory(state.active_users, state.instances)

    state.last_scaled_time = now


def _log_event(state, event_type, direction, old_count, new_count, reason):
    event = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": event_type,
        "direction": direction,
        "from": old_count,
        "to": new_count,
        "cpu": round(state.cpu_usage, 1),
        "reason": reason,
    }
    state.scaling_events.append(event)
    state.logs.append(f"[{event_type}] {old_count} → {new_count} instances (CPU: {state.cpu_usage:.1f}%)")
