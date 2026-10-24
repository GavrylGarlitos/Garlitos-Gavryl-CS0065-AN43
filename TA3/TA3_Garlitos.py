import json
from pathlib import Path

# Google Colab-compatible case database
CASE_FILE = Path("/content/cases.json")

# 1. CASE REPRESENTATION
# Five sample cases containing previous student problems and solutions.
INITIAL_CASES = [
    {
        "id": 1,
        "grade": 7,
        "topic": "fractions",
        "errors": ["wrong_denominator", "addition_rule"],
        "intervention": "Review fraction addition and practise with visual fraction bars.",
        "outcome": "Improved after guided examples."
    },
    {
        "id": 2,
        "grade": 8,
        "topic": "linear_equations",
        "errors": ["sign_error", "inverse_operation"],
        "intervention": "Practise inverse operations one step at a time and check signs.",
        "outcome": "Solved similar equations correctly."
    },
    {
        "id": 3,
        "grade": 7,
        "topic": "fractions",
        "errors": ["simplification", "wrong_denominator"],
        "intervention": "Use equivalent fractions and practise simplifying answers.",
        "outcome": "Made fewer fraction errors."
    },
    {
        "id": 4,
        "grade": 9,
        "topic": "algebra",
        "errors": ["sign_error", "like_terms"],
        "intervention": "Review positive and negative terms and combine like terms.",
        "outcome": "Improved accuracy in algebra exercises."
    },
    {
        "id": 5,
        "grade": 8,
        "topic": "fractions",
        "errors": ["multiplication_rule", "simplification"],
        "intervention": "Practise fraction multiplication and simplifying answers.",
        "outcome": "Correctly multiplied and simplified fractions."
    }
]

# Error patterns that users can select.
ERROR_OPTIONS = {
    "1": ("wrong_denominator", "Using the wrong denominator"),
    "2": ("addition_rule", "Incorrect fraction addition rule"),
    "3": ("simplification", "Difficulty simplifying fractions"),
    "4": ("sign_error", "Sign errors"),
    "5": ("inverse_operation", "Incorrect inverse operations"),
    "6": ("like_terms", "Combining unlike terms"),
    "7": ("multiplication_rule", "Incorrect fraction multiplication rule")
}


def save_cases(cases):
    """Save the case base to a JSON file."""
    with CASE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cases, file, indent=4)


def load_cases():
    """Load existing cases or initialize the five sample cases."""
    if not CASE_FILE.exists():
        save_cases(INITIAL_CASES)

    try:
        with CASE_FILE.open("r", encoding="utf-8") as file:
            cases = json.load(file)

        return cases if isinstance(cases, list) else INITIAL_CASES.copy()

    except (json.JSONDecodeError, OSError):
        print("Could not read cases.json. Loading starter cases.")
        return INITIAL_CASES.copy()


# 2. SIMILARITY ASSESSMENT
def similarity(new_case, old_case):
    """
    Calculate similarity from 0 to 100.

    Topic match: 30 points
    Same grade: 20 points
    One grade apart: 10 points
    Error-pattern similarity: up to 50 points
    """
    score = 0.0

    # Compare the math topics.
    if new_case["topic"] == old_case["topic"]:
        score += 30

    # Compare the grade levels.
    grade_difference = abs(
        new_case["grade"] - old_case["grade"]
    )

    if grade_difference == 0:
        score += 20
    elif grade_difference == 1:
        score += 10

    # Compare error patterns using Jaccard similarity.
    new_errors = set(new_case["errors"])
    old_errors = set(old_case["errors"])

    union = new_errors | old_errors
    intersection = new_errors & old_errors

    if union:
        error_similarity = len(intersection) / len(union)
    else:
        error_similarity = 1

    score += 50 * error_similarity

    return round(score, 1)


