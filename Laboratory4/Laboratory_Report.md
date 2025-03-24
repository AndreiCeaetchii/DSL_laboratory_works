# Lexer & Scanner

### Course: Formal Languages & Finite Automata

### Author: Andrei Ceaetchii

## Theory

Regular expressions, often abbreviated as regex or regexp, are powerful pattern-matching tools used across various domains of computer science and software engineering. They provide a concise and flexible means to identify, match, and manipulate text patterns according to specific rules. Originating from the mathematical concept of regular languages in automata theory, regular expressions have evolved into an indispensable tool for text processing tasks.

### Understanding Regular Expressions

At their core, regular expressions describe patterns of characters. These patterns can range from simple literal matches to complex sequences with specialized meaning. Regular expressions are built using a combination of:

1. **Literal Characters**: Standard characters that match themselves (e.g., 'a' matches the character 'a')
2. **Metacharacters**: Special characters with predefined meanings (e.g., '.' matches any character)
3. **Quantifiers**: Symbols that specify how many instances of a character or group should be matched (e.g., '*' for zero or more, '+' for one or more)
4. **Character Classes**: Sets of characters enclosed in square brackets that match any single character within the set
5. **Grouping Constructs**: Parentheses that group parts of the expression together and capture matched subexpressions
6. **Alternation**: The pipe symbol '|' which acts as a boolean OR between alternatives

### Applications of Regular Expressions

Regular expressions are widely used for:

1. **Text Search and Manipulation**: Finding patterns within text or replacing specific patterns
2. **Input Validation**: Ensuring that user input conforms to expected formats (e.g., email addresses, phone numbers)
3. **Lexical Analysis**: Breaking down source code into tokens during the compilation process
4. **Data Extraction**: Identifying and extracting specific pieces of information from larger texts
5. **URL Routing**: Matching URL patterns in web applications
6. **Log Analysis**: Parsing and filtering log files for relevant information

### Regular Expressions and Formal Languages

In the context of formal languages and automata theory, regular expressions precisely define the set of strings that belong to a regular language. They correspond directly to finite automata, with every regular expression having an equivalent finite automaton that recognizes the same language. This theoretical foundation is what gives regular expressions their expressive power and makes them amenable to efficient implementations.

## Objectives

1. Understand the structure and interpretation of regular expressions.
2. Implement a generator that produces valid strings conforming to given regular expressions.
3. Develop a dynamic interpretation mechanism rather than hardcoding solutions.
4. Limit repetitions for indefinite quantifiers (*, +) to a maximum of 5 occurrences.
5. Create a function to demonstrate the sequence of processing steps for a regular expression.

## Implementation Description

### Overview of the Implementation

The implementation consists of a `RegexGenerator` class that can parse regular expressions and generate strings that match those patterns. The generator handles various regex constructs including character repetition, alternation (OR operations), and grouping.

The core functionality is divided into three main components:
1. **Tokenization**: Breaking down the regex pattern into meaningful tokens
2. **Processing**: Interpreting the tokens to generate valid strings
3. **Generation**: Creating multiple valid strings based on the processed patterns

### Key Components

#### 1. The RegexGenerator Class

```python
class RegexGenerator:
    def __init__(self, max_iterations=1000, max_star_repeat=5, max_plus_repeat=5):
        self.max_iterations = max_iterations
        self.max_star_repeat = max_star_repeat
        self.max_plus_repeat = max_plus_repeat
```

This class encapsulates all the functionality for processing regular expressions and generating valid strings. The parameters control:
- The maximum number of attempts to generate unique strings
- The upper limit for repetitions with the Kleene star operator (*)
- The upper limit for repetitions with the plus operator (+)

#### 2. Tokenization Function

