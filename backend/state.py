import time
import random
import streamlit as st

INSTANCE_NAMES = [
    "alpha", "beta", "gamma", "delta", "epsilon",
    "zeta", "eta", "theta", "iota", "kappa"
]

class InstanceInfo:
    def __init__(self, index):
        self.id = f"i-{random.randint(10000,99999)}"
        self.name = f"instance-{INSTANCE_NAMES[index]}"
        self.cpu = 0.0
        self.memory = 0.0
        self.requests = 0
        self.status = "launching"  # launching → running → terminating
        self.health = "initializing"
        self.launched_at = time.time()
        self._boot_ticks = 2  # takes 2 ticks to become running

    def tick(self, users_per_instance):
        """Update this instance's metrics for one tick."""
        if self._boot_ticks > 0:
            self._boot_ticks -= 1
            self.status = "launching"
            self.health = "initializing"
            self.cpu = random.uniform(5, 15)
            self.memory = random.uniform(10, 20)
            return

        self.status = "running"

        # Each instance handles its share of users
        if users_per_instance > 0:
            self.cpu = min(100, (users_per_instance / 100) * 100 + random.uniform(-5, 5))
            self.memory = min(100, 15 + (users_per_instance / 120) * 60 + random.uniform(-3, 3))
            self.requests += int(users_per_instance * random.uniform(0.8, 1.2))
        else:
            self.cpu = max(0, random.uniform(1, 8))
            self.memory = max(5, random.uniform(8, 18))

        self.cpu = round(max(0, self.cpu), 1)
        self.memory = round(max(0, self.memory), 1)

        # Health based on CPU
        if self.cpu > 90:
            self.health = "critical"
        elif self.cpu > 75:
            self.health = "warning"
        else:
            self.health = "healthy"


class SystemState:
    def __init__(self):
        self.active_users = 0
        self.instances = 1
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.load_running = False

        # Individual instance tracking
        self.instance_fleet = [InstanceInfo(0)]

        self.history_cpu = []
        self.history_memory = []
        self.history_instances = []
        self.history_users = []
        self.history_timestamps = []

        self.logs = []
        self.scaling_events = []
        self.last_scaled_time = time.time()

        self.total_requests = 0
        self.total_scale_outs = 0
        self.total_scale_ins = 0

    def sync_fleet(self):
        """Sync the instance_fleet list to match self.instances count."""
        current = len(self.instance_fleet)
        target = self.instances

        # Add new instances
        while len(self.instance_fleet) < target:
            idx = len(self.instance_fleet)
            self.instance_fleet.append(InstanceInfo(idx % len(INSTANCE_NAMES)))

        # Remove excess instances (mark as terminating, then remove)
        while len(self.instance_fleet) > target:
            self.instance_fleet.pop()

    def tick_fleet(self):
        """Update all individual instance metrics."""
        self.sync_fleet()

        running_count = len(self.instance_fleet)
        users_per_instance = self.active_users / running_count if running_count > 0 else 0

        for inst in self.instance_fleet:
            inst.tick(users_per_instance)

    def get_fleet_summary(self):
        """Get fleet info for display."""
        return [
            {
                "id": inst.id,
                "name": inst.name,
                "cpu": inst.cpu,
                "memory": inst.memory,
                "requests": inst.requests,
                "status": inst.status,
                "health": inst.health,
            }
            for inst in self.instance_fleet
        ]

    def record_snapshot(self):
        """Record current metrics for history charts."""
        self.history_cpu.append(round(self.cpu_usage, 1))
        self.history_memory.append(round(self.memory_usage, 1))
        self.history_instances.append(self.instances)
        self.history_users.append(self.active_users)
        self.history_timestamps.append(time.time())

        if len(self.history_cpu) > 100:
            self.history_cpu = self.history_cpu[-100:]
            self.history_memory = self.history_memory[-100:]
            self.history_instances = self.history_instances[-100:]
            self.history_users = self.history_users[-100:]
            self.history_timestamps = self.history_timestamps[-100:]


def get_state():
    if "system_state" not in st.session_state:
        st.session_state["system_state"] = SystemState()
    return st.session_state["system_state"]
