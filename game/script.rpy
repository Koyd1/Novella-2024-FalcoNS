### Config to change brightness (might be moved in different file)
# init python:
#     def show(*args, **kwargs):
#         renpy.show(*args, **kwargs)

#     def ShowWithBrightness(*args, **kwargs):
#         if not "at" in kwargs:
#             kwargs["at_list"] = []
#         kwargs["at_list"].append(bright)
#         renpy.show(*args, **kwargs)

#     config.show = ShowWithBrightness
    # def func():
    #     renpy.retain_after_load()

    # config.after_load_callbacks.append(func)

### Config to store variable info in savefiles
init python:

    chapter = "Chapter Zero"
    location = "1st Location"

    def save_add_info(data):
        data["chapter"] = chapter
        data["location"] = location
    
    config.save_json_callbacks = [save_add_info]

### Characters
define mc = Character("Джеки Картер")
define mc_thoughts = Character("Мысли Джеки")
define julie = Character("Джуди")

define persistent.chapters = []

define chapter1_locs1 = [
    [839, 77, "Дом родителей",True, locations["Дом родителей"], True],
    [570, 230, "Дом Леони\nДжонс", False, None, True],
    [769, 405, "Ресторан на\nБлинк-роуд", False, None, True],
    [634, 600, "Дом на\nАрмори-стрит 19", False, None, True],
    [1115, 154, "Больница", True, locations["Больница"], True],
    [1273, 275, "Полиция", False, None, True],
    [1604, 260, "Дом на\nМарч-драйв 77", False, None, True],
    [1291, 549, "Университет", True, locations["Университет"], True]
]

define chapter1_locs2 = [
    [839, 77, "Дом родителей",False, None, True],
    [570, 230, "Дом Леони\nДжонс", True, locations["Дом родителей"], False],
    [769, 405, "Ресторан на\nБлинк-роуд", True, locations["Дом родителей"], True],
    [634, 600, "Дом на\nАрмори-стрит 19", True, locations["Дом родителей"], True],
    [1115, 154, "Больница", False, None, True],
    [1273, 275, "Полиция", False, None, True],
    [1604, 260, "Дом на\nМарч-драйв 77", True, locations["Дом родителей"], True],
    [1291, 549, "Университет", False, None, True]
]

### Splash screen and start screen
image black = "#000"
image white = "#ffffff"
image logo = "gui/MainMenu/splash.png"

transform halfed:
    zoom 0.6
    xalign 0.5

transform transform_logo:
    on show:
        alpha 0 xalign 0.5 yalign 0.5
        linear 2.0 alpha 1
    on hide:
        linear 2.0 alpha 0

# label splashscreen:
#     # python:
#     #     config.show = show

#     scene black 
#     $ renpy.pause(1, hard=True) 
    
#     show logo at transform_logo
#     $ renpy.pause(4, hard=True) 
    
#     hide logo 
#     $ renpy.pause(2, hard=True)
    
#     # python:
#     #     config.show = ShowWithBrightness

#     return

label before_main_menu:

    call screen press_to_start_game with dissolve


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

# The game starts here.

label start:

    $ unlock_achievement( "acquaintances", "1.1", "Вы получили досижение!")

    scene bg room

    show eileen happy

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    e "Я заметила, что Х ведет себя странно, он уже два дня не разговаривает со мной. Сегодня он оставил свой бумажник на столе, при том что обычно не забывает свои вещи... Может у него что-то случилось и он боится сказать?"

    "Andrew added this text for initial commit in his branch."

    menu(screen="choice_arrows"):
        "Будешь в форт"
        "Конечно пошли" (arrow_down=False):
            "Красава"
        "Нет, не иду" (arrow_down=True):
            "Нет, идешь"

    menu:
        "You have a choice!"
        "Choice 1":
            "Text for choice 1"
        "Choice 2":
            "Text for choice 2"

    menu:
        "Choice with 3 options!"
        "Choice 1":
            "Text for choice 1"
        "Choice 2":
            "Text for choice 2"
        "Choice 3":
            "Text for choice 3"

    menu:
        "Choice with 4 options here!"
        "Choice 1":
            "Text for choice 1"
        "Choice 2":
            "Text for choice 2"
        "Choice 3":
            "Text for choice 3"
        "Choice 4":
            "Text for choice 4"
    
    $ quick_menu = False
    call screen Map(chapter1_locs1)
    
    jump chapter_1

label chapter_1:
    $ quick_menu = True
    $ chapter = "Chapter One"
    $ location = "2nd Location"
    if "Chapter 1" not in persistent.chapters:
        $ persistent.chapters.append("Chapter 1")
    "Убийство молодой студентки: Джейн Лоуренс, 22 года. 
    Тело найдено на берегу реки прохожей пожилой женщиной, выгуливающей собаку.
    Согласно первоначальной версии, это несчастный случай либо суицид, но руки жертвы покрыты жуткими порезами, 
    поэтому дело предстоит раскрыть."

    $ quick_menu = False
    call screen Map(chapter1_locs1)
    
    return

