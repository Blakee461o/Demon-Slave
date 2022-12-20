from random import random
import sys
import json

class Inventory:
    _node = 0
    _size = 0
    _visit_req = []
    _inventory_req = []  # 1 - Убийство демона, 2 - нож, 3 - ...

    def __init__(self):
        self.__used = [0] * self._node
        self.__inventory = [0] * self._size

    @classmethod
    def visit_req(
        cls,
        v: "Вершина, для которой задается требование",
        u: "Вершина, которую необходимо посетить",
    ):
        """Задает требование для посещения вершины"""
        if max(v, u) >= cls._node:
            raise IndexError("Такой вершины нет")
        cls._visit_req[v].append(u)

    @classmethod
    def inventory_req(
        cls,
        v: "Вершина, для которой задается требование",
        i: "Индекс предмета, который должен быть у игрока",
    ):
        """Задает требование для посещения вершины"""
        if v >= cls._node:
            raise IndexError("Такой вершины нет")
        if i >= cls._size:
            raise IndexError("Такого предмета нет")
        cls._inventory_req[v].append(i)

    def visit_add(self, v: "Индекс вершины"):
        """Добавляет вершину v в список посещенных"""
        if v >= self._node:
            raise IndexError("Такой вершины нет")
        self.__used[v] += 1

    def visit_check(self, v: "Индекс начальной вершины", u: "Индекс конечной вершины"):
        """Проверка на возможность пройти по ребру v->u учитывая посещенные вершины"""
        if u not in l[v]:
            return False
        for i in self._visit_req[u]:
            if not self.__used[i]:
                return False
        return True

    def visit_get(self, v: "Индекс вершины"):
        """Количество посешений вершины v"""
        if v >= self._node:
            raise IndexError("Такой вершины нет")
        return self.__used[v]

    def visit_get_all(self):
        """Список посещенности всех вершин"""
        return self.__used.copy()

    def inventory_add(self, i: "Индекс предмета в инвенторе"):
        """Добавление предмета с индексом i в инвентарь"""
        if i >= self._size:
            raise IndexError("Такого предмета нет")
        self.__inventory[i] += 1

    def inventory_check(
        self, v: "Индекс начальной вершины", u: "Индекс конечной вершины"
    ):
        """Проверка на возможность пройти по ребру v->u учитывая предметы инвенторя"""
        if u not in l[v]:
            return False
        for i in self._inventory_req[u]:
            if not self.__inventory[i]:
                return False
        return True

    def inventory_get(self, i: "Индекс предмета в инвенторе"):
        """Количество предметов с индексом i"""
        if i >= self._size:
            raise IndexError("Такого предмета нет")
        return self.__inventory[i]

    def inventory_get_all(self):
        """Инвентарь игрока"""
        return self.__inventory.copy()

    def check(self, v: "Индекс начальной вершины", u: "Индекс конечной вершины"):
        """Проверка на возможность пройти по ребру v->u"""
        return self.visit_check(v, u) and self.inventory_check(v, u)


Inventory._node = 30
Inventory._size = 3
Inventory._visit_req = [[] for _ in range(Inventory._node)]
Inventory._inventory_req = [[] for _ in range(Inventory._node)]


def edge(u, v):
    l[u].append(v)


def vreq(u, v):
    Inventory.visit_req(u, v)


def ireq(u, j):
    Inventory.inventory_req(u, j)


def go(v, u, i):
    return i.check(v, u)

