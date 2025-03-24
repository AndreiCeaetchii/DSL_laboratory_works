import random
import argparse
from typing import List


class RegexGenerator:
    def __init__(self, max_iterations=1000, max_star_repeat=5, max_plus_repeat=5):
        self.max_iterations = max_iterations
        self.max_star_repeat = max_star_repeat
        self.max_plus_repeat = max_plus_repeat

    def parse_regex(self, regex_str: str) -> List[str]:
        tokens = self._tokenize(regex_str)
        valid_strings = self._process_tokens(tokens)
        return valid_strings

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

    def generate(self, regex_patterns: List[str], count: int = 1) -> List[str]:
        all_results = []
        pattern_results = {}

        # Generate strings for each pattern
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

        # Print results per pattern
        for pattern, results in pattern_results.items():
            print(f"Pattern: {pattern}")
            print(f"  {results}")

        return all_results

if __name__ == "__main__":
    generator = RegexGenerator(max_star_repeat=3, max_plus_repeat=4)

    # Patterns from the handwritten image
    patterns = [
        "M?N²(O|P)³Q*R+",
        "(X|Y|Z)³8+(9|0)",
        "(H|i)(J|K)L*N?"
    ]

    # Generate examples from each pattern
    valid_strings = generator.generate(patterns, 3)