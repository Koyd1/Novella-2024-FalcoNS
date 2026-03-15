# ## Config to change brightness (might be moved in different file)
# init python:
#     def show(*args, **kwargs):
#         renpy.show(*args, **kwargs)

#     def ShowWithBrightness(*args, **kwargs):
#         if not "at" in kwargs:
#             kwargs["at_list"] = []
#         kwargs["at_list"].append(bright)
#         renpy.show(*args, **kwargs)

#     config.show = ShowWithBrightness
#     def func():
#         renpy.retain_after_load()

#     config.after_load_callbacks.append(func)

### Config to store variable info in savefiles
init python:

    chapter = "Chapter Zero"
    location = "1st Location"

    def save_add_info(data):
        data["chapter"] = chapter
        data["location"] = location
    
    def add_person_file_info(persons_file, image_path: str, description: str):
        persons_file.append({
        "image_path" : image_path, 
        "description" : description
        })

    config.save_json_callbacks = [save_add_info]


# Создание персонажей

### Characters
define mc= Character("Жаклин", image = "jaclyn")
define mc_thoughts = Character("Мысли Жаклин")
define govard = Character("Говард Браун", image="govard")
define phil = Character("Фил Моррисон", image="phil")
define casey = Character("Кейси Аронс", image= "casey")
define judy = Character("Джуди")
define mr_lawrence = Character("Мистер Лоуренс", image="mr_lawrence")    #text issue
define mrs_lawrence = Character("Миссис Лоуренс", image="mrs_lawrence")    #text issue
define dr_andrews = Character("Доктор Эндрюс", image="dr_andrews")     #text issue
define mrs_velaskez = Character("Миссис Веласкес", image="mrs_velaskez")    #text issue
define lisa = Character("Лиза", image="lisa")
define james = Character("Джеймс", image="james")
define kyle = Character("Кайл", image="kyle")

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
    [570, 230, "Дом Леони\nДжонс", True, locations["Дом Леони\nДжонс"], False],
    [769, 405, "Ресторан на\nБлинк-роуд", True, locations["Ресторан на\nБлинк-роуд"], True],
    [634, 600, "Дом на\nАрмори-стрит 19", True, locations["Дом на\nАрмори-стрит 19"], True],
    [1115, 154, "Больница", False, None, True],
    [1273, 275, "Полиция", False, None, True],
    [1604, 260, "Дом на\nМарч-драйв 77", True, locations["Дом на\nМарч-драйв 77"], True],
    [1291, 549, "Университет", False, None, True]
]
init python:
    def char_callback(tag):
        def callback(event, interact=True, **kwargs):
            if event == "show":
                renpy.show(tag, at_list=[sprite_centered, active])
                for other in ["mc", "govard", "phil", "casey"]:
                    if other != tag:
                        renpy.show(other, at_list=[sprite_left if other=="casey" else sprite_right, inactive], layer="master")
        return callback

### Splash screen and start screen
image black = "#000"
image white = "#ffffff"
image logo = "gui/MainMenu/splash.png"


### Transforms and positions
transform halfed:
    zoom 0.6
    xalign 0.5

transform halfed_left:
    zoom 0.6
    xalign 0.2

transform halfed_right:
    zoom 0.6
    xalign 0.8

transform transform_logo:
    on show:
        alpha 0 xalign 0.5 yalign 0.5
        linear 2.0 alpha 1
    on hide:
        linear 2.0 alpha 0

transform reduction:
    zoom 0.3
    yalign 1.0
    xalign 0.5

transform zoom_in:
    zoom 0.55
    yalign 1.0
    xalign 0.5

# transform reduction_left:
#     zoom 0.3
#     yalign 1.0
#     xalign 0.1

# Центрированный
transform sprite_centered:
    xalign 0.45
    yalign 1.0
    zoom 0.43

# Слева
transform sprite_left:
    xalign -0.1
    yalign 1.0
    zoom 0.43

# Справа
transform sprite_right:
    xalign 1.1
    yalign 1.0
    zoom 0.43
transform active:
    alpha 1.0
    linear 0.2 alpha 1.0

transform inactive:
    alpha 0.5
    linear 0.2 alpha 0.5

transform darken:
    # matrixcolor TintMatrix("#ffffff")*SaturationMatrix(1.0)
    linear 0.2 matrixcolor TintMatrix("#4e4e4e")*SaturationMatrix (1.0)

transform lighten:
    linear 0.2 matrixcolor TintMatrix("#ffffff")*SaturationMatrix(1.0)




label splashscreen:
    # python:
    #     config.show = show

    scene black 
    $ renpy.pause(1, hard=True) 
    
    play sound "sounds/splash_screen.mp3" fadein 1.0 fadeout 1.0 volume 0.5
    $ renpy.pause(0.8)
    show logo at transform_logo
    $ renpy.pause(4, hard=True) 
    
    hide logo 
    $ renpy.pause(2, hard=True)
    
    # python:
    #     config.show = ShowWithBrightness

    return

label before_main_menu:

    call screen press_to_start_game with dissolve


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

# The game starts here.

label start:
    # $ unlock_achievement( "acquaintances", "1.1", "Вы получили досижение!")
    jump chapter_1
    # scene bg room
    # show eileen happy
    # e "You've created a new Ren'Py game."
    # e "Once you add a story, pictures, and music, you can release it to the world!"
    # e "Я заметила, что Х ведет себя странно, он уже два дня не разговаривает со мной. Сегодня он оставил свой бумажник на столе, при том что обычно не забывает свои вещи... Может у него что-то случилось и он боится сказать?"
    # "Andrew added this text for initial commit in his branch."
    
    # menu(screen="choice_arrows"):
    #     "Будешь в форт"
    #     "Конечно пошли" (arrow_down=False):
    #         "Красава"
    #     "Нет, не иду" (arrow_down=True):
    #         "Нет, идешь"

    # menu:
    #     "You have a choice!"
    #     "Choice 1":
    #         "Text for choice 1"
    #     "Choice 2":
    #         "Text for choice 2"

    # menu:
    #     "Choice with 3 options!"
    #     "Choice 1":
    #         "Text for choice 1"
    #     "Choice 2":
    #         "Text for choice 2"
    #     "Choice 3":
    #         "Text for choice 3"

    # menu:
    #     "Choice with 4 options here!"
    #     "Choice 1":
    #         "Text for choice 1"
    #     "Choice 2":
    #         "Text for choice 2"
    #     "Choice 3":
    #         "Text for choice 3"
    #     "Choice 4":
    #         "Text for choice 4"
    
    # $ quick_menu = False
    # call screen Map(chapter1_locs1)
    
    # jump chapter_1

label chapter_1:

    play music "music/talk_detective.mp3" fadein 1.0 fadeout 1.0 loop

    $ chapter = "Chapter One"
    $ location = "2nd Location"
    scene expression im.Scale("images/chapters/chapter_1_bg.png", config.screen_width, config.screen_height)
    show expression Solid("#000000b0") as dark_overlay
    if "Chapter 1" not in persistent.chapters:
        $ persistent.chapters.append("Chapter 1")
    "Убийство молодой студентки: Джейн Лоуренс, 22 года. Тело найдено на берегу реки прохожей пожилой женщиной, выгуливающей собаку. Согласно первоначальной версии, это несчастный случай либо суицид, но руки жертвы покрыты жуткими порезами, поэтому дело предстоит раскрыть."
    

    # $ add_person_file_info(persons_files, "images/map/jaclyn_idle.png", "Добавил хуйню.")
    # $ max_person_pages = len(persons_files) // 6

    # $ config.rollback_enabled = False
    $ quick_menu = True
    # $ renpy.block_rollback()
    jump teemMeeting
    
    
    return

label teemMeeting:

    scene expression im.Scale("images/locations/office.png", config.screen_width, config.screen_height) with dissolve

    show casey at sprite_left, darken
    show govard at sprite_centered, darken
    show phil at sprite_right, darken
    mc "Жертва — Джейн Лоуренс. Двадцать два года. Училась в городском университете, факультет журналистики, второй курс. Утром её тело прибило к набережной. Пожилая леди, которая ее нашла, вряд ли будет там снова выгуливать свою собаку."
    mc "Местная полиция ограничилась ленточкой и протоколом. Родители опознали дочь. Всё. Они считают, что дальше пусть работает федеральный уровень. И вот мы здесь."
    $unlock_clue("victim_photo")
    show govard at sprite_centered, lighten
    govard "Давно наш отдел занимается утопленниками?"

    show govard at sprite_centered, darken
    mc "Агент Браун, меньше вопросов. Если дело отдали нам, на то есть причина."

    show phil at sprite_right, lighten
    phil "Но у нас пока нет заключения по телу. Только время смерти в общих чертах — вчера вечером, несколько часов до того, как её вынесло к берегу. Ни причины, ни характера повреждений."

    show phil at sprite_right, darken
    mc "Верно. Первое направление — морг городской больницы. Мистер Эндрюс уже ждет кого-то из нас с заключением."

    show govard at sprite_centered, lighten
    govard "Если её убили, патологоанатом расскажет больше, чем все свидетели вместе."

    show govard at sprite_centered, darken
    mc "Второе направление — университет. Второй курс журналистики. Друзья, одногруппники, завистники. Любые слухи и сплетни."

    show casey at sprite_left, lighten
    casey "Там же мы можем узнать о её личной жизни. Возможно, были отношения, о которых родители не знали."

    show casey at sprite_left, darken
    mc "Именно. А родители — третье направление. Дом семьи Лоуренс. Там лежат её вещи, фотографии, записки. Родители скажут нам, какой была Джейн вне стен кампуса."

    mc "Но учтите — они только что потеряли дочь. Разговор будет тонкий. Впрочем, это не повод размазывать эмоции. Мы расследуем убийство."

    show phil at sprite_right, lighten
    phil "Тогда один из нас остаётся здесь? Чтобы разобрать материалы полиции?"

    show phil at sprite_right, darken
    mc "Да. У нас три точки и четыре человека. Тот, кто остаётся, не отдыхает, а проверяет материалы полиции."

    show govard at sprite_centered, lighten
    govard "То есть кто-то сидит за бумагами, пока остальные работают по-настоящему. Отличный жребий."

    show govard at sprite_centered, darken
    mc "Вопрос один: кто куда пойдёт. Морг. Университет. Дом родителей. Штаб. Решаем быстро."

    hide mc
    hide govard
    hide casey

    $ quick_menu = False
    call screen Map(chapter1_locs1)



