import collections

INPUT = '../inputs/day8.txt'
TEST_INPUT = '../inputs/day8_test.txt'

Node = collections.namedtuple('Node', 'id parent metadata_entries children')


def part1(root_node):
    return sum([sum(n.metadata_entries) for n in dfs(root_node)])


def dfs(node):
    yield node
    for c in node.children:
        for n in dfs(c):
            yield n


def part2(root_node):
    return get_value(root_node)


def get_value(node):
    if not node.children:
        return sum(node.metadata_entries)

    child_count = len(node.children)
    node_sum = 0
    for metadata in node.metadata_entries:
        if metadata <= child_count and metadata > 0:
            child = node.children[metadata - 1]
            node_sum += get_value(child)
    return node_sum


def parsefile(path):
    with open(path, mode='r') as data:
        nodes = data.read().rstrip().split(' ')
        root_node = parse_node(nodes, None, 0, 'A')
        return root_node


def parse_node(node_data, parent, index, node_id):
    child_count = int(node_data[index])
    metadata_count = int(node_data[index + 1])
    index += 2
    node = Node(node_id, parent, [], [])
    node_id = chr(ord(node_id) + 1)
    for _ in range(child_count):
        child = parse_node(node_data, node, index, node_id)
        node.children.append(child)
        index += get_node_length(child)
        node_id = chr(ord(node_id) + 1)
    for i in range(metadata_count):
        metadata = int(node_data[index + i])
        node.metadata_entries.append(metadata)
    return node


def get_node_length(node):
    length = len(node.metadata_entries) + 2
    for c in node.children:
        length += get_node_length(c)
    return length


if __name__ == '__main__':
    test_root_node = parsefile(TEST_INPUT)
    assert part1(test_root_node) == 138

    root_node = parsefile(INPUT)
    result1 = part1(root_node)
    print(result1)

    assert part2(test_root_node) == 66
    result2 = part2(root_node)
    print(result2)
