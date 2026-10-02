"""Topic -> subtopic catalogue used for assessments, roadmaps and quizzes.

The MVP ships a rich catalogue for Machine Learning (the demo topic) plus a
reasonable default for any other topic the learner types in.
"""

from typing import Any

# Ordered by prerequisite so generated roadmaps stay sensible.
CURRICULUM: dict[str, list[str]] = {
    "machine learning": [
        "Python for ML",
        "NumPy",
        "Pandas",
        "Data preprocessing",
        "Supervised learning",
        "Regression",
        "Classification",
        "Clustering",
        "Model evaluation",
        "Decision Trees",
        "KNN",
        "Ensemble methods",
        "Feature engineering",
        "Model deployment",
    ],
    "data science": [
        "Python for Data Science",
        "NumPy",
        "Pandas",
        "Data cleaning",
        "Data visualisation",
        "Statistics for DS",
        "Data aggregation",
        "Introduction to ML",
        "Model evaluation",
        "Storytelling with data",
    ],
    "python": [
        "Python syntax",
        "Data types",
        "Control flow",
        "Functions",
        "Lists and dictionaries",
        "File handling",
        "Modules and packages",
        "Error handling",
        "OOP basics",
        "Virtual environments",
    ],
    "data structures": [
        "Arrays",
        "Linked lists",
        "Stacks and queues",
        "Trees",
        "Binary search trees",
        "Heaps",
        "Hashing",
        "Graphs",
        "Sorting algorithms",
        "Recursion",
    ],
    "deep learning": [
        "Neural network basics",
        "Activation functions",
        "Backpropagation",
        "Optimisers",
        "CNNs",
        "Transfer learning",
        "Regularisation",
        "Transformers",
    ],
    "data structures and algorithms": [
        "Arrays",
        "Linked lists",
        "Stacks and queues",
        "Trees",
        "Hashing",
        "Graphs",
        "Sorting algorithms",
        "Recursion",
        "Dynamic programming",
        "Greedy algorithms",
    ],
}

GENERIC_SUBTOPICS = [
    "Core concepts",
    "Key terminology",
    "Practical application",
    "Common tools",
    "Best practices",
    "Hands-on exercise",
    "Real-world case study",
    "Practice problems",
]

# Friendly aliases so "ml" or "Machine-Learning" both resolve.
ALIASES: dict[str, str] = {
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "machinelearning": "machine learning",
    "ds": "data science",
    "data-science": "data science",
    "deep-learning": "deep learning",
    "deeplearning": "deep learning",
    "dl": "deep learning",
    "dsa": "data structures and algorithms",
    "data-structures": "data structures",
    "data-structures-and-algorithms": "data structures and algorithms",
}


def normalise_topic(topic: str) -> str:
    key = topic.strip().lower()
    return ALIASES.get(key, key)


def subtopics_for(topic: str) -> list[str]:
    """Return an ordered subtopic list for any topic string."""
    key = normalise_topic(topic)
    return CURRICULUM.get(key, GENERIC_SUBTOPICS)


def is_known_topic(topic: str) -> bool:
    return normalise_topic(topic) in CURRICULUM


def display_name(topic: str) -> str:
    """Title-case a topic for UI display without mangling known names."""
    key = normalise_topic(topic)
    known = {
        "machine learning": "Machine Learning",
        "data science": "Data Science",
        "python": "Python",
        "data structures": "Data Structures",
        "deep learning": "Deep Learning",
        "data structures and algorithms": "Data Structures & Algorithms",
    }
    if key in known:
        return known[key]
    return topic.strip().title()


def topic_context_block(topic: str, limit: int = 8) -> dict[str, Any]:
    """Compact dict handed to the LLM so it knows the allowed subtopics."""
    return {"topic": display_name(topic), "subtopics": subtopics_for(topic)[:limit]}
