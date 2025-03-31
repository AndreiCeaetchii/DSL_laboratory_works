# Lexer & Scanner

### Course: Formal Languages & Finite Automata  
### Author: Andrei Ceaetchii

---

## Theory

Regular expressions, often abbreviated as **regex**, are powerful tools for pattern matching and text processing. Rooted in formal language theory, regexes are used to define regular languages and serve as a foundational concept in lexical analysis and compiler design.

### Understanding Regular Expressions

Regular expressions describe patterns composed of:

1. **Literal Characters**: Match themselves (e.g., `a` matches `a`)
2. **Metacharacters**: Have special meanings (e.g., `.` matches any character)
3. **Quantifiers**: Specify repetition (`*`, `+`, `?`, superscripts like `²`)
4. **Character Classes**: Match any character within `[]`
5. **Groups**: Parentheses group subpatterns
6. **Alternation**: The pipe symbol `|` provides "OR" logic

### Applications

Regexes are used in:

- **Search/replace tools**
- **Form input validation**
- **Lexical analysis in compilers**
- **Web URL routing**
- **Data extraction from text**
- **Log and event stream parsing**

---

## Objectives

1. Understand regex structure and behavior.
2. Implement a generator that outputs valid strings matching a given pattern.
3. Dynamically interpret regex, not hardcode results.
4. Limit repetitions of `*` and `+` to a max of 5.
5. Include processing step visualization for learning purposes.

---

## Implementation Description

### Overview

The project implements a `RegexGenerator` class capable of:
- Parsing regex patterns
- Tokenizing them
- Recursively generating valid strings based on interpreted rules

The core logic is split into:
1. **Tokenization**
2. **Processing**
3. **Generation**

---

### 1. The `RegexGenerator` Class

```python
class RegexGenerator:
    def __init__(self, max_iterations=1000, max_star_repeat=5, max_plus_repeat=5):
        self.max_iterations = max_iterations
        self.max_star_repeat = max_star_repeat
        self.max_plus_repeat = max_plus_repeat
```

- Controls max attempts per pattern
- Limits repetition for quantifiers like `*` and `+`

---

### 2. Tokenization Function

The `_tokenize()` function splits a regex string into meaningful tokens, such as:

- **Groups**: `(ab|cd)+`
- **Repetition modifiers**: `a*`, `b+`, `c?`, `d²`
- **Simple characters**: `x`, `y`, etc.

This prepares the regex for recursive evaluation.

---

### 3. Token Processing Function

The `_process_tokens()` function interprets the tokens and generates valid strings.

#### Key Logic (Simplified):

- **Literal characters**: Added to results directly
- **Character + Quantifier**: Repeated according to limits (e.g., `a+`, `b²`)
- **Groups**: `(abc)` processed recursively; supports quantifiers
- **Alternation**: `(a|b)` randomly selects one option
- **Empty string** (`μ`): Preserves current result
- **Recursion**: Ensures nested expressions are resolved fully

Instead of building an automaton, it simulates regex evaluation via recursive string construction.

---

### 4. Generation Function

```python
def generate(self, regex_patterns: List[str], count: int = 1) -> List[str]:
```

This method:
- Iterates through patterns
- Calls the parser and generator
- Generates multiple valid strings for each pattern
- Tracks attempts to avoid infinite loops

---

### Example Usage

```python
if __name__ == "__main__":
    generator = RegexGenerator(max_star_repeat=3, max_plus_repeat=4)
    patterns = [
        "M?N²(O|P)³Q*R+",
        "(X|Y|Z)³8+(9|0)",
        "(H|i)(J|K)L*N?"
    ]
    valid_strings = generator.generate(patterns, 3)
```

---

### Example Output

```
Pattern: M?N²(O|P)³Q*R+
  ['NNPPPQRR', 'NNOOORRR', 'NNPPPRRRR']
Pattern: (X|Y|Z)³8+(9|0)
  ['YYY888889', 'ZZZ8889', 'XXX88880']
Pattern: (H|i)(J|K)L*N?
  ['iJN', 'HKLLN', 'iKLLN']
```

---

## Conclusions

This project illustrates how regular expressions can be interpreted dynamically without relying on deterministic finite automata. Key insights:

1. Regex patterns can be broken into interpretable tokens.
2. Recursive processing enables flexible string generation.
3. Limiting quantifiers avoids excessive or infinite outputs.
4. This generator can help in testing, teaching, or prototyping regex-based tools.

---

## Bibliography

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation.
2. Friedl, J. (2006). Mastering Regular Expressions. O'Reilly Media.
3. Thompson, K. (1968). "Programming Techniques: Regular Expression Search Algorithm". Communications of the ACM.
4. Sipser, M. (2012). Introduction to the Theory of Computation.
5. Python documentation on Regular Expressions: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)