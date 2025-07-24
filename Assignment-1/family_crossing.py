class State:
    def _init_(self, amogh, ameya, grandmother, grandfather, time, umbrella):
        self.amogh = amogh
        self.ameya = ameya
        self.grandmother = grandmother
        self.grandfather = grandfather
        self.time = time
        self.umbrella = umbrella

    def goalTest(self):
        return (self.amogh == self.ameya == self.grandmother == self.grandfather == 'R' and self.time <= 60)

    def isSafe(self):
        return self.time <= 60

    def moveGen(self):
        children = []
        persons = ["amogh", "ameya", "grandmother", "grandfather", None]
        times = {
            "amogh": 5,
            "ameya": 10,
            "grandmother": 20,
            "grandfather": 25
        }
        new_side = 'R' if self.umbrella == 'L' else 'L'

        for i in range(5):
            first = persons[i]
            if first and getattr(self, first) != self.umbrella:
                continue
            for j in range(i, 5):
                second = persons[j]
                if second and getattr(self, second) != self.umbrella:
                    continue

                # Copy current positions
                a, m, g, f, t, u = self.amogh, self.ameya, self.grandmother, self.grandfather, self.time, self.umbrella

                # Move first person
                if first == "amogh":
                    a = new_side
                elif first == "ameya":
                    m = new_side
                elif first == "grandmother":
                    g = new_side
                elif first == "grandfather":
                    f = new_side

                # Move second person
                if second == "amogh":
                    a = new_side
                elif second == "ameya":
                    m = new_side
                elif second == "grandmother":
                    g = new_side
                elif second == "grandfather":
                    f = new_side

                # Calculate trip time
                trip_time = 0
                if first and second:
                    trip_time = max(times[first], times[second])
                elif first:
                    trip_time = times[first]
                elif second:
                    trip_time = times[second]

                new_state = State(a, m, g, f, t + trip_time, new_side)

                if new_state.isSafe():
                    children.append(new_state)

        return children

    def _str_(self):
        return f"[Amogh:{self.amogh} Ameya:{self.ameya} Grandmother:{self.grandmother} Grandfather:{self.grandfather} Time:{self.time} Umbrella:{self.umbrella}]"

    def _eq_(self, other):
        return (self.amogh == other.amogh and
                self.ameya == other.ameya and
                self.grandmother == other.grandmother and
                self.grandfather == other.grandfather and
                self.time == other.time and
                self.umbrella == other.umbrella)

    def _hash_(self):
        return hash((self.amogh, self.ameya, self.grandmother, self.grandfather, self.time, self.umbrella))


def reconstructPath(node_pair, CLOSED):
    parent_map = {node: parent for node, parent in CLOSED}
    path = []
    node, parent = node_pair
    while node is not None:
        path.append(node)
        node = parent_map.get(node)
    return path[::-1]


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    return [node for node in children if node not in open_nodes and node not in closed_nodes]


def bfs(start):
    print("\n=== BFS ===")
    OPEN = [(start, None)]
    CLOSED = []

    while OPEN:
        node_pair = OPEN.pop(0)
        node, parent = node_pair

        if node.goalTest():
            print("Goal found")
            path = reconstructPath(node_pair, CLOSED)
            for p in path:
                print("->", p)
            return

        CLOSED.append(node_pair)
        children = node.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        OPEN.extend([(child, node) for child in new_nodes])

    print("Goal not found.")


def dfs(start):
    print("\n=== DFS ===")
    OPEN = [(start, None)]
    CLOSED = []

    while OPEN:
        node_pair = OPEN.pop(0)
        node, parent = node_pair

        if node.goalTest():
            print("Goal found")
            path = reconstructPath(node_pair, CLOSED)
            for p in path[::-1]:
                print("->", p)
            return

        CLOSED.append(node_pair)
        children = node.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        OPEN = [(child, node) for child in new_nodes] + OPEN

    print("Goal not found.")


# Starting state
if __name__ == "_main_":
    start_state = State('L', 'L', 'L', 'L', 0, 'L')
    bfs(start_state)
    dfs(start_state)