```python
def _tokenize(self, regex_str: str) -> List[str]:
    tokens = []
    i = 0

    while i < len(regex_str):
        if regex_str[i] == '(':
            # Find matching closing parenthesis
            level = 1
            j = i + 1
            while j < len(regex_str) and level > 0:
                if regex_str[j] == '(':
                    level += 1
                elif regex_str[j] == ')':
                    level -= 1
                j += 1

            if level == 0:
                group_content = regex_str[i + 1:j - 1]

                # Check for repetition operators after the closing parenthesis
                repetition = ""
                if j < len(regex_str) and regex_str[j] in "*+?²³⁴⁵⁶⁷⁸⁹":
                    repetition = regex_str[j]
                    j += 1

                tokens.append(f"({group_content}){repetition}")
                i = j
            else:
                # Unmatched parenthesis, add as literal
                tokens.append(regex_str[i])
                i += 1
        elif i < len(regex_str) - 1 and regex_str[i + 1] in "*+?²³⁴⁵⁶⁷⁸⁹":
            # Character with *, +, ? or numeric repetition
            tokens.append(f"{regex_str[i]}{regex_str[i + 1]}")
            i += 2
        else:
            # Single character
            tokens.append(regex_str[i])
            i += 1

    return tokens
```

The tokenization function breaks down the regex pattern into tokens that can be processed. It handles:
- **Grouping**: Identifying groups enclosed in parentheses
- **Repetition Operators**: Recognizing characters followed by repetition symbols (*, +, ?, ², ³, etc.)
- **Simple Characters**: Processing individual characters that aren't part of special constructs

#### 3. Token Processing Function

```python
def _process_tokens(self, tokens: List[str]) -> List[str]:
    results = [""]

    for token in tokens:
        new_results = []

        if token.startswith('(') and token.endswith(')'):
            # Group without repetition
            group_content = token[1:-1]
            if '|' in group_content:
                # Alternative patterns
                alternatives = group_content.split('|')
                # Choose one alternative randomly
                alt = random.choice(alternatives)
                alt_results = self._process_tokens(self._tokenize(alt))
                for r in results:
                    for alt_r in alt_results:
                        new_results.append(r + alt_r)
            else:
                # Simple group
                group_results = self._process_tokens(self._tokenize(group_content))
                for r in results:
                    for gr in group_results:
                        new_results.append(r + gr)

        elif token.startswith('(') and any(
                token.endswith(op) for op in ["²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "*", "+", "?"]):
            # Group with repetition
            repeat_op = token[-1]
            group_content = token[1:-2]  # Remove '(', ')' and the repetition operator

            if repeat_op == '*':
                # Kleene star: 0 or more repetitions
                repeat_count = random.randint(0, self.max_star_repeat)
            elif repeat_op == '+':
                # Plus: 1 or more repetitions
                repeat_count = random.randint(1, self.max_plus_repeat)
            elif repeat_op == '?':
                # Question mark: 0 or 1 repetitions
                repeat_count = random.randint(0, 1)
            else:
                # Numeric repetition (²³⁴⁵⁶⁷⁸⁹)
                repeat_count = {"²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}[repeat_op]

            # Handle alternatives in group
            if '|' in group_content:
                alternatives = group_content.split('|')
                # Choose one alternative randomly
                choice = random.choice(alternatives)
                
                # Process the chosen alternative
                group_results = self._process_tokens(self._tokenize(choice))
                
                for r in results:
                    temp = r
                    for _ in range(repeat_count):
                        if group_results:
                            # Take just the first result for simplicity
                            temp += group_results[0]
                    new_results.append(temp)
            else:
                # Simple group
                group_results = self._process_tokens(self._tokenize(group_content))
                
                for r in results:
                    temp = r
                    for _ in range(repeat_count):
                        if group_results:
                            temp += group_results[0]
                    new_results.append(temp)

        elif len(token) == 2 and token[1] in "²³⁴⁵⁶⁷⁸⁹":
            # Single character with numeric repetition
            char = token[0]
            repeat_count = {"²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}[token[1]]
            for r in results:
                new_results.append(r + char * repeat_count)

        elif len(token) == 2 and token[1] == '*':
            # Kleene star operator on a single character
            char = token[0]
            repeat_count = random.randint(0, self.max_star_repeat)
            for r in results:
                new_results.append(r + char * repeat_count)

        elif len(token) == 2 and token[1] == '+':
            # Plus operator on a single character
            char = token[0]
            repeat_count = random.randint(1, self.max_plus_repeat)
            for r in results:
                new_results.append(r + char * repeat_count)
                
        elif len(token) == 2 and token[1] == '?':
            # Question mark operator - 0 or 1 occurrence
            char = token[0]
            repeat_count = random.randint(0, 1)
            for r in results:
                new_results.append(r + char * repeat_count)

        elif token == 'μ':
            # Empty string - just keep current results
            new_results = results

        else:
            # Single character or other literal
            for r in results:
                new_results.append(r + token)

        results = new_results

    return results
```

