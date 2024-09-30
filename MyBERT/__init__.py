# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The code is already compatible with Python 3.11 as it contains only comments and no executable code.
# If there were executable code, we would ensure compatibility with Python 3.11 by using features like
# fine-grained error locations in tracebacks, which is a new feature in Python 3.11.

# Example of handling multiple exceptions using exception groups in Python 3.11
try:
    # some code that may raise multiple exceptions
    pass
except* (ValueError, TypeError) as e:
    # handle ValueError and TypeError exceptions
    e.add_note("Handling ValueError and TypeError exceptions.")
    pass
except* Exception as e:
    # handle other exceptions
    e.add_note("Handling other exceptions.")
    pass

# Example of using the Self type for accurate type hints in class methods
from typing import Self, LiteralString

class ExampleClass:
    def __init__(self, value: int):
        self.value = value

    def increment(self) -> Self:
        self.value += 1
        return self

    def decrement(self) -> Self:
        self.value -= 1
        return self

# Example of using LiteralString for constrained string literals
def process_string(input_string: LiteralString) -> str:
    # Process the input string in some way
    return input_string.upper()
