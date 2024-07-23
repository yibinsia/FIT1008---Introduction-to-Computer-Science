import abc

from data_structures.referential_array import ArrayR
from data_structures.array_sorted_list import ArraySortedList
from data_structures.stack_adt import ArrayStack
from data_structures.sorted_list_adt import ListItem
import math
class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        # Initialize the statistics for attack, defense, speed, and max HP
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp

    def get_attack(self):
        # Return the attack statistic
        return self.attack

    def get_defense(self):
        # Return the defense statistic
        return self.defense

    def get_speed(self):
        # Return the speed statistic
        return self.speed

    def get_max_hp(self):
        # Return the max HP statistic
        return self.max_hp
    
class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    def evaluate_expression(self, expression: ArrayR[str], level: int):
        """
        Evaluate a mathematical expression written in postfix notation.
        The time complexity of this function depends on the number of tokens in the expression array, denoted by n.
        In the worst-case, the function performs a constant number of operations (push, pop, arithmetic, etc.).
        for each of the n tokens in the expression. Therefore, the worst-case time complexity of this function is O(n).
        It's also O(n) at best, because even if the function encounters a short circuit condition
        (e.g. early return due to simple expressions), each token must still be traversed at least once.
        """
        stack = ArrayStack(len(expression))
        operators = {'+', '-', '*', '/', 'level', 'power', 'sqrt', 'middle'}

        for token in expression:
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()): # Check if the current token is a valid operand (integer or negative integer) in the postfix expression.
                stack.push(int(token))
            elif token in operators: # Performs every operations in the operators.
                if token == 'level':
                    stack.push(level)
                elif token == 'power':
                    b = stack.pop()
                    a = stack.pop()
                    stack.push(int(math.pow(a, b)))
                elif token == 'sqrt':
                    a = stack.pop()
                    stack.push(int(math.sqrt(a)))
                elif token == 'middle':
                    c = stack.pop()
                    b = stack.pop()
                    a = stack.pop()
                    sorted_values = ArraySortedList(3)
                    sorted_values.add(ListItem(a, a))
                    sorted_values.add(ListItem(b, b))
                    sorted_values.add(ListItem(c, c))
                    stack.push(sorted_values[1].value) # Push the middle value among the three.
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if token == '+':
                        stack.push(a + b)
                    elif token == '-':
                        stack.push(a - b)
                    elif token == '*':
                        stack.push(a * b)
                    elif token == '/':
                        stack.push(a // b)  
        return stack.pop()
    
    def get_attack(self, level: int):
        """
        Calculate the complex attack stats.
        The time complexity of this function is same with function evaluate_expression,
        because the stats calculated in evaluate_expression.
        """
        return self.evaluate_expression(self.attack_formula, level)

    def get_defense(self, level: int):
        """
        Calculate the complex defense stats.
        The time complexity of this function is same with function evaluate_expression,
        because the stats calculated in evaluate_expression.
        """
        return self.evaluate_expression(self.defense_formula, level)

    def get_speed(self, level: int):
        """
        Calculate the complex speed stats.
        The time complexity of this function is same with function evaluate_expression,
        because the stats calculated in evaluate_expression.
        """
        return self.evaluate_expression(self.speed_formula, level)

    def get_max_hp(self, level: int):
        """
        Calculate the complex maximum hp stats.
        The time complexity of this function is same with function evaluate_expression,
        because the stats calculated in evaluate_expression.
        """
        return self.evaluate_expression(self.max_hp_formula, level)

