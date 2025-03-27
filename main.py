import random
import matplotlib.pyplot as plt
from typing import List


TSLOTS = 100000


class ClassNode:
    def __init__(self, ttl: int):
        self.ttl = ttl 

    def tick(self) -> None:
        """Decrement TTL by 1."""
        self.ttl -= 1

    def reset_ttl(self, window_size: int) -> None:
        """Reset TTL to a random value between 0 and window_size."""
        self.ttl = random.randrange(0, window_size)


def simulate_slot_efficiency(window_size: int, num_nodes: int) -> float:
    """Simulate the slot efficiency for a given window size and number of nodes."""
    snode = [ClassNode(random.randrange(0, window_size)) for _ in range(num_nodes)]
    successful_slots = 0

    for slot in range(TSLOTS):
        transmitted_nodes = []

        for i in range(num_nodes):
            if snode[i].ttl == 0:
                transmitted_nodes.append(i)
                snode[i].reset_ttl(window_size)
            else:
                snode[i].tick()

        if len(transmitted_nodes) == 1:
            successful_slots += 1
        elif len(transmitted_nodes) > 1:
            for node in transmitted_nodes:
                snode[node].reset_ttl(window_size)

    return successful_slots / float(TSLOTS)


def plot_slot_efficiency():
    """Generate and plot slot efficiency for different window sizes and node counts."""
    random.seed()

    window_sizes = [8, 16, 32]
    Nlist: List[int] = []
    selist: List[float] = []

    for window_size in window_sizes:
        print(f"Window size: {window_size:2d}")

        for N in range(1, 33):
            slot_efficiency = simulate_slot_efficiency(window_size, N)
            print(f"N = {N:2d}: {slot_efficiency:.6f}")

            Nlist.append(N)
            selist.append(slot_efficiency)

        plt.plot(Nlist, selist, label=f'W = {window_size}')
        Nlist.clear()
        selist.clear()
        print("")

    plt.xlabel("# of Nodes")
    plt.ylabel("Slot Efficiency")
    plt.legend(loc='upper right')
    plt.axis([0, 32, 0, 1])
    plt.grid(linestyle='--')
    plt.show()


def main() -> None:
    """Main entry point for the simulation and plotting."""
    plot_slot_efficiency()


if __name__ == "__main__":
    main()
