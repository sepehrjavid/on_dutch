from random import choice
import networkx as nx
import matplotlib.pyplot as plt


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

    @staticmethod
    def get_maximum_negative_must_pay() -> "Person":
        maximum = Person.people[0]
        for person in Person.people:
            if person.must_pay < 0 and person.must_pay < maximum.must_pay:
                maximum = person

        return maximum

    @staticmethod
    def get_minimum_positive_must_pay() -> "Person":
        minimum = Person.people[0]
        for person in Person.people:
            if 0 < person.must_pay < minimum.must_pay:
                minimum = person

        return minimum


def parse_input():
    number_of_people = int(input("How many people are involved?"))
    for i in range(number_of_people):
        person = input(f"Enter the {i + 1}th person's name and the money paid (name, paid):")
        Person.add_person(person.split(',')[0], int(person.split(',')[1]))


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


if __name__ == '__main__':
    parse_input()
    calculate_must_pay()
    model = create_model()
    flow_cost, flow_dict = nx.network_simplex(model)
    print(flow_dict)
    nx.draw_circular(model, with_labels=True)
    plt.show()
