# Questão 1: Sequência de Fibonacci em Python

# Implemente uma função em Python chamada `fibonacci(n)` que retorna o n-ésimo termo da sequência de Fibonacci.

def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
def menu():
    n = int(input('Retornar o n-ésimo termo da sequência de Fibonacci: '))
    print(fibonacci(n))
while True:
    menu()