label university:
    play music "music/univer.mp3" fadein 1.0 fadeout 1.0 loop
    $ renpy.block_rollback()
    
    # $ clearDict(directions)
    scene univ_front
    $ unlock_achievement( "locations", "4.2", "Вы получили достижение!")
    # show mc thoughts at sprite_centered
    mc_thoughts "Не нужно быть гением криминалистики, чтоб знать о том, что если хочешь узнать что угодно о ком угодно - найди самую тихую и неприметную девочку. Нет более качественных хранителей сплетен в старшей школе, чем они."    
    scene univ_hall
    mc "Извините, мисс?"
    show judy at zoom_in
    with dissolve
    "???" "Вы кто?"
    mc "Спецагент Картер, отдел уголовных расследований ФБР. Как я могу к Вам обращаться?"
    judy "Джуди."
    judy "Я знаю, почему Вы здесь."
    mc "О чем Вы?"
    judy "Вы не первый, кто спрашивает о Лоуренс. От нее избавились. Весь курс об этом говорит."
    mc_thoughts "По-моему, я не говорила о том, что это не несчастный случай и не суицид"
    
    menu:
        " " # Putting here spaces for it to activate the 'say' label with the choice label (black panel behind choice buttons)
        "Избавились":
            judy "От этой заносчивой занозы только глухой не слышал оскорблений в свой адрес. Ее гордая мамашка внушила ей, что она королева красоты, и что больше ничего в этой жизни неважно. А деньги папочки только усиливали их веру в это. Две куклы"
            jump univ_fe
        "Что Вы знаете об этом?":
            judy "Что желающих было предостаточно. Таких выскочек давно не было. Будь у меня побольше свободного времени, повод и хорошее алиби, я бы тоже с ней расправилась"
            jump univ_fe

label univ_fe:
    menu:
        " " # Putting here spaces for it to activate the 'say' label with the choice label (black panel behind choice buttons)
        "Вы не сильно любили мисс Лоуренс, судя по всему":
            judy "Никто ее не любил. С ней общались только из-за денег и популярности. Ее отец покупал ей места на конкурсах, лишь бы его стервозная жена реализовала свои несбывшиеся амбиции через дочь и не трогала его. Даже Мисс Университет он ей купил, хотя были девочки, которые мечтали об этом чертовом кольце не меньше, чем она, и были достойнее ее."
            judy "Кольцо Мисс Университет. Это пропуск на конкурс Мисс Штат. Девочки боролись за титул ради стипендии, чтобы помочь родителям с оплатой учебы. А Лоуренсы хотели потешить свое самолюбие. Неудивительно, что шли разговоры о том, чтоб отравить ее."
            mc "Что случается с титулом, если победительница не может исполнять свои обязанности?"
            judy "Титул переходит вице-мисс."
            mc "Кто стал вице-мисс?"
            judy "Леони Джонс"
            jump univ_rs
        "Был ли кто-то, кто особенно не любил Джейн?":
            judy "Она перешла дорогу почти каждой девушке здесь. Парни смотрят только за ее юбкой, а на обычных девочек всем все равно. "
            judy "Но если выбирать одну, то я бы назвала Леони Джонс. Лоуренс украла у нее звание Мисс Университет. Леони стала вице-мисс, хотя она была достойна этого кольца гораздо больше. Просто у нее не такой богатый папа."            
            mc "О каком кольце Вы говорите?"
            judy "Кольцо Мисс Университет. Это пропуск на конкурс Мисс Штат. Девочки боролись за титул ради стипендии, чтобы помочь родителям с оплатой учебы. А Лоуренсы хотели потешить свое самолюбие."
            jump univ_rs

label univ_rs:
    mc "Она состояла с кем-то в отношениях?"
    judy "Проще сказать с кем она не состояла в отношениях. Хотя ладно, были эти несчастные парниши, которые влюблялись в эту путышку и тащились за ней везде, начиная со школы. Но они были слишком небогаты и некрасивы для куколки, и куколка их игнорировала"
    mc "Вы знаете, что она делала в день смерти?"
    judy "Почему всем это так интересно?"
    mc_thoughts "Всем? Кто-то еще интересовался этим?"
    judy "Собиралась со своим хахалем в ресторан на Блинк-роуд. Наследник папиного бизнеса - всё как она любит. Велик ей не нравится, подавай Роллс-Ройс. Жалко парня, передайте ему привет, если будете допрашивать."
    mc_thoughts "Ладно, она еще и любительница метафор."
    mc "Вы знаете, где можно найти ее молодого человека?"
    judy "Армори-стрит 19, но за дополнительную плату и не такое найду"
    mc_thoughts "Похоже мне стоит опасаться, что я ей сказала, как меня зовут."
    mc "Спасибо, сэкономлю и поручу кибер-отделу."
    judy "Многое теряете, босс."
    mc_thoughts "О, а вот и тот, о ком мы говорили!"
    "В конце коридора направляется к выходу из здания щуплый кучерявый парниша лет 20 с небольшим."
    menu:
        " " # Putting here spaces for it to activate the 'say' label with the choice label (black panel behind choice buttons)
        "Стойте, сэр! Я из ФБР, нам нужно поговорить.":
            "Парень, не оборачиваясь, ускоряет шаг и выходит из здания"
            mc_thoughts "Черт, он либо глухой, либо что-то знает. Ну ничего, увидимся на Армори-стрит"
            $ unlock_achievement( "leadership", "5.4", "Вы получили достижение!")
            mc "Спасибо за помощь следствию, мисс."
            judy "Не забудьте передать привет."
            $character_interviewed("judy")
            hide judy
            $unlock_person("judy") 
            jump evidence_exchange

        "Я еще успею с ним общаться в более подходящей обстановке":
            mc "Спасибо за помощь следствию, мисс."
            judy "Не забудьте передать привет."
            $character_interviewed("judy")
            hide judy
            $unlock_person("judy")
            jump evidence_exchange

label parents_house:
    play music "music/james_house.mp3" fadein 1.0 fadeout 1.0 loop
    $ renpy.block_rollback()
    # $ clearDict(directions)
    $ unlock_achievement( "locations", "4.1", "Вы получили достижение!")
    scene par_h_entry 
    with dissolve
    show mr_lawrence at halfed_left,darken
    show mrs_lawrence at halfed_right,darken
    mc "Мистер и Миссис Лоуренс, я спецагент Жаклин из ФБР, примите мои соболезнования. Мне необходимо задать вам пару вопросов."
    menu:
        " "
        "Расскажите о вашей дочери.":
            jump par_house_td
        "Когда вы в последний раз говорили с вашей дочерью?":
            jump par_house_ltsd


label par_house_td: # Расскажите о дочери
    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Наша Джейн всегда была хорошей девочкой. Она не заслужила такую короткую жизнь..."

    show mr_lawrence at halfed_left, darken
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Она была нашей звездочкой, нашей единственной красавицей."
    mrs_lawrence @ pride "Всегда была лучшей на всех конкурсах. Джейн была маленькой копией меня. Я ей очень гордилась."

    show mrs_lawrence at halfed_right, darken
    mc_thoughts "Eе дочери нет в живых, а она вспоминает о конкурсах"
    mc "Ваша дочь жила вместе с Вами?"

    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Нет, ну что Вы. Она уже большая девочка. Как только ей исполнилось 18, она переехала жить к своему молодому человеку."

    show mr_lawrence at halfed_left, darken
    menu:
        " "
        "Вы знали его?":
            jump par_house_ukh
        "Вы говорили с ним после случившегося?":
            jump par_house_tthah

label par_house_ltsd: # последний раз говорили с дочерью
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Я звонила поздравить ее с титулом Мисс Университет. Это было на прошлой неделе. Джейн мечтала об этом титуле."
    mrs_lawrence "Это бы приблизило ее к тому, чтобы выйти в претендентки на Мисс Штат. Это была ее мечта, наша мечта."

    show mrs_lawrence at halfed_right, darken
    show mr_lawrence at halfed_left, lighten
    mr_lawrence @ sad "Она получила кольцо, но корону моя малышка уже не получит."

    show mr_lawrence at halfed_left, darken
    mc "Что за кольцо?"

    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Девушка, получившая титул Мисс Университет, получает кольцо в качестве приза. Только с ним она уже сможет отправиться на следующий этап. Я тоже остановилась на кольце в свое время..."
    mrs_lawrence "Но Джейни могла получить корону..."

    show mrs_lawrence at halfed_right, darken
    mc "Джейн жила у вас?"

    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Нет, ну что Вы. Она уже большая девочка. Как только ей исполнилось 18, она переехала жить к своему молодому человеку."

    show mr_lawrence at halfed_left, darken
    menu:
        " "
        "Вы знали его?":
            jump par_house_ukh
        "Вы говорили с ним после случившегося?":
            jump par_house_tthah

label par_house_ukh: # Вы знали его
    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Кайл его зовут, лично не встречались, видели фотографии и знаем адрес: Марч-Драйв 77. Познакомились они в последних классах школы. Он капитан команды по футболу, крепкий парень."

    show mr_lawrence at halfed_left, darken
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Правда, характером он был похлеще нашей Джейн. Ссорились они ежедневно."

    show mrs_lawrence at halfed_right, darken
    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Помню, однажды так сильно поругались, что она вернулась жить к нам. Так наш телефон в гостиной просто разрывался: я однажды взял трубку, а там 'Стань моей, я буду тебя любить' и всякое подобное."
    mr_lawrence "Непривычно было слышать такие вещи от брутального парня, я бы не поверил, если бы сам не услышал."
    mr_lawrence @ thoughts "Еще и говор у него такой странный, как будто с акцентом."

    show mr_lawrence at halfed_left, darken
    jump par_house_wsl

label par_house_wsl: # Когда она вновь уехала
    mc "Когда она вновь уехала от Вас?"

    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Через неделю. И вот уже почти три месяца все было спокойно. Притерлись наконец, мы думали. Не представляю, каково этому парнишке сейчас."

    show mrs_lawrence at halfed_right, darken
    menu:
        " "
        "Вы были близки с ней?":
            jump par_house_wuc
        "С кем она делилась своими переживаниями или секретами?":
            jump par_house_whss

