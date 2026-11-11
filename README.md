# Учет устройств (вариант 5)

Консольное приложение: добавление устройств с уникальным серийным номером.

    python inventory.py --file inventory.json add --name "Router" --serial SN-1
    python inventory.py --file inventory.json list
    python inventory.py --file inventory.json find --serial SN-1

Тесты: `python -m unittest discover -s tests -v`