label university:

    scene univ_front
    mc_thoughts "Не нужно быть гением криминалистики, чтоб знать о том, что если хочешь узнать что угодно о ком угодно - найди самую тихую и неприметную девочку. Нет более качественных хранителей сплетен в старшей школе, чем они."    
    
    scene univ_hall
    mc "Извините, мисс?"
    show julie at halfed
    "???" "Вы кто?"
    mc "Спецагент Картер, отдел уголовных расследований ФБР. Как я могу к Вам обращаться?"
    julie "Джули."
    julie "Я знаю, почему Вы здесь."
    mc "О чем Вы?"
    julie "Вы не первый, кто спрашивает о Лоуренс. От нее избавились. Весь курс об этом говорит."
    mc_thoughts "По-моему, я не говорил/а о том, что это не несчастный случай и не суицид"
    
    menu:
        "Избавились":
            julie "От этой заносчивой занозы только глухой не слышал оскорблений в свой адрес. Ее гордая мамашка внушила ей, что она королева красоты, и что больше ничего в этой жизни неважно. А деньги папочки только усиливали их веру в это. Две куклы"
            jump univ_fe
        "Что Вы знаете об этом?":
            julie "Что желающих было предостаточно. Таких выскочек давно не было. Будь у меня побольше свободного времени, повод и хорошее алиби, я бы тоже с ней расправилась"
            jump univ_fe

label univ_fe:
    menu:
        "Вы не сильно любили мисс Лоуренс, судя по всему":
            julie "Никто ее не любил. С ней общались только из-за денег и популярности. Ее отец покупал ей места на конкурсах, лишь бы его стервозная жена реализовала свои несбывшиеся амбиции через дочь и не трогала его. Даже Мисс Университет он ей купил, хотя были девочки, которые мечтали об этом чертовом кольце не меньше, чем она, и были достойнее ее."
            julie "Кольцо Мисс Университет. Это пропуск на конкурс Мисс Штат. Девочки боролись за титул ради стипендии, чтобы помочь родителям с оплатой учебы. А Лоуренсы хотели потешить свое самолюбие. Неудивительно, что шли разговоры о том, чтоб отравить ее."
            mc "Что случается с титулом, если победительница не может исполнять свои обязанности?"
            julie "Титул переходит вице-мисс."
            mc "Кто стал вице-мисс?"
            julie "Леони Джонс"
            jump univ_rs
        "Был ли кто-то, кто особенно не любил Джейн?":
            julie "Она перешла дорогу почти каждой девушке здесь. Парни смотрят только за ее юбкой, а на обычных девочек всем все равно. "
            julie "Но если выбирать одну, то я бы назвала Леони Джонс. Лоуренс украла у нее звание Мисс Университет. Леони стала вице-мисс, хотя она была достойна этого кольца гораздо больше. Просто у нее не такой богатый папа."            
            mc "О каком кольце Вы говорите?"
            julie "Кольцо Мисс Университет. Это пропуск на конкурс Мисс Штат. Девочки боролись за титул ради стипендии, чтобы помочь родителям с оплатой учебы. А Лоуренсы хотели потешить свое самолюбие."
            jump univ_rs

label univ_rs:
    mc "Она состояла с кем-то в отношениях?"
    julie "Проще сказать с кем она не состояла в отношениях. Хотя ладно, были эти несчастные парниши, которые влюблялись в эту путышку и тащились за ней везде, начиная со школы. Но они были слишком небогаты и некрасивы для куколки, и куколка их игнорировала"
    mc "Вы знаете, что она делала в день смерти?"
    julie "Почему всем это так интересно?"
    mc_thoughts "Всем? Кто-то еще интересовался этим?"
    julie "Собиралась со своим хахалем в ресторан на Блинк-роуд. Наследник папиного бизнеса - всё как она любит. Велик ей не нравится, подавай Роллс-Ройс. Жалко парня, передайте ему привет, если будете допрашивать."
    mc_thoughts "Ладно, она еще и любительница метафор."
    mc "Вы знаете, где можно найти ее молодого человека?"
    julie "Армори-стрит 19, но за дополнительную плату и не такое найду"
    mc_thoughts "Похоже мне стоит опасаться, что я ей сказал/а, как меня зовут."
    mc "Спасибо, сэкономлю и поручу кибер-отделу."
    julie "Многое теряете, босс."
    mc_thoughts "О, а вот и тот, о ком мы говорили!"
    "В конце коридора направляется к выходу из здания щуплый кучерявый парниша лет 20 с небольшим."
    menu: 
        "Стойте, сэр! Я из ФБР, нам нужно поговорить.":
            "Парень, не оборачиваясь, ускоряет шаг и выходит из здания"
            mc_thoughts "ГГ: Черт, он либо глухой, либо что-то знает. Ну ничего, увидимся на Армори-стрит"
            mc "Спасибо за помощь следствию, мисс."
            julie "Не забудьте передать привет."
            $ clearDict(directions)
            call screen Map(chapter1_locs2)
        "Я еще успею с ним общаться в более подходящей обстановке":
            mc "Спасибо за помощь следствию, мисс."
            julie "Не забудьте передать привет."
            $ clearDict(directions)
            call screen Map(chapter1_locs2)

label hospital:
    "Hospital label"

label parents_house:
    "Parents house label"


label chapter_2:
    $ chapter = "Chapter Two"
    $ location = "3rd Location"
    if "Chapter 2" not in persistent.chapters:
        $ persistent.chapters.append("Chapter 2")
    "This is chapter 2"
    "Congrats."
    return 

label chapter_3:
    "This is chapter 3"
    "Congrats."
    return 

label chapter_4:
    "This is chapter 4"
    "Congrats."
    return 