texts = [        #Диалоги, которые мы отправляем игроку
    '''Вы открываете глаза и оглядываетесь. Комната, в которой вы оказались, очень
        темная, но вам точно не знакома. Вы садитесь на кровати, решая дождаться того
        момента, когда глаза привыкнут к темноте, а голова перестанет так сильно кружиться.
        В спальню из небольшого грязного окошка, криво забитого досками, проникает тусклый
        свет, видимо, сейчас ночь. Тем временем вы почувствовали, что в состоянии встать и
        осмотреть место, в которое вы попали...''', 
    '''Вы ложитесь обратно, закрываете глаза
        и, уже засыпая, слышите непонятный шум, источник которого, кажется, приближается к вам. 
        Убежать, да даже встать вы не успеете, кажется, это конец...''', 
    '''Вы встаёте и на ощупь 
        выходите из спальни, попадая на лестницу, как вдругслышите странный шум, доносящийся снизу, 
        из прихожей. Посмотрев туда, вы видите странное свечение и не менее странное, даже пугающее 
        существо, из него выходящее. Если бы вы не были так уверены в том, что демонов не существует, 
        вы бы точно сказали, что это он и есть.''', 
    '''Вы быстро забегаете обратно в спальню и 
        осматриваетесь в поисках укрытия...''', 
    '''Место под кроватью кажется вам наиболее 
        безопасным, и вы ныряете туда в надежде, что демон, а это ведь без сомнений именно он, 
        вас не найдет. К несчастью, зайдя в спальню, существо, даже не задумываясь, поднимает 
        старую кровать и находит вас...''', 
    '''Вы решаете забаррикадироваться, что, по вашему 
        мнению, обезопасит вас лучше всего. Только вот времени на это у вас оказывается слишком 
        мало, а потому существу явно демонического происхождения практически ничто не препятствует, 
        и оно уже очень скоро останавливается напротив вас...''', 
    '''Вы прячетесь в старый резной 
        шкаф, надеясь, что существо вас не найдет, и с замиранием сердца вслушиваетесь в приближающиеся 
        шаги. Через время шум начинает отдаляться, и вы понимаете, что демоническая сущность, кажется, ушла.
        Неужели вы спасены?''', 
    '''Вы осторожно открываете дверцу шкафа и, не обнаружив рядом демона,
        осторожно выходите и прокрадываетесь к лестнице. Куда делся ваш преследователь,
        вы не знаете, но точно уверены в том, что вскоре он вернётся, и у вас не так уж и
        много времени на спокойное обследование дома''', 
    '''Сойдя по шаткой лестнице вы отказываетесь
        в тесной неуютной прихожей, хотя, возможно, такой её делает этот светящийся и шипящий портал. 
        Тут вы замечаете неприметную дверь, из-за которой будто доносится неразборчивый шепот''', 
    '''Дверь не выделяет безопасно, да и этот тихий голос, разобрать который не представляется 
        возможным, пугает, и вы решаете обойти это место стороной. Тут портал позади вас вспыхивает, и 
        оттуда появляется уже знакомая вам лапа... Кажется, ещё немного, и от демона вас уже ничего не спасёт…''',
    '''Отбросив сомнения, вы забегаете в дверь и быстро захлопываете её и запирает на засов, так 
        удачно на ней оказавшийся. Кажется, даже если демон и вздумает вас тут искать, попасть сюда он не сможет''',
    '''Закрыв за собой дверь, вы осматриваетесь и успокаиваетесь. Помещение оказалось кухней, а 
        странное бормотание исходит от призрака, который даже выглядит вполне дружелюбно. На столе вперемешку 
        лежит несколько книг, а на стене напротив, кажется, что-то написано корявыми буквами…''',
    '''Что же вам теперь делать?''',
    '''Среди книг вы видите только кулинарные пособия и "Краткие советы о том, как изгнать демона"... Странный наборчик…''',
    '''Спустя некоторое время вам всё же удаётся разобрать, что написано на стене: "доживи до рассвета".
        Чтож, кажется, это именно то, что вам и нужно сделать…''',
    '''Набираясь смелости, вы подходите к призраку и здороваетесь, что сразу привлекает его внимание.
        Сущность перестает бормотать и, подлетая как можно ближе, начинает шептать, словно мантру, умоляя:
        "Помогите, помогите, спасите от этого демона! Он ведь меня и в посмертии не оставит!"... Вы уже начинаете 
        думать о том, как заткнуть это полоумное привидение, но тут оно резко замолкает и отлетает в противоположную часть комнаты''',
    '''Вы вновь подходите к призраку, и тот вдруг будто становится совершенно нормальным! Отчаяние в глазах, 
        граничащее с безумием, уходит, и привидение начинает рассказывать, как можно избавиться от демона, бродящего по дому. 
        Оказывается, нужно всего то встать перед ним и прочитать молитву на латыни, но какую... Язык сломаешь, пока выговоришь. 
        Слава богу, по словам призрака, на столе должна быть бумажка, на которой записан нужный текст''',
    '''Бумажка на столе действительно находится, и вы вчитываетесь, про себя проговаривая слова:
        "Exorcizamus te, omnis immundus spiritus, omnis satanica potestas, omnis incursio infernalis adversarii, omnis legio,
        omnis congregatio et secta diabolica, in nomine et virtute Domini Nostri Jesu" ''',
    '''Чтож, вы вновь в прихожей, и сейчас вам надо решить, что делать…''',
    '''Вы поднимаетесь наверх и оказываетесь в спальне. Что вы будете делать теперь?''',
    '''Чтож, раз вам нужно только дожить до рассвета, шкаф вам кажется наилучшим убежищем, ведь в шкафу демон вас 
        почему-то не чувствует. Вы забираетесь внутрь, закрываете дверцы и, устраиваясь поудобнее, засыпаете...
        Просыпаясь в своей кровати, вы теперь можете только гадать, сон это был, или реальность…''',
    '''Вы останетесь в коридоре, и задумываетесь, как бы привлечь внимание демона, чтобы поскорее от него избавиться''',
    '''Наконец, демон появляется и уже почти набрасывается на вас, когда вы встаёте и срывающимся голосом начинаете 
        читать молитву.. (далее в х. с тем самым шансом) иначе''',
    '''Наконец, демон появляется и уже почти набрасывается на вас, когда вы встаёте и срывающимся голосом начинаете 
        читать молитву.. (далее в х. с тем самым шансом) иначе''',
    '''Добравшись до середины, вы понимаете, что слова молитвы вылетели у вас из головы, и замолкаете... Демон отмирает,
        и уже в следующую секунду делает тот самый последний рывок…''',
    '''На последних словах демон начинает визжать и извиваться, а когда вы заканчиваете, и вовсе пропадает…''',
    '''Вас манит таинственный блеск портала, и вы заходите внутрь, оказываясь в пустоте, залитой белым светом. Кроме
        выхода обратно в дом, вы видите ещё три, которые ведут куда-то в неизведанные места... Куда же вы пойдете? Сквозь прорези порталов видно немногое:
        В одном, кажется, какая-то болотистая местность, во втором - горы, а в третьем и вовсе что-то алое с оранжевым, видимо, родина того самого демона''',
    '''Продолжение следует...''',
    '''Продолжение следует...''',
    '''Продолжение следует...''',
]