label par_house_wuc: # Вы были близки с ней
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Она была свободолюбивой и гордой. Я не лезла к ней в душу. Я была хорошей матерью и никогда не нарушала ее границ."

    show mrs_lawrence at halfed_right, darken
    mc_thoughts "Или просто не интересовалась дочерью."

    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Я даже никогда не заглядывала в ее личный дневник, хотя знала, где он лежит. Он даже сейчас у нас дома. Джейн его оставила у нас, когда неделю здесь жила. Но он очень древний, вряд ли он Вам поможет."
    
    # *Получить записи дневника*
    $ unlock_achievement( "objects", "2.3", "Вы получили достижение!")
    "(В личном дневнике записи о маме-тиране и многолетнем сталкерстве)"

    mc "Кто-то мог желать ей зла?"

    show mrs_lawrence at halfed_right, darken
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence @ outraged "Ну что Вы?! Нашу девочку всегда обожали. Она всегда побеждала и была первой. Парни сходили по ней с ума, а девушки восхищались."
    $unlock_person("mrs_lawrence")
    show mrs_lawrence at halfed_right, darken
    mc_thoughts "Или завидовали.."

    show mr_lawrence at halfed_left, lighten
    mr_lawrence @ sad "Вот, посмотрите показывает детский школьный альбом. Она всегда была красивой девочкой. А здесь она уже роскошная девушка показывает выпускной альбом. Не представляю, кто мог так поступить с ней... Только чудовище. Она сама никогда бы не сделала это..."

    show mr_lawrence at halfed_left, darken
    mc "Мы сделаем всё, что в наших силах, чтобы раскрыть дело, Мистер и Миссис Лоуренс."

    hide mr_lawrence
    hide mrs_lawrence
    $character_interviewed("mr_lawrence")
    $character_interviewed("mrs_lawrence")
    
    $unlock_person("mr_lawrence")
    jump evidence_exchange

label par_house_whss: # С кем делилась переживаниями
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Она держала какую-то тетрадку под кроватью. Полагаю, что это ее личный дневник, она его оставила у нас, когда неделю здесь жила. Но он очень древний, вряд ли он Вам поможет."

    # *Получить записи дневника*
    $ unlock_achievement( "objects", "2.3", "Вы получили достижение!")
    "(В личном дневнике записи о маме-тиране и многолетнем сталкерстве)"

    mc "Кто-то мог желать ей зла?"

    show mrs_lawrence at halfed_right, darken
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "Ну что Вы?! Нашу девочку всегда обожали. Она всегда побеждала и была первой. Парни сходили по ней с ума, а девушки восхищались."

    show mrs_lawrence at halfed_right, darken
    mc_thoughts "Или завидовали.."

    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Вот, посмотрите показывает детский школьный альбом. Она всегда была красивой девочкой. А здесь она уже роскошная девушка показывает выпускной альбом. Не представляю, кто мог так поступить с ней... Только чудовище. Она сама никогда бы не сделала это..."

    show mr_lawrence at halfed_left, darken
    mc "Мы сделаем всё, что в наших силах, чтобы раскрыть дело, Мистер и Миссис Лоуренс."

    hide mr_lawrence
    hide mrs_lawrence
    $unlock_person("mrs_lawrence")
    $character_interviewed("mr_lawrence")
    $character_interviewed("mrs_lawrence")
    jump evidence_exchange

label par_house_tthah: # Вы говорили с ним после случившегося
    show mrs_lawrence at halfed_right, lighten
    mrs_lawrence "У нас нет его контактов, только знаем, что зовут его Кайл. Он живет далеко — на Марч-Драйв 77, если бы он хотел, сам бы приехал. Джейн доверяла ему, а мы доверяли Джейн. Она девочка с высокими запросами, мы ее такой воспитали."
    mrs_lawrence "Поклонников у нее всегда было много, но она выбирала самых лучших. Правда, характером он был похлеще нашей Джейн. Ссорились они ежедневно."

    show mrs_lawrence at halfed_right, darken
    show mr_lawrence at halfed_left, lighten
    mr_lawrence "Помню, однажды так сильно поругались, что она вернулась жить к нам. Так наш телефон в гостиной просто разрывался: я однажды взял трубку, а там 'Стань моей, я буду тебя любить' и всякое подобное. Непривычно было слышать такие вещи от брутального парня, я бы не поверил, если бы сам не услышал."
    mr_lawrence @ thoughts "Еще и говор у него такой странный, как будто с акцентом."

    show mr_lawrence at halfed_left, darken
    jump par_house_wsl

label hospital:
    play music "music/talk_detective.mp3" fadein 1.0 fadeout 1.0 loop
    $ renpy.block_rollback()
    # $ clearDict(directions)
    scene hospital 
    $ unlock_achievement( "locations", "4.4", "Вы получили достижение!")
    with dissolve
    show dr_andrews at halfed
    mc "Здравствуйте, Доктор Эндрюс, давно не виделись"
    dr_andrews "Здравствуй, Жаклин. Кто на этот раз?"
    mc "Мисс Джейн Лоуренс, 22 года"
    dr_andrews "Снова молоденькая. Думаете маньяк?"
    mc "Вряд ли. Почерк необычный - изрезаны кисти рук."
    dr_andrews "Что ж. Пойдешь взглянуть или только заключение?"
    menu:
        " "
        "Давайте посмотрю":
            jump hosp_lms
        "Только заключение":
            jump hosp_oc

label hosp_lms: # Давайте посмотрю
    dr_andrews "Смерть наступила около полуночи вследствие убийства. Следов сескуального насилия не обнаружено."
    dr_andrews "Но вот с отпечатками я помочь не смогу - вода все смыла."    
    mc "Убийством называешь из-за порезов на руках?"
    dr_andrews "Жаклин, порезы на руках тебе может и куст розы оставить."
    dr_andrews "У нее смерть от удушья, но не от воды она задохнулась."    
    menu:
        " "
        "В легких нет воды?":
            dr_andrews "Бинго, агент Картер! Приятно иметь с Вами дело."
            jump hosp_lm
        "Ближе к делу, Эндрюс":
            $ unlock_achievement( "leadership", "5.4", "Вы получили достижение!")
            dr_andrews "Какой скучный агент. ФБР вас специально таких отбирает?"
            mc "Мне не до шуток."
            dr_andrews "А зря, с такой работой без шуток долго не прожить."
            mc "Дальше?"
            jump hosp_lm

label hosp_oc: # Только заключение
    dr_andrews "Смерть наступила около полуночи вследствие убийства. Следов сескуального насилия не обнаружено. Отпечатков также не обнаружено из-за нахождения тела в воде. Причиной смерти является удушье, но так как в легких вода не была обнаружена, она не дышала еще до того, как оказалась в реке. Жертва была задушена собственным шарфом. Ее одежда здесь, можешь забрать орудие убийста. Родители не захотели забирать ее вещи."
    mc "Интересная семья."
    dr_andrews "Следов этилового спирта в крови не обнаружено. Обнаружены следы гематом в районе запястий, что свидетельствует о том, что убийца был физически сильнее ее, так как этого было достаточно, чтоб ее обездвижить."
    menu:
        " "
        "Вау, мы сузили круг до всех мужчин от 16 до 70":
            $ unlock_achievement( "leadership", "5.2", "Вы получили достижение!")
            dr_andrews "Не забывай и о женщинах, агент. Я многого в своей жизни насмотрелся - не стоит сбрасывать 'слабый пол' со счетов."
            mc "Есть в этом правда, Эндрюс."
            dr_andrews "Хочешь взглянуть на ее одежду?"
            mc "Пожалуй взгляну."
            jump hosp_lc
        "Что скажете о ее порезах на руках?":
            dr_andrews "А я думал, что ты не спросишь! Не зря ты начальник команды, Картер, молодец. Зришь в корень!"
            dr_andrews "54 пореза в зоне кистей рук. Но самое интересное то, что только один из них - вот этот - самый глубокий, вот здесь на безымянном пальце, был нанесен при жизни."
            mc "Зачем кому-то резать руки трупу?"
            dr_andrews "Ответы на эти вопросы - уже Ваша работа, спецагент. Можете взглянуть на ее одежду, если Вам это что-то даст."
            jump hosp_lc

label hosp_lm: # Узнать больше
    dr_andrews "Смерть наступила вследствие удушья. Жертва была задушена собственным шарфом. Ее одежда здесь, можешь забрать орудие убийста. Родители не захотели забирать ее вещи."
    mc_thoughts "Интересная семья.."
    dr_andrews "Обнаружены следы гематом в районе запястий. Видимо, ее держали за руки, не давая убежать."
    dr_andrews "Самое интересное - порезы на руках. Взгляните, агент Картер. Видите, этот? Самый глубокий на безымянном пальце."
    mc "Что в нем особенного?"
    dr_andrews "Этот порез единственный, который нанесли при жизни жертвы."
    mc "Остальные нанесли уже трупу?"
    dr_andrews "Агент Картер, да Вы сегодня гений дедукции!"
    mc_thoughts "Зачем было резать руки трупу?"
    mc "Спасибо, Эндрюс. Если в результатах анализов будет что-то интересное - набери меня."
    dr_andrews "Сразу же, Жаклин..."
    dr_andrews "Стой! Я забыл спросить: как Лия?"
    menu:
        " "
        "Держится":
            dr_andrews "Она сильная как ее мама, она справится. Если я смогу чем-то помочь, Жаклин, всегда можешь на меня рассчитывать"
            $ unlock_achievement( "leadership", "5.5", "Вы получили достижение!")
            mc "Спасибо, Эндрюс."
            hide dr_andrews
            $unlock_person("dr_andrews")
            $character_interviewed("dr_andrews")
            jump evidence_exchange
        "Я не хочу об этом говорить":
            hide dr_andrews
            $character_interviewed("dr_andrews")
            $unlock_person("dr_andrews")
            jump evidence_exchange

label hosp_lc: # Взглянуть на веши
    mc "Такие же серьги я подарила Лие на 16-летие"
    dr_andrews "Как она?"
    menu:
        " "
        "Держится":
            dr_andrews "Она сильная как ее мама, она справится. Если я смогу чем-то помочь, Жаклин, всегда можешь на меня рассчитывать"
            mc "Спасибо, Эндрюс."
            hide dr_andrews
            $character_interviewed("dr_andrews")
            $unlock_person("dr_andrews")
            jump evidence_exchange
        "Я не хочу об этом говорить":
            hide dr_andrews
            $character_interviewed("dr_andrews")
            $unlock_person("dr_andrews")
            jump evidence_exchange