This function recursively processes the tokens to build valid strings. It handles:
- **Simple Characters**: Appending the character to all current partial results
- **Character with Repetition**: Repeating a character according to the specified operator
- **Groups**: Processing enclosed content, potentially with alternatives
- **Groups with Repetition**: Repeating the processed group content
- **Empty String (μ)**: Preserving the current results without modification

#### 4. String Generation Function

```python
def generate(self, regex_patterns: List[str], count: int = 1) -> List[str]:
    all_results = []
    pattern_results = {}
    for pattern in regex_patterns:
        pattern_strings = []
        iterations = 0
        
        while len(pattern_strings) < count and iterations < self.max_iterations:
            generated = self.parse_regex(pattern)
            if generated:
                pattern_strings.append(generated[0])  # Just take the first generated result
            iterations += 1
        
        pattern_results[pattern] = pattern_strings
        all_results.extend(pattern_strings)
    
    for pattern, results in pattern_results.items():
        print(f"Pattern: {pattern}")
        print(f"  {results}")
    
    return all_results
```

This function is responsible for generating a specified number of valid strings from each provided regex pattern. It:
- Iterates through each regex pattern
- Generates the requested number of strings for each pattern
- Keeps track of results by pattern
- Prevents infinite loops by limiting the number of generation attempts

This function provides a detailed explanation of how each token in the regex is interpreted and processed, making the internal workings of the generator more transparent.

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
    
    # Demonstrate processing sequence for one pattern
    generator.show_processing_sequence(patterns[0])
```

### Expected Output

When run, the program generates valid strings for each pattern and also shows the processing sequence if requested:

```
Pattern: N² (O|P)³ Q*R+
  ['NNPPPQRR', 'NNOOORRR', 'NNPPPRRRR']
Pattern: (X|Y|Z)³ 8+ (9|0)
  ['YYY888889', 'ZZZ8889', 'XXX88880']
Pattern: (H|i) (J|K) L*N?
  ['iJN', 'HKLLN', 'iKLLN']
```

## Conclusions

The implementation of a regular expression generator provides valuable insights into the structure and interpretation of regular expressions. By breaking down the process into tokenization, processing, and generation phases, we've created a system that can dynamically interpret a variety of regex patterns and produce valid matching strings.

Key takeaways from this implementation include:

1. Regular expressions can be systematically broken down into tokens representing literals, groups, repetitions, and alternatives.
2. The generation of valid strings involves recursive processing of these tokens, with special handling for various regex constructs.
3. Limiting the number of repetitions for quantifiers like * and + is essential to prevent the generation of excessively long strings.
4. Visualizing the processing sequence helps in understanding how regular expressions are evaluated.

This project demonstrates the practical application of formal language concepts and provides a tool that could be useful in various scenarios, such as testing pattern matching algorithms, generating test data, or educational purposes to illustrate regex behavior.

## Bibliography

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation.
2. Friedl, J. (2006). Mastering Regular Expressions. O'Reilly Media.
3. Thompson, K. (1968). "Programming Techniques: Regular Expression Search Algorithm". Communications of the ACM.
4. Sipser, M. (2012). Introduction to the Theory of Computation.
5. Python documentation on Regular Expressions: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)