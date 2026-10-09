import re


TOPIC_RULES = {
    "Data Structures": [
        "stack", "queue", "linked list", "tree", "binary search tree",
        "heap", "hash", "graph traversal"
    ],
    "Algorithms": [
        "algorithm", "complexity", "sorting", "searching", "greedy",
        "dynamic programming", "divide and conquer", "recurrence"
    ],
    "Operating Systems": [
        "process", "thread", "deadlock", "semaphore", "paging",
        "page replacement", "virtual memory", "scheduling"
    ],
    "Computer Networks": [
        "tcp", "udp", "ip address", "subnet", "routing", "ethernet",
        "network", "protocol", "congestion"
    ],
    "DBMS": [
        "database", "sql", "transaction", "normalization", "relation",
        "relational", "candidate key", "primary key"
    ],
    "Computer Organization": [
        "cache", "pipeline", "cpu", "instruction", "register",
        "memory", "addressing mode", "assembly"
    ],
    "Theory of Computation": [
        "automata", "finite automaton", "dfa", "nfa", "regular language",
        "context-free", "pushdown", "turing machine"
    ],
    "Compiler Design": [
        "compiler", "lexical", "parser", "parsing", "grammar",
        "intermediate code", "syntax tree"
    ],
    "Digital Logic": [
        "boolean", "logic gate", "flip-flop", "multiplexer",
        "counter", "circuit", "k-map", "karnaugh"
    ],
    "Computer Graphics": [
        "pixel", "raster", "line drawing", "transformation",
        "bezier", "polygon"
    ],
    "Discrete Mathematics": [
        "proposition", "predicate", "logic", "set", "relation",
        "function", "graph theory", "combinatorics", "probability"
    ],
    "Engineering Mathematics": [
        "matrix", "determinant", "eigenvalue", "calculus",
        "derivative", "integral", "differential equation"
    ],
}


def classify_topic(question_text: str, current_topic: str = "") -> str:
    if current_topic and current_topic.lower() != "unclassified":
        return current_topic

    text = question_text.lower()

    scores = {}

    for topic, keywords in TOPIC_RULES.items():
        score = 0

        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                score += 1

        if score:
            scores[topic] = score

    if not scores:
        return "Unclassified"

    return max(scores, key=scores.get)