global l
global req
global t
global trev
global i

l = list()
req = dict()
t = []
trev = dict()
i = Inventory()

vreq(21, 17)
ireq(29, 0)

with open('Ways_Pre_game-2.txt', 'r') as fp:
    l = json.load(fp)
with open('Save.Pre_game_Morya.json', 'r') as fp:
    req = json.load(fp)
with open('button_save.json', 'r') as fp:
    t = json.load(fp)
with open('button_reverse_save.json', 'r') as fp:
    trev = json.load(fp)
req = {int(k): v for k, v in req.items()}
# print(*t, sep='\n')

r = 0
while r == 0:
    print("Напиши совой номер")
    try:
        client_id = int(input())
    except ValueError:
        pass
    else:
        r = 1

print("Напиши /restart")    
    
while(True):
    mes = input()
    if mes == "/restart":
        v = 0
        i = Inventory()
        print(texts[0])
        for j in l[v]:
            if go(v, j, i):
                print(t[v][j])
        print('Что будешь делать;)?')
        req[client_id] = [v, i.__dict__]
        open("Save.Pre_game_Morya.json", "w").write(json.dumps(req))

    else:
        try:
            u = trev[mes]
        except KeyError:
            print("Пиши правильно!")
            continue
        v  = req[client_id][0]
        i = Inventory()
        # print(v, u)
        i.__dict__ = req[client_id][1]
        if u not in l[v]:
            print("Пиши правильно!")
            continue
        if not go(v, u, i): 
            print("Ты не можешь это сделать!")
            continue
        print(texts[u])
        if u in [27, 28, 29]:
            print('Пошёл нафиг, никакого продолжения')
            print('Хочешь начать с начала?')
            continue

        if u == 25:
            i.inventory_add(0)

        if u == 22:
            if random() < 0.5:
                print(text=t[22][25])
            else:   
                print(text=t[22][24])
        elif u == 23:
            if random() < 0.95:
                print(text=t[23][25])
            else:   
                print(text=t[23][24])  
        else:  
            for j in l[u]:
                if go(u, j, i):
                    print(t[u][j])
        print('Что будешь делать;)?')
        req[client_id] = [u, i.__dict__]
        open("Save.Pre_game_Morya.json", "w").write(json.dumps(req))