label restaurant:
    play music "music/chill_music.mp3" fadein 1.0 fadeout 1.0 loop
    $ renpy.block_rollback()
    # $ clearDict(directions)
    scene restaurant with dissolve
    $ unlock_achievement( "locations", "4.3", "Вы получили достижение!")
    show mrs_velaskez at halfed
    with dissolve
    mc "Миссис Веласкес, я специальный агент Картер, отдел уголовных расследований ФБР."
    mrs_velaskez "Я уже сто раз рассказала легавым, что происходило в тот день. Мне нужно работать."
    #text issue
    menu:
        " "
        "Это важно для расследования и займет всего пять минут вашего времени.":
            mrs_velaskez @ irritated "Девчонку не вернуть. А свое время я терять не собираюсь. Нужны ответы - поговорите с Лизой, она обслуживала эту парочку."
            jump rest_cwl2
        "Я имею все полномочия задержать вас за сопротивление следствию и вместо пяти минут, допрос будет дилтся несколько часов.":
            $ unlock_achievement( "leadership", "5.4", "Вы получили достижение!")
            jump rest_angry

label rest_angry: # я имею все полномочия задержать вас за сопротивление следствию и вместо пяти минут, допрос будет дилтся несколько часов
    mrs_velaskez "Пять минут. Не более. Я знаю, что происходит на кухне, пока я не вижу."
    mrs_velaskez @ irritated "За эти 5 минут эти гады ее вынесут по частям."
    mc "Расскажите, что вы видели тем вечером, когда произошло убийство."
    mrs_velaskez "Я вижу целыми днями ножи и гастроемкости, тот вечер - не исключение."
    mrs_velaskez @ irritated "Еще вопросы?"
    mc "Вы видели мисс Лоуренс и ее спутника?"
    mrs_velaskez "Я видела две тарелки пасты с креветками, которые они заказали. И самое дешевое пойло к нему - стыдно должно быть портить такую еду этой гадостью."
    mc "Замечали ли вы что-то странное или подозрительное в поведении сотрудников?"
    mrs_velaskez @ irritated "Вороство уже давно не подозрительно в этом коллективе посудомоек."
    menu:
        " "
        "* Расспросить далее *":
            jump rest_am
        "* Задать следующий вопрос *":
            jump rest_nq

label rest_am: # Распросить еще
    mc "Почему Вы тогда упомянули его?"
    $ unlock_achievement( "leadership", "5.1", "Вы получили достижение!")
    mrs_velaskez "Раньше хотя бы воровали продукты, а не вещи из моего кабинета."
    mrs_velaskez @ smug " Но он уже уволен. Это было последней каплей: выносить на себе мясо - я ещё понимаю, но золото собственника ресторана - это уже слишком."
    mc "У вас украли украшения?"
    mrs_velaskez @ irritated "Этот гад не признался, но когда у меня пропадает кольцо со стола, я не могу это не заметить."
    mrs_velaskez "К счастью, это не семейная реликвия, а ее копия. Благо никто, кроме меня и нашей Лизы об этом не знает. Даже сын не в курсе."
    mrs_velaskez @ irritated "Не дура же я так рисковать в этом гадюшнике."
    # пообщаться с лизой v1
    mc_thoughts "Похоже этот разговор зашел в тупик."
    mc_thoughts "Я решил попробовать пообщаться с кем-то из сотрудников."
    mc "С кем я могу поговорить из официантов, кто видел пару в тот вечер?"
    mrs_velaskez "Сейчас позову Лизу, она их обслуживала. Единственный толковый человек, который здесь работает."
    hide mrs_velaskez with dissolve
    $character_interviewed("mrs_velaskez")
    $unlock_person("mrs_velaskez")
    show lisa at halfed
    with dissolve
    $ unlock_achievement( "leadership", "5.3", "Вы получили достижение!")
    mc "Я спецагент Картер, ФБР. Мне небходимо задать Вам пару вопросов."
    lisa "Хорошо, спрашивайте."
    mc "Вы видели эту девушку?"
    mc_thoughts "В этот момент я показал фотографию жертвы и наблюдал за реакцией Лизы."
    lisa "Да, я обслуживала их столик. Она была с молодым человеком."
    lisa @ toxic "Несостоявшийся жених."
    mc "С чего Вы взяли, что он ее жених?"
    lisa "Он приходил заранее перед их свиданием и попросил меня спрятать кольцо в десерте, который они бы заказали. Правда, не успели."
    mc "Почему?"
    lisa "Спустя минут 20 прибежал какой-то парень. Устроил скандал, оскорблял ее, а ее молодой человек просто сидел и молчал."
    lisa @ toxic "Вряд ли бы у них что-то вышло."
    mc "Что произошло после?"
    jump rest_whn


label rest_nq: # следующий вопрос
    mc "С кем я могу поговорить из официантов, кто видел пару в тот вечер?"
    mrs_velaskez "Сейчас позову Лизу, она их обслуживала. Единственный толковый человек, который здесь работает."
    $ unlock_achievement( "leadership", "5.3", "Вы получили достижение!")


label rest_whn: # # Что произошло после
    lisa "Ее спутник был не в восторге от произошедшего. Сначала ушел скандалист, бросив в сторону девушки кольцо, которое видимо предназначлось ей, а потом и ее парень встал, расплатился и ушел, оставив ее одну."
    lisa "Попросил у меня вернуть кольцо, ну я и отдала, конечно. Больше ничего не могу Вам сказать."
    mc "А что девушка?"
    lisa @ toxic "Она была приятно удивлена, что он заплатил перед уходом. Доела, допила и ушла."
    mc "Во сколько это было?"
    lisa "Где-то около десяти вечера."
    mc "Спасибо, вопросов больше нет. Выдайте мне, пожалуйста, полный список сотрудников."
    lisa "Сейчас напишу."
    hide lisa
    $unlock_person("lisa")
    $character_interviewed("lisa")
    jump evidence_second_exchange

label rest_cwl2: # пообщаться с Лизой v2
    hide mrs_velaskez with dissolve
    $character_interviewed("mrs_velaskez")
    $unlock_person("mrs_velaskez")
    show lisa at halfed
    with dissolve
    $ unlock_achievement( "leadership", "5.3", "Вы получили достижение!")
    mc "Я спецагент Картер, ФБР. Мне небходимо задать Вам пару вопросов."
    lisa "Хорошо, спрашивайте."
    mc "Вы видели эту девушку?"
    mc_thoughts "В этот момент я показал фотографию жертвы и наблюдал за реакцией Лизы."
    lisa "Да, я обслуживала их столик. Она была с молодым человеком."
    lisa @ toxic "Несостоявшийся жених."
    mc "С чего Вы взяли, что он ее жених?"
    lisa "Он приходил заранее перед их свиданием и попросил меня спрятать кольцо в десерте, который они бы заказали. Правда, не успели."
    mc "Почему?"
    lisa "Спустя минут 20 прибежал какой-то парень. Устроил скандал, оскорблял ее, а ее молодой человек просто сидел и молчал."
    lisa @ toxic "Вряд ли бы у них что-то вышло."
    menu:
        " "
        "Что стало с кольцом?":
            jump rest_whr
        "Кто этот молодой человек?":
            jump rest_wwtm

label rest_whr: # Что стало с кольцом
    lisa "С которым из колец?"
    mc "Их было много?"
    lisa "Ну, ее парень хотел сделать предложение, но после того скандала, он почти сразу ушел. Попросил у меня вернуть кольцо, ну я и отдала, конечно. А тот, что прибежал скандалить тоже был с кольцом."
    lisa "Я мало, что поняла, но кольца - это буквально проклятие того вечера."
    mc "Что Вы хотите этим сказать?"
    lisa "У нашего шефа миссис Веласкес пропало кольцо. Повезло, что это была не семейная реликвия, а только ее копия, но знают об этом только я и она, даже родной сын не в курсе."
    lisa "На кухне нельзя носить украшения, а оставлять ценные вещи на кухне - опасно. Все знают, что на кухне воруют."
    mc "Что произошло после?"
    jump rest_whn

label rest_wwtm: # Кто этот молодой человек
    lisa "Я предполагаю, что это был ее бывший."
    mc "Почему Вы так считаете?"
    lisa "Он кричал что-то про предательство. Судя по всему, он все еще не принял то, что он бывший... Либо он стал бывшим после этого случая."
    lisa "Я не очень поняла, что именно произошло, помимо того, что девушка явно нарасхват."
    jump rest_whn


label james_house:
    play music "music/james_house.mp3" fadein 1.0 fadeout 1.0 loop
    $ renpy.block_rollback()
    # $ clearDict(directions)
    scene james_house with dissolve
    $ unlock_achievement( "acquaintances", "1.1", "Вы получили достижение!")
    mc "Джеймс Майерс, это специальный агент Картер, отдел уголовных расследований ФБР. Откройте дверь."
    show james at halfed
    "Открылась дверь и показался молодой человек."
    
    with dissolve
    james "Вы здесь из-за Джейн?"
    mc_thoughts "Он совсем не похож на того парня, который был в университете. Кучерявых волос нет, а лишние лет 10 - есть."
    mc "Да. Кем Вы ей приходились?"
    james @ sad "Я бы сам хотел это знать.."
    menu:
        " "
        "Что Вы имеете в виду?":
            james @ sad "Думал, что парень, но оказалось, что не я один так думал."
            mc "Расскажите, что произошло в тот вечер."
            jump jhouse_twhte
        "Вы были с ней в ресторане вечером 17-ого числа?":
            james "Да, был. У нас было свидание. Я долго его ждал."
            james @ smile "Мы были вместе почти 3 месяца, и это были самые прекасные дни в моей жизни."
            mc "Расскажите, что произошло в тот вечер."
            jump jhouse_twhte

