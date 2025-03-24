import random
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

                    repetition = ""
                    if j < len(regex_str) and regex_str[j] in "*+?²³⁴⁵⁶⁷⁸⁹":
                        repetition = regex_str[j]
                        j += 1

                    tokens.append(f"({group_content}){repetition}")
                    i = j
                else:
                    tokens.append(regex_str[i])
                    i += 1
            elif i < len(regex_str) - 1 and regex_str[i + 1] in "*+?²³⁴⁵⁶⁷⁸⁹":
                tokens.append(f"{regex_str[i]}{regex_str[i + 1]}")
                i += 2
            else:
                tokens.append(regex_str[i])
                i += 1

        return tokens

    def _process_tokens(self, tokens: List[str]) -> List[str]:
        results = [""]

        for token in tokens:
            new_results = []

            if token.startswith('(') and token.endswith(')'):
                group_content = token[1:-1]
                if '|' in group_content:
                    alternatives = group_content.split('|')
                    alt = random.choice(alternatives)
                    alt_results = self._process_tokens(self._tokenize(alt))
                    for r in results:
                        for alt_r in alt_results:
                            new_results.append(r + alt_r)
                else:
                    group_results = self._process_tokens(self._tokenize(group_content))
                    for r in results:
                        for gr in group_results:
                            new_results.append(r + gr)

            elif token.startswith('(') and any(
                    token.endswith(op) for op in ["²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "*", "+", "?"]):
                repeat_op = token[-1]
                group_content = token[1:-2]

                if repeat_op == '*':
                    repeat_count = random.randint(0, self.max_star_repeat)
                elif repeat_op == '+':
                    repeat_count = random.randint(1, self.max_plus_repeat)
                elif repeat_op == '?':
                    repeat_count = random.randint(0, 1)
                else:
                    repeat_count = {"²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}[repeat_op]

                if '|' in group_content:
                    alternatives = group_content.split('|')
                    choice = random.choice(alternatives)

                    group_results = self._process_tokens(self._tokenize(choice))

                    for r in results:
                        temp = r
                        for _ in range(repeat_count):
                            if group_results:
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
                char = token[0]
                repeat_count = {"²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}[token[1]]
                for r in results:
                    new_results.append(r + char * repeat_count)

            elif len(token) == 2 and token[1] == '*':
                char = token[0]
                repeat_count = random.randint(0, self.max_star_repeat)
                for r in results:
                    new_results.append(r + char * repeat_count)

            elif len(token) == 2 and token[1] == '+':
                char = token[0]
                repeat_count = random.randint(1, self.max_plus_repeat)
                for r in results:
                    new_results.append(r + char * repeat_count)

            elif len(token) == 2 and token[1] == '?':
                char = token[0]
                repeat_count = random.randint(0, 1)
                for r in results:
                    new_results.append(r + char * repeat_count)

            elif token == 'μ':
                new_results = results

            else:
                for r in results:
                    new_results.append(r + token)

            results = new_results

        return results

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

if __name__ == "__main__":
    generator = RegexGenerator(max_star_repeat=3, max_plus_repeat=4)

    patterns = [
        "M?N²(O|P)³Q*R+",
        "(X|Y|Z)³8+(9|0)",
        "(H|i)(J|K)L*N?"
    ]

    valid_strings = generator.generate(patterns, 3)