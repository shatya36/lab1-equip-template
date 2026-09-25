"""Экипировка. Здесь ты пишешь новую систему.

Классы Item и Player трогать не надо: их держит остальной сервер, и менять
поля нельзя. Твоя работа — три функции внизу.
"""

SLOTS = ("head", "body", "right_hand", "left_hand", "ring_1", "ring_2")
# Не отдельное хранилище: просто два ключа из SLOTS, чтобы не писать их руками.
HANDS = ("right_hand", "left_hand")


class Item:
    """Вещь. Класс достался от старой системы."""

    def __init__(self, name, slot, power=0, durability=100, level_req=1,
                 two_handed=False):
        self.name = name
        self.slot = slot
        self.power = power
        self.durability = durability
        self.level_req = level_req
        self.two_handed = two_handed

    def __bool__(self):
        # Валера: «удобно же — if item: значит вещь целая»
        return self.durability > 0

    def __repr__(self):
        return f"<{self.name} {self.slot} dur={self.durability}>"


class Player:
    def __init__(self, name, level=1, inventory=None, capacity=20):
        self.name = name
        self.level = level
        self.inventory = list(inventory) if inventory else []
        self.capacity = capacity
        self.slots = {slot: None for slot in SLOTS}

    def __repr__(self):
        return f"<{self.name} lvl={self.level} inv={len(self.inventory)}>"


def equip(player, item) -> bool:
    """Надеть вещь из инвентаря. True — надели, False — не смогли."""

    if item.slot not in SLOTS:
        return False

    if player.level < item.level_req:
        return False

    if item not in player.inventory:
        return False
    #двуручка
    if item.two_handed:
        active_items = []
        for hand in HANDS:
            if player.slots[hand] is not None:
                active_items.append(player.slots[hand])

        if len(player.inventory) - 1 + len(active_items) > player.capacity:
            return False

        for old_item in active_items:
            player.inventory.append(old_item)

        player.slots["right_hand"] = item
        player.inventory.remove(item)
        player.slots["left_hand"] = None
        return True

    #соло амо
    active_items = []
    if item.slot in HANDS:
        for hand in HANDS:
            if (player.slots[hand] is not None) and (player.slots[hand].two_handed):
                active_items.append(player.slots[hand])
                break

        if len(active_items) == 0:
            if player.slots[item.slot] is not None:
                active_items.append(player.slots[item.slot])

    else:
        if player.slots[item.slot] is not None:
            active_items.append(player.slots[item.slot])

    if len(player.inventory) - 1 + len(active_items) > player.capacity:
        return False

    player.inventory.remove(item)

    for old_item in active_items:
        player.inventory.append(old_item)

    for old_item in active_items:
        if old_item.two_handed:
            player.slots["right_hand"] = None
            player.slots["left_hand"] = None

    player.slots[item.slot] = item
    return True

def unequip(player, slot) -> bool:
    """Снять вещь из слота в инвентарь. True — сняли, False — слот пуст."""

    if slot not in SLOTS:
        return False

    item = player.slots[slot]
    if item is None:
        return False

    if len(player.inventory) >= player.capacity:
        return False

    player.inventory.append(item)
    if item.two_handed:
        player.slots["right_hand"] = None
        player.slots["left_hand"] = None
    else:
        player.slots[slot] = None
    return True

def total_power(player) -> int:
    """Сила всех надетых вещей. Сломанная вещь даёт 0."""
    sum_power = 0
    for active_item in player.slots.values():
        if (active_item is not None) and active_item.durability >0:
            sum_power += active_item.power
        elif (active_item is not None) and active_item.durability ==0:
            sum_power += 0
        else: continue
    return sum_power



# Мне не нравится, что нет выбора при надевании двуручного оружияю мне отказали в этой операции если инвентарь забит и две руки заняты((((
# Не существенно
