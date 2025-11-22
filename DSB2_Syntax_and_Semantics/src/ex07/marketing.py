import sys

def list_to_set(l):
    return set(l)
#Клиенты, не видевшие рекламу
def call_center(clients, recipients):
    return list(list_to_set(clients) - list_to_set(recipients))
#Участники, но не клиенты
def potential_clients(participants, clients):
    return list(list_to_set(participants) - list_to_set(clients))
#Клиенты, но не участники
def loyalty_program(clients, participants):
    return list(list_to_set(clients) - list_to_set(participants))

def marketing():
    #Клиенты
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
    #Участники мероприятий + мб клиенты
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    #Клиенты, видевшие рекламу
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']


    if len(sys.argv) != 2:
        sys.exit()

    task = sys.argv[1]

    if task == 'call_center':
        result = call_center(clients, recipients)
    elif task == 'potential_clients':
        result = potential_clients(participants, clients)
    elif task == 'loyalty_program':
        result = loyalty_program(clients, participants)
    else:
        raise ValueError("Неправильный аргумент")

    for email in sorted(set(result)):
        print(email)

if __name__ == '__main__':
    marketing()