label jhouse_twhte: # Расскажите, что произошло в тот вечер
    james "Я пригласил ее в ресторан. Хотел сделать предложение."
    james @ smile "Несмотря на всю ее меркантильность, она была единственным светлым лучом в моей жизни. Я сходил заранее за кольцом, договорился с официанткой, чтобы сделать ей сюрприз."
    james "Мы пришли, заказали еду и ее любимое вино."
    james @ sad "А через полчаса туда залетает какой-то амбал и начинает орать на нее, на меня. Я сначала не понял, что происходит, я был в шоке."
    menu:
        " "
        "Вы знали что-то об этом парне?":
            james "Я видел его впервые. Не стал бы я встречаться с девушкой, а тем более делать ей предложение, если бы знал, что там есть какие-то незаконченные отношения."
            james "Я не хотел быть запасным."
            menu: 
                " "
                "Вы были знакомы с ее родителями?":
                    jump jhouse_ukhp
                "Как вы с ней познакомились?":
                    jump jhouse_hum
        "Что он говорил?":
            james "Он скорее кричал, а не говорил. Мне удалось выяснить, что они встречались около 4 лет. Она его бросила, как только он уехал."
            james @ sad "Просто перестала отвечать на его сообщения, звонки. А он тоже собирался сделать ей предложение. Кинул кольцо и ушел."
            mc "Что Вы сделали после этого?"
            james @ sad "Я понял, что не хочу видеть такого человека рядом. Встал, заплатил за ужин, попросил кольцо обратно и ушел домой."
            menu: 
                " "
                "Как вы с ней познакомились?":
                    jump jhouse_hum
                "Вы были знакомы с ее родителями?":
                    jump jhouse_ukhp

label jhouse_ukhp: # Вы были знакомы с ее родителями?
    james "Она не хотела нас знакомить. Джейн говорила, что не хочет больше быть связанной со своей семьей."
    james @ sad "У нее было тяжелое детство. Мать вечно ее таскала по всяким конкурсам, чтобы самоутвердиться. А для ребенка это большой стресс."
    mc "Джейн давно жила с Вами?"
    james "С первого дня... ну точнее с первой ночи нашего знакомства она стала жить у меня. На следующее утро она забрала свои вещи от родителей и переехала ко мне."
    mc "Вас это не напугало?" 
    james "Мне уже 30 лет, я был в отношениях, которые длились 5 лет, был в двухнедельных. В начале разницы никакой. Не рискнешь - не узнаешь."
    menu:
        " "
        "Что Вы делали после того, как ушли?":
            jump jhouse_wudal
        "Вы говорили с ней после случившегося?":
            james "Нет."
            james @ sad "Я не хотел с ней говорить."
            menu:
                " "
                "Вы не беспокоились о том, как она доберется домой?":
                    james "Она всегда была самостоятельной. Адрес знает."
                    james "С таким милым личиком, ей бы кто угодно захотел помочь."
                    mc_thoughts "Ну просто мужчина мечты.."
                    mc "Есть кто-то, кто мог желать ей смерти?"
                    jump jhouse_wawhd
                "Что с вещами Джейн?":
                    jump jhouse_wajt

label jhouse_hum: # Как вы с ней познакомились?
    james "Вечером я подъехал за кофе в свое любимое местечко, а там она. Я на нее даже не посмотрел сначала. Она сама ко мне подошла. Сделала комплимент моим часам."
    james @ smile "Мне их отец подарил, поэтому было приятно. Мы разговорились. Видно было, что ее интересуют деньги, но а кого они не интересуют?"
    james "Я ее позвал к себе тоже не из-за выдающихся моральных качеств"
    mc "Вас это не напугало?"
    james "Мне уже 30 лет, я был в отношениях, которые длились 5 лет, был в двухнедельных. В начале разницы никакой. Не рискнешь - не узнаешь." 
    menu:
        " "
        "Что Вы делали после того, как ушли?":
            jump jhouse_wudal
        "Вы говорили с ней после случившегося?":
            james "Нет."
            james @ sad "Я не хотел с ней говорить."
            menu:
                " "
                "Вы не беспокоились о том, как она доберется домой?":
                    james "Она всегда была самостоятельной. Адрес знает."
                    james "С таким милым личиком, ей бы кто угодно захотел помочь."
                    mc_thoughts "Ну просто мужчина мечты.."
                    mc "Есть кто-то, кто мог желать ей смерти?"
                    jump jhouse_wawhd
                "Что с вещами Джейн?":
                    jump jhouse_wajt

label jhouse_wudal: # Что Вы делали после того, как ушли?
    james "Пошел домой. Мне хотелось побыть одному и подышать свежим воздухом, поэтому я решил пройтись до дома пешком."
    mc "Во сколько Вы пришли домой?"
    james "Около полуночи."
    mc "Кто-то может это подтвердить?"
    james "Я живу один с котом. Только он мог бы."
    menu:
        " "
        "Что с вещами Джейн?":
            jump jhouse_wajt
        "Может, Вас видели соседи?":
            jump jhouse_mnsu

label jhouse_wajt: # Что с вещами Джейн?
    james "Они здесь. Я начал их собирать, потому что мы бы не продложили жить вместе."
    james @ sad "Но она не вернулась. Не представляю теперь, что мне с ними делать. Родителей ее я не знаю."
    mc_thoughts "Вряд ли бы это ему помогло."
    mc "Есть кто-то, кто мог желать ей смерти?"
    jump jhouse_wawhd

label jhouse_mnsu: # Может, Вас видели соседи?
    james "В этом районе все спят уже в 10 вечера. Мне никто не встречался на пути, а даже если бы кто-то и видел меня, я бы не обратил на это внимание."
    james @ sad "Не каждый день срывается предложение.."
    mc "Есть кто-то, кто мог желать ей смерти?"
    jump jhouse_wawhd

label jhouse_wawhd: # Есть кто-то, кто мог желать ей смерти?
    james "Ее бывший парень был в таком гневе, что он совершил бы что угодно, чтоб она не досталась никому кроме него."
    mc "Последний вопрос: Вы знакомы с Джуди, одногруппницей Джейн?"
    james "Я никогда не видел никого из ее знакомых."
    mc "Она просила передать Вам привет."
    james "Очень в этом сомневаюсь."
    mc_thoughts "Я тоже."
    mc "Спасибо за помощь, мистер Майерс."
    $unlock_person("james")
    $character_interviewed("james")
    jump evidence_second_exchange


label kyle_house:
    play music "music/james_house.mp3" fadein 1.0 fadeout 1.0 loop
    scene kyle_house with dissolve
    $ unlock_achievement( "acquaintances", "1.1", "Вы получили достижение!")
    mc "Кайл Ричардс, это специальный агент Картер, отдел уголовных расследований ФБР. Отройте дверь."
    show kyle at halfed
    with dissolve
    kyle "Здравстуйте. Я Вас слушаю."
    mc "Я здесь по делу мисс Лоуренс."
    menu:
        " "
        "Кем она Вам приходилась?":
            kyle "Я встречался с ней с конца школы."
            kyle @ sad "Был влюблен в нее с детства, как и многие парни, но она выбрала меня."
            kyle "Наверное, потому что был рядом тогда, когда она была уязвима."
            kyle @ sad "У нее было трудное детство, а я сам без родителей рос и знал каково это, когда тебе не хватает любви дома. Непростая у нее выдалась жизнь."
            menu:
                " "
                "Она жила у Вас?":
                    jump khouse_hslwu
                "Что делало ее жизнь такой?":
                    jump khouse_wdhlt
        "Расскажите, что Вы о ней знаете":
            kyle "Могу о ней говорить теперь либо хорошо, либо никак. Вам подходит?"
            mc "Любая информация будет ценной для следствия."
            kyle "Она была очень несчастной девушкой, которая считала свое несчастье особенностью и почти гордилась им."
            kyle "Никто никогда не понимал, что может не нравиться в такой жизни, какая была у нее, поэтому она прятала все свои чувства под маской надменности и высокомерия."
            kyle "Никто не знал, какая она на самом деле."
            kyle @ sad "Никто кроме меня."
            menu:
                " "
                "Она жила у Вас?":
                    jump khouse_hslwu
                "Что делало ее жизнь такой?":
                    jump khouse_wdhlt

label khouse_hslwu: # Она жила у Вас?
    kyle "Мы съехались, как только ей исполнилось 18 лет. Она умоляла меня забрать ее к себе, чтоб больше не жить с родителями."
    kyle "Мне самому было трудно потянуть это финансово, но она тоже помогала, да и я не мог ее оставить."
    menu:
        " "
        "Вы долго были вместе?":
            jump khouse_wutfl
        "Были ли у нее враги?":
            jump khouse_wtae

label khouse_wdhlt: # Что делало ее жизнь такой?
    kyle "Она была невероятно красива, и это ей мешало."
    kyle "Ее мать стала паразитировать на этом, чтобы реализовать свои амбиции через дочь, потому что никогда так и не добилась титула Мисс Штат."
    kyle "Вот поэтому Джейн и таскали с детства по всем конкурсам, не давая ей проживать жизнь так, как она хочет."
    kyle "Она была инструментом для своих родителей, а не любимым ребенком."
    kyle "Ее мать одновременно обожала ее за ту красоту, которая бы позволила ей добиться того, чего она сама не смогла достичь, но и ненавидела ее из-за страха, что дочь окажется лучше."
    menu:
        " "
        "Вы долго были вместе?":
            jump khouse_wutfl
        "Зачем она продолжала участвовать в конкурсах?":
            jump khouse_wskpc

label khouse_wutfl: # Вы долго были вместе?
    kyle "Почти четыре года."
    kyle @ excuses "Знаете, я был ее островком безопасности, который ограждал ее от всего мира, но я не мог посвятить всю свою жизнь на то, чтоб быть ее телохранителем."
    kyle "Я с детства мечтал стать футболистом и это одно из немногих, что у меня хорошо получается."
    kyle "С деньгами туго, поэтому я ставил на то, что буду кормить нас тем, что стану профессиональным спортсменом."
    kyle @ sad "Но когда я сказал ей, что меня заметили на игре в университете и предлагают показать себя на чемпионате за хорошую сумму - она устроила мне истерику, что я бросаю её."
    mc "Как Вы поступили?"
    kyle @ excuses "Эта возможность была ради нашего общего блага. Не надо думать, что я эгоист. Я любил её и делал всё для нашего будущего."
    # Что произошло между вами?
    mc "Что произошло между вами?"
    jump khouse_whbut