# 3. CASE ADAPTATION
def adapt_solution(new_case, retrieved_case):
    """Adapt a previous intervention to the new student's errors."""

    advice = [retrieved_case["intervention"]]

    specific_advice = {
        "wrong_denominator":
            "Find a common denominator before calculating.",

        "addition_rule":
            "Add numerators only after the denominators match.",

        "simplification":
            "Simplify the answer by dividing the numerator and denominator by a common factor.",

        "sign_error":
            "Double-check positive and negative signs at every step.",

        "inverse_operation":
            "Use the opposite operation to isolate the unknown.",

        "like_terms":
            "Combine only terms with the same variable and exponent.",

        "multiplication_rule":
            "Multiply numerators together and denominators together, then simplify."
    }

    # Add advice that matches the student's selected errors.
    for error in new_case["errors"]:
        if error in specific_advice:
            advice.append(specific_advice[error])

    topic = new_case["topic"].replace("_", " ")

    advice.append(
        f"Suggested plan for Grade {new_case['grade']} {topic}: "
        "review one worked example, solve three guided questions, "
        "then try two questions independently."
    )

    return " ".join(advice)


def ask_student_details():
    """Collect information about the new student case."""

    print("\n=== NEW STUDENT CASE ===")

    # Get a valid grade level.
    while True:
        try:
            grade = int(input("Student grade level (7-12): "))

            if 7 <= grade <= 12:
                break

            print("Please enter a grade from 7 to 12.")

        except ValueError:
            print("Please enter a whole number.")

    # Get the math topic.
    topic = input(
        "Math topic (e.g., fractions, linear_equations, algebra): "
    ).strip().lower()

    while not topic:
        topic = input("Topic cannot be blank. Enter a topic: ").strip().lower()

    # Display available error patterns.
    print("\nSelect the student's error pattern(s):")

    for key, (_, description) in ERROR_OPTIONS.items():
        print(f"{key}. {description}")

    # Allow multiple error patterns.
    while True:
        choices = [
            item.strip()
            for item in input(
                "Enter choices separated by commas (e.g., 1,3): "
            ).split(",")
        ]

        if choices and all(choice in ERROR_OPTIONS for choice in choices):
            choices = list(dict.fromkeys(choices))
            break

        print("Invalid input. Enter numbers from 1 to 7.")

    return {
        "grade": grade,
        "topic": topic,
        "errors": [
            ERROR_OPTIONS[key][0] for key in choices
        ],
        "error_choices": choices
    }


def main():
    # Load the case base.
    cases = load_cases()

    # Describe the new problem.
    new_case = ask_student_details()

    print("\n=== 1. CASE REPRESENTATION ===")
    print("Grade:", new_case["grade"])
    print("Topic:", new_case["topic"].replace("_", " "))

    print(
        "Errors:",
        ", ".join(
            ERROR_OPTIONS[key][1]
            for key in new_case["error_choices"]
        )
    )

    # 2. Calculate scores and retrieve the closest case.
    print("\n=== 2. SIMILARITY ASSESSMENT AND RETRIEVAL ===")

    ranked = sorted(
        [
            (similarity(new_case, case), case)
            for case in cases
        ],
        key=lambda item: item[0],
        reverse=True
    )

    # Display similarity rankings.
    for rank, (score, case) in enumerate(ranked, start=1):
        print(
            f"{rank}. Case {case['id']} | "
            f"Topic: {case['topic']} | "
            f"Similarity: {score:.1f}%"
        )

    best_score, best_case = ranked[0]

    print(
        f"\nRetrieved case: Case {best_case['id']} "
        f"({best_score:.1f}% similarity)"
    )
    print("Past intervention:", best_case["intervention"])
    print("Past outcome:", best_case["outcome"])

    # 3. Reuse and adapt the retrieved solution.
    print("\n=== 3. ADAPTED SOLUTION ===")

    adapted = adapt_solution(new_case, best_case)
    print(adapted)

    # 4. Retain the new case for future use.
    print("\n=== 4. LEARNING / RETENTION ===")

    next_id = max(
        (case.get("id", 0) for case in cases),
        default=0
    ) + 1

    retained_case = {
        "id": next_id,
        "grade": new_case["grade"],
        "topic": new_case["topic"],
        "errors": new_case["errors"],
        "intervention": adapted,
        "outcome": (
            "New case retained. Update this outcome "
            "after observing student progress."
        )
    }

    cases.append(retained_case)
    save_cases(cases)

    print(
        f"New case saved successfully as Case {next_id} "
        f"in {CASE_FILE}."
    )

    print(f"\nUpdated case base contains {len(cases)} cases:")

    for case in cases:
        print(
            f"Case {case['id']}: Grade {case['grade']} | "
            f"{case['topic']} | "
            f"Errors: {', '.join(case['errors'])}"
        )


# Start the program.
main()