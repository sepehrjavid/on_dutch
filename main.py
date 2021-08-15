from random import choice
import networkx as nx


class InvalidInputException(Exception):
    def __init__(self, message):
        self.message = message


class Person:
    people = []

    def __init__(self, name, money_paid):
        self.name = name
        self.money_paid = money_paid
        self.must_pay = 0
        self.debts = {}

    @staticmethod
    def add_person(name, money_paid):
        Person.people.append(Person(name=name, money_paid=money_paid))

    @staticmethod
    def calculate_person_half():
        return round(sum([x.money_paid for x in Person.people]) / len(Person.people))


def parse_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()

    lines = ["".join(line.split()) for line in lines if line != '']
    people = []

    for line in lines:
        line_split = line.split(',')
        if not line_split[0]:
            raise InvalidInputException("Name cannot be blank!")
        try:
            paid = int(line_split[1])
        except ValueError:
            raise InvalidInputException("Paid value must be a number!")

        Person.add_person(line_split[0], paid)


def calculate_must_pay():
    person_half = Person.calculate_person_half()
    for person in Person.people:
        person.must_pay = person_half - person.money_paid

    zero_mean = sum([x.must_pay for x in Person.people])
    while zero_mean > 0:
        person = choice(Person.people)
        if person.must_pay > 0:
            person.must_pay -= 1
        zero_mean = sum([x.must_pay for x in Person.people])

    while zero_mean < 0:
        person = choice(Person.people)
        if person.must_pay >= 0:
            person.must_pay += 1
        zero_mean = sum([x.must_pay for x in Person.people])


def create_model():
    network_model = nx.DiGraph()

    for person in Person.people:
        if person.must_pay != 0:
            network_model.add_node(person.name, demand=-person.must_pay)

    for source_node in Person.people:
        if source_node.must_pay > 0:
            for dest_node in Person.people:
                if dest_node.must_pay < 0:
                    network_model.add_edge(source_node.name, dest_node.name, weight=1)

    return network_model


def display_output(flow_dict):
    for payer in flow_dict:
        for receiver in flow_dict[payer]:
            if flow_dict[payer][receiver] != 0:
                print(f"{payer} should pay {receiver} {flow_dict[payer][receiver]}")


if __name__ == '__main__':
    parse_input()
    calculate_must_pay()
    model = create_model()
    flow_cost, flow_dict = nx.network_simplex(model)
    display_output(flow_dict)