label khouse_wtae: # Были ли у нее враги?
    kyle "Были завистники и поклонники. Но Вы знаете: от любви до ненависти - один шаг. Я и сам это проверил на себе."
    kyle "Она очень долго была объектом нездорового внимания, с самого детства: от матери, от жюри конкурсов, от мальчиков-подростков, пускающих слюни при ее виде, поэтому я был ее гарантом безопасности: когда я был рядом - ее никто бы не обидел."
    kyle @ excuses "Но Вы поймите, я рядом был на протяжении нескольких лет - я не могу остановить свою жизнь, если она не может идти дальше."
    kyle "С деньгами туго, поэтому я ставил на то, что буду кормить нас тем, что стану профессиональным спортсменом."
    kyle @ sad "Но когда я сказал ей, что меня заметили на игре в университете и предлагают показать себя на чемпионате за хорошую сумму - она устроила мне истерику, что я бросаю её."
    mc "Как Вы поступили?"
    kyle @ excuses "Эта возможность была ради нашего общего блага. Не надо думать, что я эгоист. Я любил её и делал всё для нашего будущего."
    mc "Что произошло между вами?"
    jump khouse_whbut

label khouse_wskpc: # Зачем она продолжала участвовать в конкурсах?
    kyle "Джейн думала, что мама ее полюбит, если она исполнит ее мечту. Поэтому она продолжала готовиться ко всем этим конкурсам."
    kyle @ excuses "Когда меня пригласили на чемпионат, я понимал, что оставляю ее наедине с детской травмой, но Вы поймите, я рядом был на протяжении нескольких лет - я не могу остановить свою жизнь, если она не может идти дальше."
    kyle "С деньгами туго, поэтому я ставил на то, что буду кормить нас тем, что стану профессиональным спортсменом."
    kyle @ sad "Но когда я сказал ей, что меня заметили на игре в университете и предлагают показать себя на чемпионате за хорошую сумму - она устроила мне истерику, что я бросаю её."
    mc "Как Вы поступили?"
    kyle @ excuses "Эта возможность была ради нашего общего блага. Не надо думать, что я эгоист. Я любил её и делал всё для нашего будущего."
    mc "Что произошло между вами?"
    jump khouse_whbut

label khouse_whbut: # Что произошло между вами?
    kyle "Она осталась у меня, а я уехал с командой."
    kyle "Старался ее поддерживать, мы каждый день были на связи. Но в какой-то момент у нее случилась паническая атака на почве конкурса - она ничего не ела весь день, чтобы влезть в конкурсное платье."
    kyle "Ее забрала скорая, а она обвинила в произошедшем меня."
    kyle @ sad "Ну я уже не смог стерпеть и высказал ей всё, что думаю об этих ее конкурсах."
    kyle "В общем, мы сильно поругались - даже сильнее обычного, и она уехала к родителям. А потом она просто пропала."
    mc "Вы звонили ее родителям?"
    kyle "Нет, у меня нет их номера."
    mc_thoughts "А кто тогда им звонил?"
    menu:
        " "
        "Подождите, Вы уверены?":
            kyle "Да, она нас никогда не знакомила. Я примерно знал, где она живет, но на этом всё."
            kyle @ sad "Собственно, это был наш предпоследний разговор."
            mc "Стойте, она не переехала к Вам спустя неделю?"
            kyle "Нет, я вернулся с чемпионата только на днях, я не видел ее с тех пор, как уехал и до того самого злополучного дня, когда я вернулся в город."
            kyle "Я думал, что она у родителей."
            mc_thoughts "А где она тогда жила?"
            menu:
                " "
                "Что Вы сделали, когда вернулись?":
                    jump khouse_wudtb
                "Что Вы сделали, когда она перестала отвечать?":
                    jump khouse_wudssa
        "У неё могли быть отношения параллельно с Вами?":
            kyle "Это вряд ли. Слухи всегда ходили, что она пользуется спросом у парней, но это придумали ее завистницы."
            kyle "Я ничего подобного не видел. Ссорились мы не из-за этого, а потому что оба упрямые и хотим, чтоб было по-нашему."
            menu:
                " "
                "Что Вы сделали, когда вернулись?":
                    jump khouse_wudtb
                "Когда Вы говорили с ней в последний раз?":
                    jump khouse_wuslt

label khouse_wudtb: # Что Вы сделали, когда вернулись?
    kyle "Я к этому времени окончательно понял, что не хочу её терять. Жить с ней не сахар, но без нее еще хуже."
    kyle "Я решил действовать решительно: купил кольцо и поехал по всему городу искать ее."
    kyle "А потом подумал, что не нужно быть гением криминалистики, чтоб знать о том, что если хочешь узнать что угодно о ком угодно - найди самую тихую и неприметную девочку, и я поехал в университет."
    kyle "Спросил у ее одногруппницы и поехал на Блинк-роуд в ресторан. Там я ее и нашел."
    kyle @ sad "И не только ее."
    # Что произошло в ресторане?
    mc "Что произошло в ресторане?"
    jump khouse_whir

label khouse_wudssa: # Что Вы сделали, когда она перестала отвечать?
    kyle "Мне было ужасно плохо. Я себе места не находил."
    kyle @ sad "Я был ужасно зол на нее, но без нее я не мыслил своей жизни. Я хотел узнать, как прошел конкурс, но не мог. Хотел услышать ее голос, но не мог."
    kyle "Я уже точно знал, что когда вернусь, то найду ее и она станет моей женой, и я больше никогда ее не оставлю."
    # Как Вы узнали, где ее найти?
    mc "Как Вы узнали, где ее найти?"
    kyle "Не нужно быть гением криминалистики, чтоб знать о том, что если хочешь узнать что угодно о ком угодно - найди самую тихую и неприметную девочку, и я поехал в университет."
    kyle "Спросил у ее одногруппницы и поехал на Блинк-роуд в ресторан. Там я ее и нашел."
    kyle @ sad "И не только ее."
    # Что произошло в ресторане?
    mc "Что произошло в ресторане?"
    jump khouse_whir

label khouse_wuslt: # Когда Вы говорили с ней в последний раз?
    kyle "В самый последний - в ресторане, где застал ее с новым мужиком. Видно, что богатый."
    kyle "Не думал, что она так легко променяет мою любовь на деньги. Это был день, когда я вернулся с чемпионата."
    # Как Вы узнали, где ее найти?
    mc "Как Вы узнали, где ее найти?"
    kyle "Не нужно быть гением криминалистики, чтоб знать о том, что если хочешь узнать что угодно о ком угодно - найди самую тихую и неприметную девочку, и я поехал в университет."
    kyle "Спросил у ее одногруппницы и поехал на Блинк-роуд в ресторан. Там я ее и нашел."
    kyle @ sad "И не только ее."
    mc "Что произошло в ресторане?"
    jump khouse_whir

label khouse_whir: # Что произошло в ресторане?
    kyle @ sad "Я зашел туда, увидел их двоих и понял, что меня предали."
    kyle "Я точно не помню, что говорил - я был в ярости и понимал, что это конец."
    kyle "Я кинул в нее это кольцо, которое должно было стать обручальным, и уехал на наше с ней место, вспомнить как всё начиналось."
    kyle "Я так понимаю, что она в тот вечер разбила не одно сердце."
    menu:
        " "
        "Что Вы имеете в виду под этим?":
            kyle "Я надеюсь, что мое существование было сюрпризом для второго парня, иначе это совсем подлый человек. В любом случае, ее больше нет ни у кого из нас."
            mc "Где Вы были в районе полуночи в ту ночь?"
            kyle "Озеро Ист-Спринг в 15 милях отсюда."
            kyle @ sad "Вспоминал счатливые времена."
            mc "Кто-то может подтвердить то, что Вы были там?"
            kyle "Мы любили эот место за то, что оно безлюдное, так что очень сомневаюсь."
            mc "Ясно, спасибо за помощь следствию, мистер Ричардс."
            kyle "Рад помочь."
            $unlock_person("kyle")
            $character_interviewed("kyle")
            jump evidence_second_exchange
        "Где находится это 'ваше место'?":
            kyle "Озеро Ист-Спринг в 15 милях отсюда."
            mc "Кто-то может подтвердить то, что Вы были там?"
            kyle "Мы любили это место за то, что оно безлюдное, так что очень сомневаюсь."       
            mc "Ясно, спасибо за помощь следствию, мистер Ричардс."
            kyle "Рад помочь."
            $unlock_person("kyle")
            $character_interviewed("kyle")
            jump evidence_second_exchange

label evidence_exchange:
    play music "music/solving_the_crime.mp3" fadein 1.0 fadeout 1.0 loop
    scene expression im.Scale("images/locations/office.png", config.screen_width, config.screen_height) with dissolve
    show casey at sprite_left, darken
    show govard at sprite_centered, darken
    show phil at sprite_right, darken
    mc " Ладно, времени терять нечего. Разъехались, посмотрели — теперь выкладывайте."
    $ main_location = next((loc for name, loc in directions.items() if name == "jaclyn"), None)
    if main_location !="Больница":
        $location = "Больница"
        mc "Начнём с морга."
        $ assigned_person = next((name for name, loc in directions.items() if loc == location), None)
        if assigned_person == "casey":
            show casey at sprite_left, lighten
            casey "Смерть наступила около полуночи вследствие убийства. Следов сескуального насилия не обнаружено. Отпечатков также не обнаружено из-за нахождения тела в воде."
            casey "Причиной смерти является удушье, но так как в легких вода не была обнаружена, она не дышала еще до того, как оказалась в реке. Жертва была задушена собственным шарфом. Родители не захотели забирать ее вещи."
            casey "Следы гематом в районе запястий, что свидетельствует о том, что убийца был физически сильнее ее, так как этого было достаточно, чтоб ее обездвижить. Множество порезов в зоне кистей рук. Но только один из них, на безымянном пальце, был нанесен при жизни."
            $unlock_person("dr_andrews", "casey")
            show casey at sprite_left, darken
        if assigned_person == "govard":
            show govard at sprite_centered, lighten
            govard "Смерть наступила около полуночи вследствие убийства. Следов сескуального насилия не обнаружено. Отпечатков также не обнаружено из-за нахождения тела в воде."
            govard "Причиной смерти является удушье, но так как в легких вода не была обнаружена, она не дышала еще до того, как оказалась в реке. Жертва была задушена собственным шарфом. Родители не захотели забирать ее вещи."
            govard "Следы гематом в районе запястий, что свидетельствует о том, что убийца был физически сильнее ее, так как этого было достаточно, чтоб ее обездвижить. Множество порезов в зоне кистей рук. Но только один из них, на безымянном пальце, был нанесен при жизни." 
            $unlock_person("dr_andrews", "govard")
            show govard at sprite_centered, darken
        if assigned_person == "phil":
            show phil at sprite_right, lighten
            phil "Смерть наступила около полуночи вследствие убийства. Следов сескуального насилия не обнаружено. Отпечатков также не обнаружено из-за нахождения тела в воде."
            phil "Причиной смерти является удушье, но так как в легких вода не была обнаружена, она не дышала еще до того, как оказалась в реке. Жертва была задушена собственным шарфом. Родители не захотели забирать ее вещи."
            phil "Следы гематом в районе запястий, что свидетельствует о том, что убийца был физически сильнее ее, так как этого было достаточно, чтоб ее обездвижить. Множество порезов в зоне кистей рук. Но только один из них, на безымянном пальце, был нанесен при жизни."
            $unlock_person("dr_andrews", "phil")
            show phil at sprite_right, darken

        mc "С заключением ясно."

    if main_location !="Дом родителей":
        mc "Что достали ценного у родителей?"
        $ location1 = "Дом родителей"
        $ assigned_person = next((name for name, loc in directions.items() if loc == location1), None)
        if assigned_person == "casey":
            show casey at sprite_left, lighten
            casey "Мистер и миссис Лоуренс сообщили, что у их дочери был личный дневник, в котором она могла записывать важные моменты своей жизни и переживания. Также они упомянули странные звонки, которые Джейн начала получать после расставания с парнем. Один из звонков звучал так: \"Стань моей, я буду тебя любить.\""
            casey "Голос был с иностранным акцентом, и это может быть ключом к расследованию. Джейн выиграла кольцо мисс Университет, что давало ей возможность участвовать в конкурсе мисс Штат, конкурс, который когда-то не смогла выиграть её мать. Это могло быть для Джейн сильным мотивом. "
            casey "Она жила с парнем Кайлом на Марч-драйв, 77. Однажды, после ссоры, она уехала к родителям, но вернулась уже через неделю, что может свидетельствовать о сложных и нестабильных отношениях."
            $unlock_person("mr_lawrence", "casey")
            show casey at sprite_left, darken
            $unlock_person("mrs_lawrence", "casey")
        if assigned_person == "govard":
            show govard at sprite_centered, lighten
            govard "Мистер и миссис Лоуренс сообщили, что их дочь выиграла конкурс красоты и получила кольцо мисс Университет, что дало ей возможность пройти на конкурс мисс Штат. Этот конкурс когда-то не выиграла её мать, что могло быть для Джейн важной мотивацией."
            govard "Также родители сообщили о странных звонках, которые Джейн получала после расставания с парнем. Например, один из звонков был следующим: \"Стань моей, я буду тебя любить.\" Голос был с иностранным акцентом, что стоит исследовать. "
            govard "Джейн жила с парнем Кайлом на Марч-драйв, 77, и даже уезжала от него к родителям после ссоры, но вернулась через неделю. Это подтверждает, что отношения были сложными, и могут быть связаны с её смертью."
            $unlock_person("mr_lawrence", "govard")
            show govard at sprite_centered, darken
            $unlock_person("mrs_lawrence", "govard")
        if assigned_person == "phil":
            show phil at sprite_right, lighten
            phil "Из архива Джейн были извлечены фотографии, включая выпускной альбом за 4-й и 10-й классы. Эти снимки могут дать нам представление о её социальной жизни и окружении. "
            phil "Мистер и миссис Лоуренс также сообщили, что после расставания с парнем Джейн получала странные звонки. Один из них был таким: \"Стань моей, я буду тебя любить.\" Голос был с иностранным акцентом, что, вероятно, может помочь нам установить личность звонившего. "
            phil "Джейн выиграла кольцо мисс Университет, с которым должна была пройти на конкурс мисс Штат. Этот конкурс когда-то не выиграла её мать, что может объяснять дополнительные мотивы."
            phil "Джейн жила с парнем Кайлом на Марч-драйв, 77. Ругалась с ним, и однажды уехала к родителям, но через неделю вернулась, что подтверждает нестабильность её отношений."
            $unlock_person("mr_lawrence", "phil")
            show phil at sprite_right, darken
            $unlock_person("mrs_lawrence", "phil")
        mc "Ну уже есть с чем работать. Марч-Драйв 77 - запишите новый адрес, туда нужно будет отправиться."
    
    if main_location !="Университет":
        mc "Жду отчет по университету. "
        $ location2 = "Университет"
        $ assigned_person = next((name for name, loc in directions.items() if loc == location2), None)
        if assigned_person == "casey":
            show casey at sprite_left, lighten
            casey "Джуди сказала: \"Будь у меня побольше свободного времени, повод и хорошее алиби, я бы тоже с ней расправилась.\" Это звучит довольно жёстко, но, скорее всего, это просто её эмоции. "
            casey "Она также выразилась так: \"Велик ей не нравится, подавай Роллс-Ройс,\" что даёт понять, как она воспринимает людей, стремящихся к высокому статусу. Джейн, к сожалению, выиграла конкурс красоты и получила стипендию, которая вполне могла бы быть полезнее другим более нуждающимся девушкам. Титул вице-мисс Университет теперь перейдёт к Леони Джонс."
            casey "В день своей гибели Джейн была на свидании в ресторане на Блинк-роуд с парнем, который живёт на Армори-стрит, 19. Джуди также сказала: \"Джейн собиралась со своим хахалем в ресторан. Наследник папиного бизнеса — это её стиль. Жалко парня, передайте ему привет, если будете допрашивать.\" Этот парень был замечен в университете, но, увидев слежку, поспешил уйти. Всё это наводит на размышления."
            $unlock_person("judy", "casey")
            show casey at sprite_left, darken
        if assigned_person == "govard":
            show govard at sprite_centered, lighten
            govard "Про Джейн ходят слухи, что она была доступной девушкой, и это могло повлиять на её отношения с другими людьми. Джейн выиграла конкурс красоты и получила стипендию, которая могла бы гораздо больше помочь другим девушкам, которые в ней нуждаются. Семья Джейн была известна тем, что покупала ей победы на конкурсах, что ставит под сомнение её достижения."
            govard "Джуди сказала: \"Велик ей не нравится, подавай Роллс-Ройс,\" что подчёркивает её высокомерие и стремление к роскоши. Теперь титул вице-мисс Университет перейдёт к Леони Джонс."
            govard "В день смерти Джейн она была на свидании с парнем, который живёт на Армори-стрит, 19. Джуди добавила: \"Джейн собиралась со своим хахалем в ресторан. Наследник папиного бизнеса — это её стиль. Жалко парня, передайте ему привет, если будете допрашивать.\" Этот парень был замечен в университете, но, заметив слежку, поспешил уйти.\" Это выглядит крайне подозрительно."
            $unlock_person("judy", "govard")
            show govard at sprite_centered, darken
        if assigned_person == "phil":
            show phil at sprite_right, lighten
            phil "Семья Джейн неоднократно покупала ей места на конкурсах красоты, чтобы удовлетворить амбиции её матери. Джейн выиграла один из таких конкурсов, что позволило ей получить стипендию, которая, по мнению многих, могла бы достаться другим, более нуждающимся девушкам. Это только подчёркивает искусственность её успеха."
            phil "Джуди, как свидетель, использует странные аналогии, например: \"Велик ей не нравится, подавай Роллс-Ройс.\" Также стоит отметить, что теперь титул вице-мисс Университет перейдёт к Леони Джонс."
            phil "В день своей смерти Джейн была на свидании в ресторане на Блинк-роуд с парнем, который живёт на Армори-стрит, 19. Джуди добавила: \"Джейн собиралась со своим хахалем в ресторан. Наследник папиного бизнеса — это её стиль. Велик ей не нравится, подавай Роллс-Ройс. Жалко парня, передайте ему привет, если будете допрашивать.\" Этот парень был замечен в университете, но при виде наблюдения ускорил шаг и скрылся, что вызывает подозрение."
            $unlock_person("judy", "phil")
            show phil at sprite_right, darken
        mc "Судя по тому, что ее парень живет в двух местах, парень вовсе не один."

    mc "Итого у нас четыре новых точки: Марч-Драйв 77 с таинственным незнакомцем, Армори-стрит 19 с неким Кайлом, ресторан на Блинк-Роуд, где жертву вероятно видели в последний раз и проверьте мисс Джонс - у нее пока самый явный мотив."
    $ quick_menu = False
    $ renpy.block_rollback()
    $ clearDict(directions)
    call screen Map(chapter1_locs2)


label evidence_second_exchange:
    play music "music/solving_the_crime.mp3" fadein 1.0 fadeout 1.0 loop
    scene expression im.Scale("images/locations/office.png", config.screen_width, config.screen_height) with dissolve
    show casey at sprite_left, darken
    show govard at sprite_centered, darken
    show phil at sprite_right, darken
    mc "Итак, быстрый доклад."

    $ main_location = next((loc for name, loc in directions.items() if name == "jaclyn"), None)
    if main_location !="Дом на\nАрмори-стрит 19":
        $location = "Дом на\nАрмори-стрит 19"
        mc "Какие улики получены от парня жертвы?"
        show phil at sprite_right, lighten
        phil "Которого из?"
        show phil at sprite_right, darken
        mc "Армори-стрит 19. Слушаю."
        
        $ assigned_person = next((name for name, loc in directions.items() if loc == location), None)
        if assigned_person == "casey":
            show casey at sprite_left, lighten
            casey "Джеймс встречался с ней три месяца и в тот вечер собирался сделать Джейн предложение, но после скандала с бывшим оставил её одну в ресторане. Это говорит о серьёзных проблемах в отношениях, правда? Тогда когда она пожила неделю у родителей, она ушла не к Кайлу, а к Джеймсу."
            casey "И знаете, она даже не хотела знакомить его с родителями. Значит, она либо уже тогда понимала, что это ненадолго, либо не хотела портить эти отношения вмешательством матери. А еще, когда я спросила про \"привет\" от Джуди, он не понял о чем я говорю - он не знает её."
            $unlock_person("james", "casey")
            show casey at sprite_left, darken
        if assigned_person == "govard":
            show govard at sprite_centered, lighten
            govard "Майерс собирался сделать ей предложение, но в итоге после скандала с ее бывшим бросил её одну в ресторане. Они встречались три месяца, познакомились случайно, она к нему подсела в заведении. Я бы тоже вряд ли хотел себе в жены подобную даму. То, когда она пожила неделю у родителей, она потом ушла не к бывшему, а к Майерсу. По датам сошлось."
            govard "Но вот что важнее — отсутствие алиби, он говорит, что никто его не видел, когда он ушел из ресторана. Он даже не удосужился придумать, где был. Это повод присмотреться к нему серьёзнее. А еще он не понял, почему универская зануда просила ему передать привет - он ее даже не знает."
            $unlock_person("james", "govard")
            show govard at sprite_centered, darken
        if assigned_person == "phil":
            show phil at sprite_right, lighten
            phil "Согласно данным, Джеймс Майерс планировал сделать предложение спустя три месяца отношений, но после конфликта с ее бывшим молодым человеком оставил Джейн одну в ресторане. Это демонстрирует нестабильность в их взаимодействии. Примечательно также, что после недели у родителей она переехала к новому парню, что свидетельствует о завершении их отношений."
            phil "Они встречались всего три месяца, познакомились в кофейне — довольно типичная история. Однако, учитывая выгорание Джеймса и его стремление найти 'новые ощущения' в отношениях с молодой девушкой, можно предположить, что для него это было скорее бегство от внутреннего кризиса. Кстати, он утверждает, что не знает Джуди, что может быть правдой, но это ещё нужно проверить."
            $unlock_person("james", "phil")
            show phil at sprite_right, darken
        mc "Это озеро Ист-Спринг как-то связано с рекой, откуда выловили жертву?"
        show casey at sprite_left, lighten
        casey "Она впадает туда"
        show casey at sprite_left, darken

    if main_location !="Дом на\nМарч-драйв 77":
        $location1 = "Дом на\nМарч-драйв 77"
        mc "Что узнали от второго парня?"
        $ assigned_person = next((name for name, loc in directions.items() if loc == location1), None)
        if assigned_person == "casey":
            show casey at sprite_left, lighten
            casey "Они встречались с самого школьного возраста и были вместе четыре года, но когда Джейн пережила нервный срыв из-за конкурса красоты в отсутствие Кайла, отношения начали рушиться. Когда Кайл поехал на чемпионат по футболу, она восприняла это как предательство, ведь она нуждалась в нём больше, чем когда-либо."
            casey "После этого она уехала к своим родителям, но он не попытался с ними связаться, так как у него не было их номеров. С того времени она не вернулась к нему. Кайл решил найти её через Джуди из университета и поехал делать ей предложение, но было ли поздно? После инцидента в ресторане, который, видимо, сильно повлиял на его эмоции, он поехал на озеро Ист-Спринг."
            $unlock_person("kyle", "casey")
            show casey at sprite_left, darken
        if assigned_person == "govard":
            show govard at sprite_centered, lighten
            govard "Кайл был защитником Джейн на протяжении четырёх лет их отношений, оберегая её от многолетнего сталкерства со стороны других парней. После инцидента в ресторане, который, видимо, сильно повлиял на его эмоции, он поехал на озеро Ист-Спринг. "
            govard "Важно отметить, что когда Джейн ушла от него после того, как он уехал на чемпионат по футболу, он не попытался связаться с её родителями, так как у него нет их номеров. Эти детали важно учитывать. Он был всё-таки её защитником, но, видимо, в какой-то момент потерял связь с реальностью."
            $unlock_person("kyle", "govard")
            show govard at sprite_centered, darken
        if assigned_person == "phil":
            show phil at sprite_right, lighten
            phil "Джейн пережила тиранию со стороны своей матери в детстве, что могло сильно повлиять на её восприятие отношений и чувствительность к предательству. В связи с этим важно отметить, что её отношения с Кайлом развивались на фоне её внутренней борьбы с этим прошлым. Когда Кайл уехал на чемпионат по футболу, Джейн восприняла это как предательство и ушла к родителям."
            phil "При этом Кайл не пытался связаться с её родителями, так как у него не было их номеров. После этого он решил найти её через Джуди из университета и поехал делать предложение, что также стоит учитывать в контексте её переживаний и его действий. После инцидента в ресторане, который, видимо, сильно повлиял на его эмоции, он поехал на озеро Ист-Спринг."
            $unlock_person("kyle", "phil")
            show phil at sprite_right, darken


    if main_location !="Ресторан на\nБлинк-роуд":
        $location2 = "Ресторан на\nБлинк-роуд"
        mc "Есть новости из ресторана?"
        $ assigned_person = next((name for name, loc in directions.items() if loc == location2), None)
        if assigned_person == "casey":
            show casey at sprite_left, lighten
            casey "Это так романтично — Джейн хотели сделать предложение! Но всё сорвалось… Кольцо должно было быть спрятано в десерте, но его даже не использовали. А потом ещё эта ужасная кража кольца у миссис Веласкес… Интересно, как она себя чувствует? "
            casey "Представляете, даже её сын не знает, что это была копия! Спутник Джейн ушёл один сразу после скандала. Наверное, он был сильно расстроен. А человек, который сорвал предложение, тоже был с кольцом… Думаю, это был бывший, это так… трагично, если правда."
            $unlock_person("mrs_velaskez", "casey")
            show casey at sprite_left, darken
            $unlock_person("lisa", "casey")#!!!
        if assigned_person == "govard":
            show govard at sprite_centered, lighten
            govard "Джейн собирались сделать предложение, но всё пошло наперекосяк. Кольцо, которое официантка должна была спрятать в десерте, так и не понадобилось. Ситуация осложняется ещё и тем, что у владелицы ресторана, миссис Веласкес, пропало кольцо — копия семейной реликвии. Забавно, что даже её сын не знает, что это всего лишь копия."
            govard "Я запросил список сотрудников ресторана. Будем разбираться, кто мог замешан быть в этой кражи. Ну и важный момент: тот, кто сорвал предложение, сам был с кольцом. Ставлю на бывшего парня Джейн. Они же вечно приходят, когда не надо."
            $unlock_person("mrs_velaskez", "govard")
            show govard at sprite_centered, darken
            $unlock_person("lisa", "govard")#!!!
        if assigned_person == "phil":
            show phil at sprite_right, lighten
            phil "Изначальный план включал спрятанное в десерте кольцо, но предложение сорвалось. Это уже создаёт эмоционально насыщенную обстановку, типичную для таких ситуаций. Примечательно, что у владелицы ресторана, миссис Веласкес, украли кольцо, являющееся копией семейной реликвии. Забавно, что её сын не знает, что это подделка — возможно, её мотивы стоит изучить."
            phil "На кухне недавно уволили сотрудника за воровство, что может быть связано с пропажей кольца. Также важная деталь: человек, который сорвал предложение, был с кольцом. Это, скорее всего, бывший партнёр Джейн, что могло быть мотивом его вмешательства."
            $unlock_person("mrs_velaskez", "phil")
            show phil at sprite_right, darken
            $unlock_person("lisa", "phil")#!!!

    mc "Так, теперь у нас есть немного времени изучить все улики и составить обвинение. Оно должно быть подкреплено уликами, а не случайно. "
    mc "После этого мы выезжаем к одному из свидетелей, чтобы подтвердить свои догадку и выйти на убийцу. Кто-то из них знает больше, чем сказал. Может, осознанно врёт, может, сам не понимает, что держит ключ к делу. Но именно там мы сможем подтвердить или опровергнуть наши догадки.И этот выбор решит, доберёмся ли мы до убийцы."

    $ quick_menu = True
    # $ renpy.block_rollback()
    $ clearDict(directions)
    hide casey
    hide govard
    hide phil
    jump choose_suspect
    return


label choose_suspect:
    $ quick_menu = True
    $ renpy.block_rollback()
    # $ selected = call screen Choose_suspect()

    $ selected = None
    call screen Choose_suspect()
    $ selected = _return
    if selected == "lewis":
        jump chapter1_good_end
    else:
        $ suspects_order = ["james", "kyle", "lewis"]
        $ show_window = False
        $ transform_to_use = None
        $ selected = None
        $ selected_suspect = None
        jump chapter1_wrong_end

label chapter1_good_end:
    $ renpy.block_rollback()

    scene expression im.Scale("images/locations/right_end.png",
        config.screen_width, config.screen_height) with dissolve

    "Ещё со школы Луис Веласкес был влюблён в Джейн и следил за ней - об этом писала сама Джейн в дневнике. «Вечно где-то рядом: у колледжа, у дома, даже когда я с подругами иду за кофе. Он думает, что если будет везде появляться, то я “передумаю”»"
    "Он устроился помощником к матери в ресторан, где позже Джейн ужинала с Джеймсом Майерсом. Когда увидел её вместе с другим - в тот день, когда Майерс готовил предложение, - в нём сорвало предохранитель. Он украл из материнской шкатулки копию фамильного кольца и отправился за Джейн. "
    "После ухода Майерса он перехватил её у чёрного входа ресторана, встал на одно колено и в третий раз за день предложил ей выйти замуж. Получив отказ, он сорвал кольцо ей с пальца, поцарапав безымянный, и шепнул: «Теперь шрам останется навсегда». Когда Джейн закричала, он задушил её шарфом и сбросил тело в реку. Задолго до этого родители Джейн получили звонок: «Стань моей… я буду тебя любить…». Голос с испанским акцентом записался на автоответчик."
    
    "Его нашли через сравнение показаний в дневнике и университетских фотоальбомов: кучерявый «Велик» из списка сотрудников совпал с одноклассником Джейн. При задержании в кармане нашли украденное кольцо и мобильник с несколькими черновиками звонков на номер Лоуренсов. Дело Джейн Лоуренс закрыто. Наконец найден тот, кому Джуди просила передать “привет”."
    $ togle_first_try(True)
    scene expression im.Scale("images/locations/right_end_busted.jpg",
        config.screen_width, config.screen_height) with dissolve
    "Справедливость восторжествовала."
    $ unlock_achievement( "acquaintances", "1.2", "Вы получили достижение!")
    
    

    return


label chapter1_wrong_end:
    $ renpy.block_rollback()

    scene expression im.Scale("images/locations/right_end.png",
        config.screen_width, config.screen_height) with dissolve

    "Обвинение оказалось ошибочным."
    $ unlock_achievement( "acquaintances", "1.3", "Вы получили достижение!")

    scene expression im.Scale("images/locations/wrong_end.png",
        config.screen_width, config.screen_height) with dissolve

    "Убийца все еще на свободе."
    $togle_first_try()
    call screen SuspectAccuseRetryConfirm
    return




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