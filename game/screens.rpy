################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    unscrollable "hide"
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_idle_bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_idle_thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    # base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    # thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    unscrollable "hide"
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_idle_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_idle_thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    # base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    # thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style text:
    color "#D9D9D9"

################################################################################
## In-game screens
################################################################################

### Map Screen ##################################################################
##
##############
screen unlock_notification(name, image_path):
    zorder 200  # поверх всего
    frame:
        at notif_slide
        xalign 0.5
        yalign 0.01  # сверху по центру
        background Frame("gui/button/1111choice_idle_background.png", 10, 10)
        padding (20, 20)
        xmaximum 700
        yminimum 0
        xfill False

        hbox:
            spacing 10
            add Transform(image_path, xysize=(70, 70), fit="contain")
            text f"Добавлена информация: {{b}}{name}!{{/b}}":
                color "#ffffff"
                size 26
                # bold True
                xalign 0.5
                yalign 0.5
                outlines [(1, "#000", 0, 0)]

    # автоматическое скрытие через 2.5 секунды
    timer 2.5 action Hide("unlock_notification")

transform notif_slide:
    yoffset -100
    alpha 0.0
    easein 0.4 yoffset 0 alpha 1.0
    pause 2.0
    easeout 0.4 alpha 0.0

screen unlock_notification_achievement(message, title, currentImage):
    zorder 1100  # поверх всего
    frame:
        at notif_slide
        xalign 0.5
        yalign 0.01  # сверху по центру
        background Frame("gui/button/1111choice_idle_background.png", 10, 10)
        padding (20, 20)
        xmaximum 700
        yminimum 0
        xfill False

        hbox:
            spacing 20
            add Transform(currentImage, xysize=(70, 70), fit="contain")
            text f"Получено достижение: {{b}}{title}{{/b}}!":
                color "#ffffff"
                size 26
                # bold True
                xalign 0.5
                yalign 0.5
                outlines [(1, "#000", 0, 0)]

    # автоматическое скрытие через 2.5 секунды
    timer 2.5 action Hide("unlock_notification")

init python:
    def unlock_person(key, from_ch=""):
        """
        Разблокирует персонажа и показывает кастомное уведомление
        с его именем из словаря persons.
        """
        if key in persons:
            person = persons[key]
            person["locked"] = False
            person["from"] = from_ch
            person_name = person.get("name", key)
            image_path = person.get("image_path", None)

            if image_path:
                renpy.show_screen("unlock_notification", name=person_name, image_path=image_path)
            else:
                renpy.notify(f"Добавлено досье о {person_name}!")
        else:
            renpy.notify(f"Персонаж '{key}' не найден.")
    
    def unlock_clue(key):
        """
        Разблокирует улику и показывает кастомное уведомление
        с его именем из словаря clue.
        """
        if key in clues:
            clue = clues[key]
            clue["locked"] = False
            clue_name = clue.get("name", key)
            image_path = clue.get("image_path", None)
            unlocked_clues.append(clue)

            if image_path:
                renpy.show_screen("unlock_notification", name=clue_name, image_path=image_path)
            else:
                renpy.notify(f"Добавлена новая улика: {clue_name}!")
        else:
            renpy.notify(f"Улика '{key}' не найдена.")


init python:
    def setLocation(dict, person, location):
        # print(person, location)
        """
            Set location in the dictionary. This also removes all the same locations of other persons in the dict.
        """
        dict[person] = location
        for key in dict.keys():
            print(key)
            if key != person and dict[key] == location:
                dict[key] = ""
    
    def clearDict(dict):
        """
            This clears all keys' values and sets the to empty strings
        """
        for key in dict.keys():
            dict[key] = ""

    def all_active_locations_assigned(locs, directions):
        """
        Проверяет, что каждая активная локация занята хотя бы одним агентом.
        locs = список локаций chapter1_locs1 или chapter1_locs2
        directions = словарь вида {agent : location_name}
        """
        active_locations = [loc[2] for loc in locs if loc[3] == True]

        assigned_locations = directions.values()

        for loc_name in active_locations:
            if loc_name not in assigned_locations:
                return False
        
        return True


screen map_frame(locs):
    frame:
        xsize 1830
        ysize 715
        background "images/map/map.png"
        xalign 0.5
        yalign 0.6   

        for loc in locs:
            use map_dot(loc[0], loc[1], loc[2], loc[3], loc[4], loc[5])

screen map_loc(x, y, name, image_path = None):
    frame:
        background "images/map/dot_loc.png"
        pos(x, y)
        image image_path:
        # image "images/map/test.png":
            xpos 14
            ypos 11

    use map_name(x + 90, y, name)

screen map_name(x, y, name):
    frame:
        xsize 200
        ysize 100
        background "images/map/dot_name.png"
        pos(x, y)
        text _(name):
            size(20)
            bold(True)
            color("#000000")
            xalign 0.5
            yalign 0.5

screen map_dot(x, y, name, active, image_path = None, is_accessible_mc = True):
    imagebutton:
        xpos x
        ypos y 
        if active:
            idle "images/map/dot_idle.png"
            hovered [Play("sound", map_hover_sound), Show("map_loc", x = x+17, y= y+103, name=name, image_path=image_path)]
            unhovered Hide("map_loc")
            hover "images/map/dot_hover.png"
            if not is_accessible_mc:
                if selected_person != "jaclyn":
                    action [Play("sound", button_click), Function(setLocation, directions, selected_person, name), SetVariable("selected_person", "")]
            else:
                action [Play("sound", button_click), Function(setLocation, directions, selected_person, name), SetVariable("selected_person", "")]
            # SetDict(directions, selected_person, name)
            # setLocation(directions, selected_person, name)
        else:
            idle "images/map/dot_inactive.png"

default persons = {
    "james": {"name":"Джеймс Майерс","image_path":"images/scaled_characters/scene_characters/james.png", "description": "Сожитель Джейн. Привык получать всё без усилий, но внутри чувствует пустоту. Ищет чувство нужности через отношения. Прожигает жизнь, находя легкие удовольствия.", "locked": True, "from":"" },
    "kyle": {"name":"Кайл Ричардс","image_path":"images/scaled_characters/scene_characters/kyle.png", "description": "Бывший парень Джейн. Талантливый футболист, стремящийся монетизировать свою спортивную карьеру. Сомневается в себе из-за чувства финансовой несостоятельности.", "locked": True, "from":"" },
    "lisa": { "name":"Лиза","image_path":"images/scaled_characters/scene_characters/lisa.png","description": "официантка, 20-22 года, стройная, высокая девушка, собранные темно-русые волосы. Апатичная и уставшая от работы. ", "locked": True, "from":"" },
    "mr_lawrence": { "name":"Мистер Лоуренс","image_path":"images/scaled_characters/scene_characters/mr_lawrence.png", "description": " Отец Джейн Лоуренс, привыкший жить по расписанию бизнеса. Спокоен, редко показывает эмоции. В семье скорее наблюдатель, чем участник.", "locked": True , "from":""},
    "mrs_lawrence": { "name":"Миссис Лоуренс","image_path":"images/scaled_characters/scene_characters/mrs_lawrence.png", "description": "Мать Джейн Лоуренс. Стремится выглядеть моложе, чем есть, и всегда держит лицо победительницы. Резка, контролирующая, склонна к драматизации.", "locked": True ,  "from":""},
    "mrs_velaskez": { "name":"Миссис Веласкес","image_path":"images/scaled_characters/scene_characters/mrs_velaskez.png", "description": "Шеф-повар и владелица ресторана. Властная и громкая женщина, привыкшая командовать кухней и людьми. Любит давить авторитетом и не терпит возражений.", "locked": True, "from":"" },
    "dr_andrews":{"name":"Доктор Эндрюс", "image_path":"images/scaled_characters/scene_characters/dr_andrews.png", "description":"Спокойный, опытный и немного ворчливый патологоанатом. Предпочитает иронию серьезности и часто добродушно язвит над детективами. На удивление еще не разочарован в этом мире.", "locked": True, "from":"" },
    "judy":{"name":"Джуди", "image_path":"images/scaled_characters/scene_characters/judy.png", "description":"Любит собирать слухи и анализировать людей, что делает её ценным, хотя и не всегда приятным собеседником. Часто держится отстранённо, будто выше происходящего.", "locked": True, "from":"" },
    "lewis":{"name":"Луис Веласкес", "image_path":"images/scaled_characters/scene_characters/lewis.png", "description":"Щуплый, нервный парень с латинскими корнями. Выглядит младше своего возраста, но компенсирует это резкими реакциями и стремлением казаться смелее, чем есть.", "locked": True, "from":"" },
    "lisa":{"name":"Лиза", "image_path":"images/scaled_characters/scene_characters/lisa.png", "description":"Тихая и эмоционально выгоревшая официантка. Делает свою работу механически, пытаясь оставаться незаметной и не вовлекаться в чужие драмы.", "locked": True, "from":"" }
}
default main_characters = {
    "jaclyn" : {"name":"Жаклин Картер", "image_path":"images/scaled_characters/main_characters/jaclyn.png", "description":"Старший агент, чья хладнокровная собранность позволяет ей удерживать команду в рамках и вести расследование чётко и жёстко."},
    "casey" : {"name":"Кейси Айронс", "image_path":"images/scaled_characters/main_characters/casey.png", "description":"Мягкий эмпат, легко находящий общий язык с родственниками жертвы и тонко улавливающий эмоции, от которых сама нередко страдает."},
    "govard" : {"name":"Говард Браун", "image_path":"images/scaled_characters/main_characters/govard.png", "description":"Мощная силовая опора, чья прямота и резкость особенно эффективны в разговорах с подозреваемыми, привыкшими давить на окружающих."},
    "phil" : {"name":"Фил Моррисон", "image_path":"images/scaled_characters/main_characters/phil.png", "description":"Аналитический ум команды, погружённый в отчёты, экспертизы и улики, благодаря чему он замечает то, что остальные могли бы упустить."}
}

default clues = {
    "ring" : {
        "name": "Кольцо Миссис Веласкес", 
        "image_path": "images/clues/ring.png",
        "description": "Массивное золотое кольцо с рубином, обычно лежащее на рабочем столе в кабинете Миссис Веласкес. Не обладая высокой стоимостью, оно ценно как семейная реликвия, передаваемая по женской линии из поколения в поколение.",
        "locked": True
    },
    "adult_album" : {
        "name": "Выпускной альбом 10 класс", 
        "image_path": "images/clues/adult_album.png",
        "description": "Имена: \nДжейн Лоуренс \nЛуис Веласкес \nЛили Морган...",
        "locked": True
    },
    "victim_photo" : {
        "name": "Фото Жертвы", 
        "image_path": "images/clues/victim_photo.png",
        "description": "Победительница конкурса «Мисс Университет»: жертва с именным кольцом и короной, подтверждающими главный приз и право участия в «Мисс Штат». Победу многие считали купленной и незаслуженной.",
        "locked": True
    },
    "corpse" : {
        "name": "Фото с места преступления", 
        "image_path": "images/clues/corpse.png",
        "description": "Первые кадры, сделанные после обнаружения тела на берегу реки. Тело обнаружила случайная прохожая, выгуливавшая собаку, после того как его вынесло течением к берегу.",
        "locked": True
    },
    "workers_list" : {
        "name": "Список сотрудников", 
        "image_path": "images/clues/workers_list.png",
        "description": "Служебный документ с перечнем персонала ресторана Миссис Веласкес. В нём указаны имена работников, их должности, а также время и продолжительность рабочих смен.",
        "locked": True
    },
    "hands" : {
        "name": "Фото порезов на руках", 
        "image_path": "images/clues/hands.png",
        "description": "Кисти жертвы, покрытые множественными порезами по всей поверхности, включая пальцы. В ходе судебно-медицинского осмотра установлено, что самый глубокий порез расположен на левом безымянном пальце.",
        "locked": True
    },
    "diary" : {
        "name": "Личный дневник", 
        "image_path": "images/clues/diary.png",
        "description": "Розовая записная книжка жертвы, где она хранила свои личные записи о повседневной жизни и переживаниях, отражающие сложное эмоциональное состояние.",
        "locked": True
    },
    "kid_album" : {
        "name": "Выпускной альбом 4 класс", 
        "image_path": "images/clues/kid_album.png",
        "description": "Имена: \nДжейн Лоуренс \nЛуис Веласкес \nЭшли Картер...",
        "locked": True
    },
    "clothes" : {
        "name": "Фото одежды жертвы", 
        "image_path": "images/clues/clothes.jpg",
        "description": "Одежда, в которой была найдена жертва. Сумка с личными вещами, которая была при жертве в день убийства, так и не была найдена.",
        "locked": True
    },
    "hospital1" : {
        "name": "Запись из больницы",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Смерть наступила от удушения, но в легких нет воды.\nШарф жертвы - орудие убийства.",
        "locked": True
    },
    "hospital2" : {
        "name": "Запись из больницы",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Только один из порезов на руках был сделан при жизни девушки - тот, что на безымянном пальце.\nНет следов сексуального насилия.",
        "locked": True
    },
    "parents_house1_1" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Родители Джейн получали странные звонки после расставания 'Стань моей, я буду тебя любить' от парня с иностранным говором",
        "locked": True
    },
    "parents_house1_2" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн выиграла кольцо мисс Университет, с которым должна была пройти на конкурс мисс Штат, который когда-то не выиграла ее мать",
        "locked": True
    },
    "parents_house2_1" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Родители сказали, что со своего совершеннолетия Джейн жила с парнем Кайлом на Марч-драйв 77",
        "locked": True
    },
    "parents_house2_2" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн часто ругалась со своим парнем и даже однажды уехала от него к родителям, но уже через неделю вернулась",
        "locked": True
    },
    "parents_house_black" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Мистер и Миссис Лоуренс сожалеют о невыигранных конкурсах, а не о потере дочери.",
        "locked": True
    },
    "university1" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Леони Джонс стала вице-мисс Университет, и теперь титул и награда перейдут ей",
        "locked": True
    },
    "university2_1" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Цитата Джуди - 'Собиралась со своим хахалем в ресторан на Блинк-роуд. Наследник папиного бизнеса - всё как она любит.'",
        "locked": True
    },
    "university2_2" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "'Велик ей не нравится, подавай Роллс-Ройс.'",
        "locked": True
    },
    "university3" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн была в вечер смерти на свидании в ресторане на Блинк-роуд со своим парнем, который живет на Армори-стрит 19”",
        "locked": True
    },
    "university4" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Парня, которому Джуди хотела передать привет, видели в университете, но он ускорил шаг и ушел.",
        "locked": True
    },
    "university_phil" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Семья девушки покупала ей места на конкурсах красоты для удовлетворения амбиций матери",
        "locked": True
    },
    "university_casey" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Цитата Джуди - 'Будь у меня побольше свободного времени, повод и хорошее алиби, я бы тоже с ней расправилась'",
        "locked": True
    },
    "restaurant1" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн собирались сделать предложение, но оно сорвалось\nЧеловек, который сорвал предложение, тоже был с кольцом",
        "locked": True
    },
    "restaurant2_1" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У владелицы ресторана Миссис Веласкес украли кольцо - копию семейной реликвии,",
        "locked": True
    },
    "restaurant2_2" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "но даже ее сын не знает, что это копия.",
        "locked": True
    },
    "restaurant_casey" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Спутник ушел один сразу после скандала.",
        "locked": True
    },
    "restaurant_phil" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Недавно был уволен работник кухни за воровство, хотя он так и не признал это.",
        "locked": True
    },
    "james_house1" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джеймс собирался сделать предложение, но после скандала оставил ее одну в ресторане",
        "locked": True
    },
    "james_house2_1" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "После недели жизни у родителей она уехала не к бывшему, а к Джеймсу\nДжейн и Джеймс встречались 3 месяца",
        "locked": True
    },
    "james_house2_2" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джеймс не знает Джуди",
        "locked": True
    },
    "james_house_govard" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У Джеймса отсутствует алиби.",
        "locked": True
    },
    "james_house_casey" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн не хотела знакомить Джеймса с родителями.",
        "locked": True
    },
    "james_house_phil" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джеймс выгорел от жизни и просто искал новых ощущений и тепла от молоденькой девочки.",
        "locked": True
    },
    "kyle_house1_1" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Бывший парень Джейн поехал на озеро Ист-Спринг после инцидента в ресторане, но никто не может это подтвердить",
        "locked": True
    },
    "kyle_house1_2" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "3-4 месяца назад Кайл уехал на чемпионат по футболу и Джейн восприняла это как предательство",
        "locked": True
    },
    "kyle_house2_1" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Кайл смог найти Джейн с помощью Джуди и поехал делать ей предложение - тогда они увиделись впервые после его отъезда",
        "locked": True
    },
    "kyle_house2_2" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У Кайла нет контактов родителей Джейн",
        "locked": True
    },
    "kyle_house_govard" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Кайл был защитником безопасности Джейн от многолетнего сталкерства со стороны парней.",
        "locked": True
    },
    "kyle_house_casey" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У Джейн был нервный срыв из-за конкурса красоты в отсутствие Кайла.",
        "locked": True
    },
    "kyle_house_phil" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн с детства терпела тиранию и контроль со стороны матери.",
        "locked": True
    },
    "hospital_mc1" : {
        "name": "Запись из больницы",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Смерть наступила от удушения, но в легких нет воды.\nШарф жертвы - орудие убийства.",
        "locked": True
    },
    "hospital_mc2" : {
        "name": "Запись из больницы",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Шарф жертвы - орудие убийства.",
        "locked": True
    },
    "hospital_mc3" : {
        "name": "Запись из больницы",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Только один из порезов на руках был сделан при жизни девушки - тот, что на безымянном пальце.",
        "locked": True
    },
    "hospital_mc4" : {
        "name": "Запись из больницы",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Нет следов сексуального насилия.",
        "locked": True
    },
    "parents_house_mc1" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Родители Джейн получали странные звонки после расставания 'Стань моей, я буду тебя любить' от парня с иностранным говором.",
        "locked": True
    },
    "parents_house_mc2" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн выиграла кольцо мисс Университет, с которым должна была пройти на конкурс мисс Штат, который когда-то не выиграла ее мать.",
        "locked": True
    },
    "parents_house_mc3" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Родители сказали, что со своего совершеннолетия Джейн жила с парнем Кайлом на Марч-драйв 77.",
        "locked": True
    },
    "parents_house_mc4" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн часто ругалась со своим парнем и даже однажды уехала от него к родителям, но уже через неделю вернулась.",
        "locked": True
    },
    "parents_house_mc5" : {
        "name": "Запись из дома родителей",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Мистер и Миссис Лоуренс сожалеют о невыигранных конкурсах, а не о потере дочери.",
        "locked": True
    },
    "university_mc1" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Семья девушки покупала ей места на конкурсах красоты для удовлетворения амбиций матери.",
        "locked": True
    },
    "university_mc2" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Цитата Джуди - “Будь у меня побольше свободного времени, повод и хорошее алиби, я бы тоже с ней расправилась”",
        "locked": True
    },
    "university_mc3" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "О Джейн ходит слава доступной девушки.",
        "locked": True
    },
    "university_mc4" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Леони Джонс стала вице-мисс Университет, и теперь титул и награда перейдут ей.",
        "locked": True
    },
    "university_mc5" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн была в вечер смерти на свидании в ресторане на Блинк-роуд со своим парнем, который живет на Армори-стрит 19”",
        "locked": True
    },
    "university_mc6" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Цитата Джуди - 'Собиралась со своим хахалем в ресторан на Блинк-роуд. Наследник папиного бизнеса - всё как она любит. Велик ей не нравится, подавай Роллс-Ройс. Жалко парня, передайте ему привет, если будете допрашивать.'",
        "locked": True
    },
    "university_mc7" : {
        "name": "Запись из университета",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Парня, которому Джуди хотела передать привет, видели в университете, но он ускорил шаг и ушел.",
        "locked": True
    },
    "restaurant_mc1" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Спутник ушел один сразу после скандала.",
        "locked": True
    },
    "restaurant_mc2" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Человек, который сорвал предложение, тоже был с кольцом.",
        "locked": True
    },
    "restaurant_mc3" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Недавно был уволен работник кухни за воровство, хотя он так и не признал это.",
        "locked": True
    },
    "restaurant_mc4" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн собирались сделать предложение, но оно сорвалось.",
        "locked": True
    },
    "restaurant_mc5" : {
        "name": "Запись из ресторана",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У владелицы ресторана Миссис Веласкес украли кольцо - копию семейной реликвии, но даже ее сын не знает, что это копия.",
        "locked": True
    },
    "kyle_house_mc1" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Кайл был защитником безопасности Джейн от многолетнего сталкерства со стороны парней.",
        "locked": True
    },
    "kyle_house_mc2" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У Джейн был нервный срыв из-за конкурса красоты в отсутствие Кайла.",
        "locked": True
    },
    "kyle_house_mc3" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн с детства терпела тиранию и контроль со стороны матери.",
        "locked": True
    },
    "kyle_house_mc4" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Бывший парень Джейн поехал на озеро Ист-Спринг после инцидента в ресторане, но никто не может это подтвердить.",
        "locked": True
    },
    "kyle_house_mc5" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "3-4 месяца назад Кайл уехал на чемпионат по футболу и Джейн восприняла это как предательство.",
        "locked": True
    },
    "kyle_house_mc6" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Кайл смог найти Джейн с помощью Джуди и поехал делать ей предложение - тогда они увиделись впервые после его отъезда.",
        "locked": True
    },
    "kyle_house_mc7" : {
        "name": "Запись из дома Кайла",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У Кайла нет контактов родителей Джейн.",
        "locked": True
    },
    "james_house_mc1" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "У Джеймса отсутствует алиби.",
        "locked": True
    },
    "james_house_mc2" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн не хотела знакомить Джеймса с родителями.",
        "locked": True
    },
    "james_house_mc3" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джеймс выгорел от жизни и просто искал новых ощущений и тепла от молоденькой девочки.",
        "locked": True
    },
    "james_house_mc4" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джеймс собирался сделать предложение, но после скандала оставил ее одну в ресторане.",
        "locked": True
    },
    "james_house_mc5" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "После недели жизни у родителей она уехала не к бывшему, а к новому парню.",
        "locked": True
    },
    "james_house_mc6" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джейн и Джеймс встречались 3 месяца.",
        "locked": True
    },
    "james_house_mc7" : {
        "name": "Запись из дома Джеймса",
        "image_path" : "images/clues/pencil.jpg",
        "description" : "Джеймс не знает Джуди.",
        "locked": True
    }
}
default unlocked_clues = [] # List of unlocked clues, for sorting in notebook

default selected_person = ""
default directions = {
    "" : "",
    "jaclyn" : "",
    "casey" : "",
    "govard" : "",
    "phil" : ""
}

define rus_to_eng_locs = {
    "Дом родителей" : "parents_house",
    "Больница" : "hospital",
    "Университет" : "university",
    "Дом Леони\nДжонс" : "leoni's_house",
    "Ресторан на\nБлинк-роуд" : "restaurant",
    "Дом на\nАрмори-стрит 19" : "james_house",
    "Полиция" : "police_station",
    "Дом на\nМарч-драйв 77" : "kyle_house"
}


define locations = {
    "Дом родителей" : "images/map/chapter1/parent_house.png",
    "Больница" : "images/map/hospital.png",
    "Университет" : "images/map/chapter1/university.png",
    "Дом Леони\nДжонс" : "images/map/chapter1/parent_house.png",
    "Ресторан на\nБлинк-роуд" : "images/map/chapter1/restaurant.png",
    "Дом на\nАрмори-стрит 19" : "images/map/chapter1/bf_house.png",
    "Полиция" : "",
    "Дом на\nМарч-драйв 77" : "images/map/chapter1/ex_house.png"

}

screen person(name):
    hbox:
        imagebutton:
            if selected_person == name:
                idle "images/map/" + name + "_selected.png"
                action [Play("sound", button_click), SetVariable("selected_person", "")]
            else:
                idle "images/map/" + name + "_idle.png"
            action [Play("sound", button_click), SetVariable("selected_person", name)]
            # action NullAction()
        if directions[name] == "":
            image "images/map/not_selected.png":
                yalign 1.0
                xpos -55
                # xalign 0.8
        else:
            image locations[directions[name]]:
                yalign 1.0
                xpos -55

screen confirm_map_button(locs):
    imagebutton:
        xalign 0.5
        yalign 0.97
        idle "images/map/confirm.png"
        action If(
            all_active_locations_assigned(locs, directions),
            true = [SetVariable("quick_menu", True), Jump(rus_to_eng_locs.get(directions["jaclyn"], "fallback_label"))],
            false = Notify("Каждая открытая локация должна быть занята агентом!")
        )


screen notebook_icon():
    imagebutton:
            xalign 0.998
            ypos 56
            idle "images/map/notebook.png"
            hover "images/map/notebook_selected.png"
            action [Play("sound", button_click), ToggleScreen("Notebook")]

screen Map(locs):
    add "images/map/background.png"

    # text (selected_person)
    # text (directions["casey"])

    imagebutton:
        xpos 15
        ypos 15
        auto "gui/quickMenu/settings_%s.png" 
        hovered [Play("sound", button_menu_hovered)]
        action [Play("sound", button_click), ShowMenu("preferences")]

    use notebook_icon    

    hbox:
        xalign 0.5
        ypos 25
        spacing 20
        use person("jaclyn")
        use person("casey")
        use person("govard")
        use person("phil")
        

        vbox:
            xsize 640
            text _("НА КАЖДУЮ ЛОКАЦИЮ ДОЛЖЕН БЫТЬ ОТПРАВЛЕН ТОЛЬКО 1 АГЕНТ. НЕ ЗАДЕЙСТВОВАННЫЕ ЧЛЕНЫ КОМАНДЫ ОСТАЮТСЯ В УЧАСТКЕ ВЕСТИ ДОКУМЕНТАЦИЮ ДЕЛА."):
                ypos 20
                size(24)
                font "fonts/Philosopher-BoldItalic.ttf"

    use map_frame(locs)

    # use confirm_map_button
    use confirm_map_button(locs)


## Notebook Screen ##############################################################
##
## The notebook screen with all the clues and characters
## 
## For Persons file assuming only 6 files per page.
##
init python:
    def frame_with_image(image_path, name):
        return Frame("images/notebook/photo_frame.png", 10, 10, tile=False), image_path, name


screen from_icon(from_name, size=42):
    if from_name:
        fixed:
            xsize size
            ysize size
            align (1.2, -0.1)
            offset (-6, -6)
            add Transform(
                "images/map/%s_idle.png" % from_name,
                xysize=(size, size)
            )
            add Transform(
                "images/map/black_boder.png",
                xysize=(size, size)
            )
        
default cur_notebook_screen = "title"
default cur_page = 0 # Counter for displaying notebook page

screen Notebook:
    modal True
    frame:
        xsize 1201
        ysize 977
        xalign 0.5
        yalign 0.55
        if cur_notebook_screen == "persons" and cur_page % 2 == 1:
            background "images/notebook/notebook_bg_dirty1.png"
        elif cur_notebook_screen == "clues" and cur_page % 2 == 1:
            background "images/notebook/notebook_bg_dirty2.png"
        else: 
            background "images/notebook/notebook_bg.png"

        button:
            xpos 990
            ypos 30
            xsize 60
            ysize 200
            background Transform("images/notebook/closeNotebookBut.png", zoom=0.75)  action [Play("sound", button_click), SetVariable("cur_notebook_screen", "title"), Hide("Notebook")]
            tooltip "Закрыть дневник"

        
        if cur_notebook_screen == "title":
            use Title_notebook 
        elif cur_notebook_screen == "persons":
            use Persons_notebook   
        elif cur_notebook_screen == "clues":
            use Clues_notebook
        elif cur_notebook_screen == "team":
            use Team_notebook

style tx_button:
    color "#131212"
    hover_color "#13275e"
    # bold True

screen Title_notebook():
    # Left Page
    frame:
        xpos 184
        ypos 75
        xsize 395
        ysize 675
        background "gui/chaptersScreen/transparent.png"
        # background "#FFF"

        text "Записи дела":
            color "#000000"
            bold True
            xalign 0.5

        vbox:
            ypos 50
            spacing 20
            textbutton _("Досье"):
                action [Play("sound", notebook_click), SetVariable("cur_notebook_screen", "persons")]
            textbutton _("Улики"):
                action [Play("sound", notebook_click), SetVariable("cur_notebook_screen", "clues")]
            textbutton _("Напарники"):
                action [Play("sound", notebook_click), SetVariable("cur_notebook_screen", "team")]

screen Persons_notebook():

    # 2 персонажа слева, 3 справа
    default unlocked_persons = [p for p in persons.values() if not p.get("locked", True)]
    default left_persons_count = 2
    default right_persons_count = 3
    default max_persons_per_page = left_persons_count + right_persons_count
    default total_persons = len(unlocked_persons)
    default max_pages = max(0, (total_persons - 1) // max_persons_per_page)
    $ max_left_box_height = 650
    $ max_right_box_height = 600

    $ min_spacing = 5
    $ max_spacing = 100

    $ current_height = min(renpy.get_physical_size()[1], max_left_box_height)
    $ dynamic_spacing = min_spacing + (max_spacing - min_spacing) * (current_height / max_left_box_height)
    $ dynamic_spacing_right = min_spacing + (max_spacing - min_spacing) * (current_height / max_right_box_height)


    frame:
        xsize 1201
        ysize 977
        xalign 0.5
        yalign 0.55
        
        background "images/notebook/notebook_bg.png"

        button:
            xpos 990
            ypos 30
            xsize 60
            ysize 200
            background Transform("images/notebook/closeNotebookBut.png", zoom=0.75)
            action [Play("sound", button_click), SetVariable("cur_notebook_screen", "title"), SetVariable("cur_page", 0), Hide("Notebook")]
            tooltip "Закрыть дневник"

        # ==== ЛЕВАЯ СТРАНИЦА ====
        frame:
            xpos 184
            ypos 75
            xsize 395
            # ysize 675
            ysize max_left_box_height
            background "gui/chaptersScreen/transparent.png"

            imagebutton:
                xpos -5
                ypos -10
                idle "images/notebook/home.png"
                action [Play("sound", notebook_click), SetVariable("cur_notebook_screen", "title"), SetVariable("cur_page", 0)]

            text "ДОСЬЕ":
                color "#000000"
                bold True
                xalign 0.5
                ypos 0

            vbox:
                ypos 90
                spacing 60

                $ start_index = cur_page * max_persons_per_page
                $ left_persons = unlocked_persons[start_index : start_index + left_persons_count]


                for i, person in enumerate(left_persons):
                    hbox:
                        spacing 20

                        # фото всегда слева
                        vbox:
                            spacing 5
                            xalign 0.5
                            yalign 0.0
                            frame:
                                xsize 155
                                ysize 191
                                background Frame("images/notebook/photo_frame.png", 10, 10)
                                add Transform(person["image_path"], xysize=(155,190), fit="fit", align=(0.5,0.5))
                                use from_icon(person.get("from", ""), size=42)
                            text person.get("name", ""):
                                xalign 0.5
                                color "#000000"
                                size 20
                                bold True

                        # текст всегда справа
                        text person["description"]:
                            color "#000000"
                            size 18
                            xmaximum 210

        # ==== ПРАВАЯ СТРАНИЦА ====
        frame:
            xpos 605
            ypos 25
            xsize 378
            # ysize 675
            ysize max_right_box_height
            background "gui/chaptersScreen/transparent.png"

            vbox:
                ypos 40
                spacing 15

                $ right_start = start_index + left_persons_count
                $ right_persons = unlocked_persons[right_start : right_start + right_persons_count]

                for i, person in enumerate(right_persons):
                    $ index = right_start + i + 1

                    hbox:
                        spacing 20
                        if index % 2 == 1:
                            vbox:
                                spacing 5
                                frame:
                                    xsize 155
                                    ysize 191
                                    background Frame("images/notebook/photo_frame.png", 10, 10)
                                    add Transform(person["image_path"], xysize=(155,190), fit="fit", align=(0.5,0.5))
                                    use from_icon(person.get("from", ""), size=42)
                                text person.get("name", ""):
                                    color "#000000"
                                    size 20
                                    bold True
                                    xalign 0.5
                            text person["description"]:
                                color "#000000"
                                size 18
                                xmaximum 210
                        else:
                            text person["description"]:
                                color "#000000"
                                size 18
                                xmaximum 210
                            vbox:
                                spacing 8
                                frame:
                                    xsize 155
                                    ysize 191
                                    background Frame("images/notebook/photo_frame.png", 10, 10)
                                    add Transform(person["image_path"], xysize=(155,190), fit="fit", align=(0.5,0.5))
                                    use from_icon(person.get("from", ""), size=42)
                                text person.get("name", ""):
                                    color "#000000"
                                    size 20
                                    bold True
                                    xalign 0.5

        # ==== КНОПКИ ПЕРЕЛИСТЫВАНИЯ ====
        if cur_page > 0:
            imagebutton:
                xalign 0.18
                yalign 0.81
                idle "images/notebook/arrow_left.png"
                action [Play("sound", notebook_click), SetVariable("cur_page", cur_page - 1), With(dissolve)]

        if cur_page < max_pages:
            imagebutton:
                xalign 0.82
                yalign 0.81
                idle "images/notebook/arrow_right.png"
                action [Play("sound", notebook_click), SetVariable("cur_page", cur_page + 1), With(dissolve)]

screen Team_notebook():

    default main_chars = [c for c in main_characters.values()]
    $ total_chars = len(main_chars)
    $ left_count = 2
    $ right_count = 2
    $ max_per_page = left_count + right_count
    $ max_pages = max(0, (total_chars - 1) // max_per_page)

    frame:
        xsize 1201
        ysize 977
        xalign 0.5
        yalign 0.55
        background "images/notebook/notebook_bg.png"

        button:
            xpos 990
            ypos 30
            xsize 60
            ysize 200
            background Transform("images/notebook/closeNotebookBut.png", zoom=0.75)
            action [Play("sound", button_click), SetVariable("cur_notebook_screen", "title"), SetVariable("cur_page", 0), Hide("Notebook")]
            tooltip "Закрыть дневник"

        # ==== ЛЕВАЯ СТРАНИЦА ====
        frame:
            xpos 184
            ypos 75
            xsize 395
            ysize 650
            background "gui/chaptersScreen/transparent.png"

            imagebutton:
                xpos -5
                ypos -10
                idle "images/notebook/home.png"
                action [Play("sound", notebook_click), SetVariable("cur_notebook_screen", "title"), SetVariable("cur_page", 0)]

            text "НАПАРНИКИ":
                color "#000000"
                bold True
                xalign 0.5
                ypos 0

            vbox:
                ypos 90
                spacing 60

                $ start = cur_page * max_per_page
                $ left_side = main_chars[start : start + left_count]

                for person in left_side:
                    hbox:
                        spacing 20

                        vbox:
                            spacing 5
                            frame:
                                xsize 155
                                ysize 191
                                background Frame("images/notebook/photo_frame.png", 10, 10)
                                add Transform(person["image_path"], xysize=(155,190), fit="fit", align=(0.5,0.5))
                            text person["name"]:
                                xalign 0.5
                                color "#000000"
                                size 20
                                bold True

                        text person["description"]:
                            color "#000000"
                            size 18
                            xmaximum 210


        # ==== ПРАВАЯ СТРАНИЦА ====
        frame:
            xpos 605
            ypos 25
            xsize 378
            ysize 600
            background "gui/chaptersScreen/transparent.png"

            vbox:
                ypos 40
                spacing 30

                $ right_start = start + left_count
                $ right_side = main_chars[right_start : right_start + right_count]

                for i, person in enumerate(right_side):
                    $ index = i
                    hbox:
                        spacing 20
                        if index % 2 == 0:
                            vbox:
                                spacing 8
                                frame:
                                    xsize 155
                                    ysize 191
                                    background Frame("images/notebook/photo_frame.png", 10, 10)
                                    add Transform(person["image_path"], xysize=(155,190), fit="fit", align=(0.5,0.5))
                                text person["name"]:
                                    color "#000000"
                                    size 20
                                    bold True
                                    xalign 0.5
                            text person["description"]:
                                color "#000000"
                                size 18
                                xmaximum 210
                        else:
                            text person["description"]:
                                color "#000000"
                                size 18
                                xmaximum 210
                            vbox:
                                spacing 8
                                frame:
                                    xsize 155
                                    ysize 191
                                    background Frame("images/notebook/photo_frame.png", 10, 10)
                                    add Transform(person["image_path"], xysize=(155,190), fit="fit", align=(0.5,0.5))
                                text person["name"]:
                                    color "#000000"
                                    size 20
                                    bold True
                                    xalign 0.5


        # ==== ПЕРЕЛИСТЫВАНИЕ ====
        if cur_page > 0:
            imagebutton:
                xalign 0.18
                yalign 0.81
                idle "images/notebook/arrow_left.png"
                action [Play("sound", notebook_click), SetVariable("cur_page", cur_page - 1), With(dissolve)]

        if cur_page < max_pages:
            imagebutton:
                xalign 0.82
                yalign 0.81
                idle "images/notebook/arrow_right.png"
                action [Play("sound", notebook_click), SetVariable("cur_page", cur_page + 1), With(dissolve)]



screen Clues_notebook():
    # default unlocked_clues = [c for c in clues.values() if not c.get("locked", True)]
    # default unlocked_clues = [c for c in clues.values()]
    # default unlocked_clues = [c for c in unlocked_clues.values() if not c.get("locked", True)]
    default clues_count_per_page = 3
    default total_clues = len(unlocked_clues)
    # default max_pages = max(0, (total_clues - 1) // max_persons_per_page)
    default max_pages = max(0, (total_clues - 1) // clues_count_per_page)
    $ max_left_box_height = 650
    $ max_right_box_height = 675

    $ min_spacing = 5
    $ max_spacing = 40

    $ current_height = min(renpy.get_physical_size()[1], max_left_box_height)
    $ dynamic_spacing = min_spacing + (max_spacing - min_spacing) * (current_height / max_left_box_height)
    $ dynamic_spacing_right = min_spacing + (max_spacing - min_spacing) * (current_height / max_right_box_height)

    # Left Page
    frame:
        xpos 184
        ypos 75
        xsize 395
        ysize 675
        background "gui/chaptersScreen/transparent.png"
        # background "#FFF"

        imagebutton:
            xpos -5
            ypos -10
            idle "images/notebook/home.png"
            action [Play("sound", notebook_click), SetVariable("cur_notebook_screen", "title"), SetVariable("cur_page", 0)]
        
        text "Улики":
            color "#000000"
            bold True
            xalign 0.5

        vbox:
            ypos 50
            spacing 15
            $ start_index = cur_page * clues_count_per_page
            $ clues_dict_per_page = unlocked_clues[start_index:start_index + clues_count_per_page]
            
            for clue in clues_dict_per_page:
                vbox:
                    spacing 10
                    text clue["name"]:
                        color "#000000"
                        size 20 #28
                        bold True
                    text clue["description"]:
                        color "#000000"
                        size 22
                        xmaximum 410
                    if clue != clues_dict_per_page[-1]:
                        image "images/notebook/clue_line.png":
                            xsize 390
                    

    # Right Page
    frame:
        xpos 620
        ypos 25
        xsize 395
        # ysize 675
        ysize max_right_box_height
        background "gui/chaptersScreen/transparent.png"

        vbox:
            ypos 40
            spacing dynamic_spacing_right

            $ start_index = cur_page * clues_count_per_page
            $ clues_dict_per_page = unlocked_clues[start_index:start_index + clues_count_per_page]

            for i, clue in enumerate(clues_dict_per_page):
                $ index = i + 1

                vbox:
                    spacing 20
                    if index % 2 == 1:
                        frame:
                            xsize 150
                            ysize 192
                            background Frame("images/notebook/photo_frame.png", 10, 10)
                            add Transform(clue["image_path"], xysize=(140,192), fit="contain", align=(0.5,0.5))
                            button:
                                xfill True
                                yfill True
                                background None
                                hover_background None
                                # hovered [Play("sound", button_menu_hovered)]
                                action[Play("sound", button_click), Show("clue_large", image_path=clue["image_path"]), With(dissolve)]
                    else:
                        frame:
                            xpos 1.0
                            xsize 150
                            ysize 192
                            background Frame("images/notebook/photo_frame.png", 10, 10)
                            add Transform(clue["image_path"], xysize=(140,200), fit="contain", align=(0.5,0.5))
                            button:
                                xfill True
                                yfill True
                                background None
                                hover_background None
                                # hovered [Play("sound", button_menu_hovered)]
                                action[Play("sound", button_click), Show("clue_large", image_path=clue["image_path"]), With(dissolve)]
                            
    if cur_page > 0:
        imagebutton:
            xalign 0.18
            yalign 0.81
            idle "images/notebook/arrow_left.png"
            action [Play("sound", notebook_click), SetVariable("cur_page", cur_page-1)]
       
    if cur_page < max_pages:
        imagebutton:
            xalign 0.82
            yalign 0.81
            idle "images/notebook/arrow_right.png"
            action [Play("sound", notebook_click), SetVariable("cur_page", cur_page+1)]

    # use notebook_icon

##
screen clue_large(image_path):
    modal True
    zorder 101
    add Solid("#00000080")

    frame:
        xalign 0.5
        yalign 0.5
        background Frame("images/notebook/photo_frame.png", 10, 10)

        fixed:
            fit_first True
            add image_path:
                xsize int(config.screen_width * 0.6)
                ysize int(config.screen_height * 0.6)
                fit "contain"

            imagebutton:
                    ypos 5
                    xalign 0.98
                    idle "gui/overlay/close_idle.png"
                    hover "gui/overlay/close_hover.png"
                    hovered [Play("sound", button_menu_hovered)]
                    action [Play("sound", button_click), Hide("clue_large"), With(dissolve)]

##Choice screen ################################################################
      
default selected_suspect = None
default hovered_suspect = None
default suspects_order = ["james", "kyle", "lewis"]
default show_window = False

default suspects_info = {
    "james" : {"ПОДОЗРЕВАЕМЫЙ":"Джеймс Майерс","Место проживания":"Армори-стрит, 19", "Краткое описание":"Встречался с жертвой три месяца, собирался сделать предложение, но после скандала в ресторане оставил ее одну. Последний, кто видел ее живой.", "Отношения с жертвой": "Сожитель жертвы.","Алиби":"Не подтверждено: после инцидента в ресторане ушел домой. "},
    "kyle" : {"ПОДОЗРЕВАЕМЫЙ":"Кайл Ричардс","Место проживания":"Марч-драйв, 77", "Краткое описание":"Были вместе четыре года. Расстались из-за уезда Кайла на чемпионат - попытался вернуть её, но она была уже с другим.", "Отношения с жертвой": "Бывший парень жертвы.","Алиби":"Не подтверждено: после инцидента в ресторане уехал на озеро Ист-Спринг"},
    "lewis" : {"ПОДОЗРЕВАЕМЫЙ":"Луис Веласкес","Место проживания":"Неизвестно", "Краткое описание":"Студент, подрабатывает мойкой посуды в ресторане на Блинк-Роуд. С детства имел много прозвищ из-за латинских корней, популярностью никогда не пользовался", "Отношения с жертвой": "Одногруппник жертвы","Алиби":"Неизвестно"}
}
default persistent.first_try = True
default persistent.characters = {
    "judy":False,
    "mr_lawrence": False,
    "mrs_lawrence":False,
    "dr_andrews":False,
    "mrs_velaskez":False,
    "lisa":False,
    "james":False,
    "kyle":False
}
init python:
    def togle_first_try(correct_suspect = False):
        if persistent.first_try and correct_suspect:
            unlock_achievement("case", "3.1", "Вы получили достижение!")
        persistent.first_try = False
        renpy.save_persistent()
    def character_interviewed(pers):
        persistent.characters[pers] = True
        for value in persistent.characters.values():
            if not value:
                return
        unlock_achievement("case", "3.3", "Вы получили достижение!")
        renpy.save_persistent()


    


transform darken:
    matrixcolor BrightnessMatrix(-0.95)

transform normal_color:
    matrixcolor BrightnessMatrix(0.0)

transform suspect_normal:
    zoom 1.0
    anchor (0.0, 0.0)

transform suspect_zoomed:
    zoom 1.0
    anchor (0.0, 0.0)
    ease 0.25 zoom 1.1
    
transform move_left:
    zoom 1.0
    linear 0.5 xalign 0.2 
    linear 0.3 zoom 1.2

transform fade_in_transform:
    alpha 0.0
    linear 0.1 alpha 1.0

init python:
    def select_and_show_window(clicked):
        global suspects_order, selected_suspect, hovered_suspect, show_window
        if clicked not in suspects_order:
            return
        suspects_order.remove(clicked)
        suspects_order.insert(0, clicked)
        selected_suspect = clicked
        hovered_suspect = None
        show_window = True
        renpy.show_screen("SuspectWindow", suspect=clicked)

screen Choose_suspect():
    frame:
        xsize 1925
        ysize 1085
        xalign 0.5
        yalign 0.5

        if selected_suspect:
            background "images/locations/office_blur.png"
        else:
            background "images/locations/office_choice.png"

        fixed:
            xalign 0.5
            yalign 0.6
            $ positions = [0.0, 0.35, 0.7]

            for i, sus in enumerate(suspects_order):

                $ ypos_offset = 250
                $ sizes = {
                    "james": (582, 858),
                    "kyle": (591, 858),
                    "lewis": (548, 858)
                }
                $ size = sizes.get(sus, (582, 858))
                $ img_path = f"images/characters/chapter1/suspects/{sus}.png" if sus != "lewis" else "images/characters/chapter1/lewis.png"

                $ is_left = show_window and i == 0
                $ transform_to_use = suspect_zoomed if is_left else suspect_normal

                imagebutton:
                    xpos positions[i]
                    ypos ypos_offset
                    anchor (0.5, 0.0)

                    idle Transform(img_path, size=size)
                    at transform_to_use

                    if selected_suspect and selected_suspect != sus:
                        if hovered_suspect != sus:
                            at darken

                    hovered SetVariable("hovered_suspect", sus)
                    unhovered SetVariable("hovered_suspect", None)

                    action Function(select_and_show_window, sus)


screen SuspectWindow(suspect):
    modal True
    zorder 100

    frame:
        xalign 0.85 yalign 0.7
        xsize 1085 ysize 808
        background "images/suspect_window/sus_background.png"
        at fade_in_transform

        # Заголовок с именем подозреваемого
        hbox:
            xpos 140
            ypos 40
            spacing 30
            ysize 50

            
            text "ПОДОЗРЕВАЕМЫЙ:" :
                size 40
                color "#000000"
                bold True
                yalign 0.5
                
            text suspects_info.get(suspect, {}).get("ПОДОЗРЕВАЕМЫЙ", ""):
                size 48
                color "#000000"
                bold True
                yalign 0.5
                

        hbox:
            xpos 100
            ypos 130
            spacing 20
            xsize 850

            vbox:
                spacing 60
                yalign 0.0
                
                text "Место\nпроживания:" :
                    size 36
                    bold True
                    color "#000000"
                    xsize 220
                    text_align 0.0
                    yalign 0.0

                text "Краткое\nописание:" :
                    size 36
                    bold True
                    color "#000000"
                    xsize 220
                    text_align 0.0
                    yalign 0.0
                    
                text "Отношения с\nжертвой:" :
                    size 36
                    bold True
                    color "#000000"
                    xsize 220
                    text_align 0.0
                    yalign 0.0
                
                text "Алиби:" :
                    size 36
                    bold True
                    color "#000000"
                    xsize 220
                    text_align 0.0

            vbox:
                ypos 10
                spacing 1

                text suspects_info.get(suspect, {}).get("Место проживания", ""):
                    size 30
                    color "#000000"
                    xsize 650
                    text_align 0.0
                    ypos 0
                
                text suspects_info.get(suspect, {}).get("Краткое описание", ""):
                    size 30
                    color "#000000"
                    xsize 650
                    text_align 0.0
                    ypos 80
                    
                text suspects_info.get(suspect, {}).get("Отношения с жертвой", ""):
                    size 30
                    color "#000000"
                    xsize 650
                    text_align 0.0
                    ypos 135
                text suspects_info.get(suspect, {}).get("Алиби", ""):
                    size 30
                    color "#000000"
                    xsize 650
                    text_align 0.0
                    ypos 215
                    
        hbox:
            xalign 0.5 
            yalign 0.95
            spacing -100
            
            imagebutton:
                idle "images/suspect_window/cancel_button.png" 
                action [Hide("SuspectWindow"), SetVariable("show_window", False), Play("sound", button_click)]

                
            imagebutton:
                idle "images/suspect_window/blame_button.png"
                action [
                    Play("sound", button_click),
                    Show("AccuseConfirm", suspect=suspect),
                    # Return(suspect)
                ]
## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    on "show" action Play("sound", "sounds/dialogue_click.mp3")

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who:
                    id "who"
                    color "#D9D9D9"
                    yalign 0.5
                    xalign 0.5

        text what id "what":
            xsize 0.85
            xpos 150
            yalign 0.1
            size(40)
            color "#D9D9D9"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    # xpos 40
    ypos -86
    xsize 400
    ysize 54
    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    # padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice
screen choice_arrows(items):

    hbox:
        style "choice_arrows_hbox"
        yalign 0.9
        spacing gui.choice_spacing + 30
        for i in items:
            button:
                if i.kwargs.get("arrow_down", False):
                    style "menu_arrow_down_button"
                else:
                    style "menu_arrow_up_button"

                text i.caption:
                    style "menu_arrow_text"
                action i.action

            # textbutton i.caption action i.action

style choice_arrows_hbox:
    xalign 0.5
    yalign 0.95
    spacing gui.choice_spacing

style menu_arrow_down_button is button:
    background Frame("gui/button/choice_down_idle_background.png")
    hover_background Frame("gui/button/choice_down_hover_background.png")
    xsize 759
    ysize 85

style menu_arrow_up_button is button:
    background Frame("gui/button/choice_up_idle_background.png")
    hover_background Frame("gui/button/choice_up_hover_background.png")
    xsize 759
    ysize 85

style menu_arrow_text is text:
    properties gui.text_properties("choice_button")
    
screen choice(items):
    style_prefix "choice"

    if len(items) == 3:
        vbox:
            hbox:
                textbutton items[0].caption action items[0].action
                textbutton items[1].caption action items[1].action
            hbox:
                textbutton items[2].caption action items[2].action
        
    elif len(items) == 4:
        vbox:
            hbox:
                textbutton items[0].caption action items[0].action
                textbutton items[1].caption action items[1].action
            hbox:
                textbutton items[2].caption action items[2].action
                textbutton items[3].caption action items[3].action

    else: # 2 options (or more but 4 or more will get out of the screen)
        hbox:
            yalign 0.99
            ysize 300
            spacing gui.choice_spacing + 30
            for i in items:
                textbutton i.caption action i.action yalign 0.5

style choice_vbox:
    xalign 0.5
    yalign 0.95
    spacing 15

style choice_hbox:
    xalign 0.5
    yalign 0.95
    spacing gui.choice_spacing

# style choice_vbox is hbox
style choice_button is button
style choice_button_text is button_text


# style choice_button is default:
#     properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")

# style choice_long_button is choice_button:
#     background Frame("gui/button/long_choice.png")
#     hover_background Frame("gui/button/long_choice_hover.png")
style choice_button is button:
    background Frame("gui/button/choice_idle_background.png", 15, 15)
    hover_background Frame("gui/button/choice_hover_background.png", 15, 15)
    yminimum 85
    xsize 800
    xpadding 40



## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100
    use notebook_icon

    if quick_menu:

        hbox:
            style_prefix "quick_left"

            xpos 15
            yalign 0.006

            imagebutton:
                auto "gui/quickMenu/settings_%s.png" 
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), ShowMenu("preferences")]
        
        hbox:
            style_prefix "quick_right"
            spacing 7
            ypos 10
            xalign 0.995

            imagebutton:
                auto "gui/quickMenu/back_%s.png" 
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Rollback()]

            imagebutton:
                ypos -2
                selected_idle "gui/quickMenu/stop_hover.png"
                selected_hover "gui/quickMenu/stop_hover.png"
                auto "gui/quickMenu/stop_%s.png" 
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Preference("auto-forward", "toggle")]
            imagebutton:
                auto "gui/quickMenu/forward_%s.png" 
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), RollForward()]
            imagebutton:
                auto "gui/quickMenu/skip_%s.png" 
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Skip(fast=False, confirm=False)]


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.
screen StartButton(cur_saves):
    imagebutton:
        selected_idle "gui/menuButtons/start_game/selected.png"
        selected_hover "gui/menuButtons/start_game/selected.png"
        idle "gui/menuButtons/start_game/idle.png"
        hover "gui/menuButtons/start_game/hover.png"
        hovered [Play("sound", button_menu_hovered)]
        if cur_saves:
            action [Show("ContinueOrNewGame"), With(dissolve), Play("sound", button_menu_hovered)] # Play("sound", button_click)
        else:
            action [Start(), Play("sound", button_menu_hovered)]
        # action Start()
        
        # action Start()
    # vbox:
    #     spacing 0
    #     imagebutton idle "gui/MainMenu/button.png" action Start():
    #         at zoom
    #     textbutton _(text) action Start():
    #         # anchor(0.5, 0.5)
    #         pos(xpos, ypos)

screen ContinueStoryButton():
    imagebutton:
        auto "gui/menuButtons/continue_story/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [Continue(confirm=False), Play("sound", button_menu_hovered)]

screen NewGameButton():
    imagebutton:
        auto "gui/menuButtons/new_game/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [Start(), Play("sound", button_menu_hovered)]

screen ContinueGameButton():
    imagebutton:
        auto "gui/menuButtons/continue_game/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [Return(), Play("sound", button_menu_hovered)]

screen LoadButton():
    imagebutton:
        selected_idle "gui/menuButtons/load/selected.png"
        selected_hover "gui/menuButtons/load/selected.png"
        auto "gui/menuButtons/load/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [ShowMenu("load"), Play("sound", button_menu_hovered)]

screen SaveButton():
    imagebutton:
        selected_idle "gui/menuButtons/save/selected.png"
        selected_hover "gui/menuButtons/save/selected.png"
        auto "gui/menuButtons/save/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [ShowMenu("save"), Play("sound", button_menu_hovered)]

screen SettingsButton():
    imagebutton:
        selected_idle "gui/menuButtons/settings/selected.png"
        selected_hover "gui/menuButtons/settings/selected.png"
        auto "gui/menuButtons/settings/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [ShowMenu("preferences"), Play("sound", button_menu_hovered)]

screen ChaptersButton():
    imagebutton:
        selected_idle "gui/menuButtons/chapters/selected.png"
        selected_hover "gui/menuButtons/chapters/selected.png"
        auto "gui/menuButtons/chapters/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [ShowMenu("chapters"), Play("sound", button_menu_hovered)]

screen AchievementsButton():
    imagebutton:
        selected_idle "gui/menuButtons/achievements/selected.png"
        selected_hover "gui/menuButtons/achievements/selected.png"
        auto "gui/menuButtons/achievements/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [ShowMenu("achievements_types"), Play("sound", button_menu_hovered)]

screen MainMenuButton():
    imagebutton:
        auto "gui/menuButtons/quit/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [Show("ToMainScreenConfirm"), With(dissolve), Play("sound", button_menu_hovered)]
        # action MainMenu()

screen QuitButton():
    imagebutton:
        selected_idle "gui/menuButtons/quit/selected.png"
        selected_hover "gui/menuButtons/quit/selected.png"
        auto "gui/menuButtons/quit/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [Show("QuitConfirm"), With(dissolve), Play("sound", button_menu_hovered)]
        # action Quit(confirm=True)

screen ReturnButton():
    imagebutton:
        auto "gui/menuButtons/return/%s.png"
        hovered [Play("sound", button_menu_hovered)]
        action [Return(), Play("sound", button_menu_hovered)]


screen ContinueOrNewGame():    
    modal True

    frame:
        xsize 992
        ysize 315
        xalign 0.8
        yalign 0.5
        # # size(992, 315)
        # pos(0.45, 0.35)
        background "gui/overlay/confirm.png"

        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("ContinueOrNewGame"), With(dissolve)]
        
            text _("Хотите продолжить историю?"):
                color "#D9D9D9"
                size(45)
                xalign 0.5
        
        hbox:
            yalign 0.85
            xalign 0.5
            spacing 10
            
            use ContinueStoryButton
            use NewGameButton


screen QuitConfirm():
    modal True

    frame:
        xsize 992
        ysize 315
        xalign 0.8
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("QuitConfirm"), With(dissolve)]

            text _("Вы действительно хотите выйти?"):
                size(45)
                color "#D9D9D9"
                xalign 0.5

        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/quit_confirm_return/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("QuitConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/quit_confirm_quit/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action Quit()

screen StartChapterConfirm(chapter_label, cur_sel_chapter):
    # cur_sel_chapter variable needed for the chapter button to be selected
    modal True

    frame:
        xsize 992
        ysize 315
        xalign 0.8
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), SetVariable("cur_sel_chapter", ""), Hide("StartChapterConfirm"), With(dissolve)]

            text _("Хотите пройти заново данную главу?"):
                size(45)
                color "#D9D9D9"
                xalign 0.5
            
        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/quit_confirm_return/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), SetVariable("cur_sel_chapter", ""), Hide("StartChapterConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/replay_chapter/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), SetVariable("cur_sel_chapter", ""), Start(label=str(chapter_label))]

screen LoadSaveConfirm(slot, chapter, location, cur_sel_save, do_load):
    modal True

    frame:
        xsize 992
        ysize 315
        xalign 0.8
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), SetVariable("cur_sel_save", ""), Hide("LoadSaveConfirm"), With(dissolve)]

            if do_load:
                vbox:
                    ypos -15
                    xalign 0.5
                    spacing 5
                    text _("Хотите загрузить сохранение"):
                        color "#D9D9D9"
                        size(45)
                        xalign 0.5
                    text _(str(chapter) + " - " + str(location)):
                        color "#D9D9D9"
                        size(45)
                        xalign 0.5
            else:
                if FileLoadable(slot):
                    text _("Хотите перезаписать данное сохранение?"):
                        color "#D9D9D9"
                        size(45)
                        xalign 0.5
                else:
                    text _("Хотите сделать новое сохранение?"):
                        color "#D9D9D9"
                        size(45)
                        xalign 0.5
            
        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/quit_confirm_return/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), SetVariable("cur_sel_save", ""), Hide("LoadSaveConfirm"), With(dissolve)]

            if do_load:
                imagebutton:
                    auto "gui/menuButtons/load_confirm/%s.png"
                    hovered [Play("sound", button_menu_hovered)]
                    action [Play("sound", button_click), FileLoad(slot, confirm=False)]
            else:
                imagebutton:
                    auto "gui/menuButtons/save_confirm_save/%s.png"
                    hovered [Play("sound", button_menu_hovered)]
                    action [Play("sound", button_click), FileSave(slot, confirm=False), SetVariable("cur_sel_save", ""), Hide("LoadSaveConfirm"), With(dissolve)]

screen DeleteSaveConfirm(slot, cur_sel_save):
    # cur_sel_chapter variable needed for the chapter button to be selected
    modal True

    frame:
        xsize 992
        ysize 315
        xalign 0.8
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), SetVariable("cur_sel_save", ""), Hide("DeleteSaveConfirm"), With(dissolve)]

            text _("Хотите удалить данное сохранение?"):
                color "#D9D9D9"
                size(45)
                xalign 0.5
            
        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/quit_confirm_return/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("DeleteSaveConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/delete_save/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), FileDelete(slot, confirm=False), SetVariable("cur_sel_save", ""), Hide("DeleteSaveConfirm"), With(dissolve)]

screen ToMainScreenConfirm():
    modal True

    frame:
        xsize 992
        ysize 315
        xalign 0.8
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("ToMainScreenConfirm"), With(dissolve)]

            vbox:
                ypos -15
                xalign 0.5
                spacing 5

                text _("Хотите выйти в главное меню?"):
                    color "#D9D9D9"
                    size(45)
                    xalign 0.5
                text _("Весь несохраненный прогресс будет потерян."):
                    color "#D9D9D9"
                    size(45)
                    xalign 0.5
                
                null height 10

        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/quit_confirm_return/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("ToMainScreenConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/quit_confirm_quit/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), MainMenu(confirm=False, save=False)]

screen AccuseConfirm(suspect):
    modal True
    zorder 101
    add Solid("#00000080")
    
    frame:
        xsize 992
        ysize 330 # 315
        xalign 0.8
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        vbox:
            xsize 992
            spacing 30
            imagebutton:
                ypos 10
                xalign 0.95
                idle "gui/overlay/close_idle.png"
                hover "gui/overlay/close_hover.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("AccuseConfirm"), With(dissolve)]

            text _("Вы действительно хотите обвинить этого подозреваемого?"):
                size(45)
                color "#D9D9D9"
                xalign 0.5

        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/accuse_confirm_button/back/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("AccuseConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/accuse_confirm_button/accuse/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [
                    Hide("Choose_suspect"),
                    Hide("AccuseConfirm"),
                    Hide("SuspectWindow"),
                    Return(suspect) 
                ]

screen SuspectAccuseRetryConfirm():
    modal True
    zorder 101
    add Solid("#00000080")
    
    frame:
        xsize 992
        ysize 330 # 315
        xalign 0.5
        yalign 0.5
        background "gui/overlay/confirm.png"
        
        # vbox:
        #     xsize 992
        #     spacing 30
            # imagebutton:
            #     ypos 10
            #     xalign 0.95
            #     idle "gui/overlay/close_idle.png"
            #     hover "gui/overlay/close_hover.png"
            #     hovered [Play("sound", button_menu_hovered)]
            #     action [Play("sound", button_click), Hide("AccuseConfirm"), With(dissolve)]

        text _("Попробовать еще раз?"):
            size(45)
            color "#D9D9D9"
            xalign 0.5
            yalign 0.345

        hbox:
            yalign 0.85
            spacing 10
            xalign 0.5
            
            imagebutton:
                auto "gui/menuButtons/retry_confirm/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Play("sound", button_click), Hide("SuspectAccuseRetryConfirm"), With(dissolve), MainMenu(confirm=False, save=False)]

            imagebutton:
                auto "gui/menuButtons/accuse_confirm_button/accuse/%s.png"
                hovered [Play("sound", button_menu_hovered)]
                action [Hide("SuspectAccuseRetryConfirm"), Jump("choose_suspect")]

### Navigation screen used in game menus (main and in-game)
init:
    transform zoom:
        zoom 0.5

screen navigation_main_menu(cur_saves):

    vbox:
        style_prefix "game_title"
        spacing 15
        yalign 0.1
        # xanchor(0.5)
        xpos 80
        # xpos gui.navigation_xpos + 40
        image "gui/MainMenu/title_main.png"
        image "gui/MainMenu/subtitle_main.png":
            xpos 50
        # text _("Детектив")
        # vbox:
        #     ypos 20
        #     xpos 0.4
        #     anchor(0.5, 0.5)
        #     style_prefix "under_title"
        #     text _("Добро пожаловать")

    vbox:
        style_prefix "navigation"
        # xpos gui.navigation_xpos - 40
        xpos 90
        yalign 0.8
        spacing 25
        
        use StartButton(cur_saves)
        use LoadButton
        use ChaptersButton
        use AchievementsButton
        use SettingsButton
        
        # textbutton _("Load") action ShowMenu("load")
        # use ShowMenuButton("load", "Load")

        # textbutton _("Preferences") action ShowMenu("preferences")
        # use ShowMenuButton("preferences", "Settings", xpos = 125)

        # use ChaptersButton("Chapters")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        # textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            pass
            ## Help isn't necessary or relevant to mobile devices.
            # textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):
            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            use QuitButton
            # textbutton _("Quit") action Quit(confirm=not main_menu)
            # use QuitButton("Quit")
            

style under_title_text:
    italic(True)
    size(34)
    color("#FFFFFF")

style game_title_text:
    bold(True)
    size(48)
    color("#FFFFFF")

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


### Navigation in menus (not main)
#
# This is used in game menu, outside the main game, but not in the main menu
#
screen navigation_menu():
    vbox:
        style_prefix "navigation"

        spacing 30
        xpos 40
        yalign 0.5

        use LoadButton
        use ChaptersButton
        use AchievementsButton
        use SettingsButton

        use ReturnButton
        # xpos 30
        # yalign 0.5
        # # spacing gui.navigation_spacing
        # spacing 0
        
        # if not main_menu:
        #     use ShowMenuButton("save", "Save")
    
        # # textbutton _("Load") action ShowMenu("load")
        # use ShowMenuButton("load", "Load")

        # use ShowMenuButton("history", "History")
        # # textbutton _("History") action ShowMenu("history")

        # if not main_menu:
        #     use Button(MainMenu, "Main Menu")

        # # textbutton _("Save") action ShowMenu("save")
        # use ShowMenuButton("preferences", "Settings", xpos = 125)



## Navigation for menus other from main #########################
##
## ----- 
##

screen navigation_game():
    vbox:
        spacing 30
        xpos 40
        yalign 0.5

        use ContinueGameButton
        use SaveButton
        use LoadButton
        use ChaptersButton
        use AchievementsButton
        use SettingsButton
        use MainMenuButton
    # vbox:
    #     style_prefix "navigation"

    #     xpos 30
    #     yalign 0.5
    #     # spacing gui.navigation_spacing
    #     spacing 0
        
    #     if not main_menu:
    #         use ShowMenuButton("save", "Save")
    
    #     # textbutton _("Load") action ShowMenu("load")
    #     use ShowMenuButton("load", "Load")

    #     use ShowMenuButton("history", "History")
    #     # textbutton _("History") action ShowMenu("history")

    #     if not main_menu:
    #         use Button(MainMenu, "Main Menu")

    #     # textbutton _("Save") action ShowMenu("save")
    #     use ShowMenuButton("preferences", "Settings", xpos = 125)


### Start game screen ##############################################
transform fit_screen:
    fit "contain"
    align (0.5, 0.5)
screen press_to_start_game():
    zorder 100
    add "gui/MainMenu/background.png" at fit_screen

    use press_to_start_game_overlay

    use press_to_start_button

    image "gui/MainMenu/title_start.png":
        anchor(0.5, 0.5)
        pos(0.5, 0.2)

    image "gui/MainMenu/subtitle_start.png":
        anchor(0.5, 0.5)
        pos(0.5, 0.35)

    button:
        xysize(config.screen_width, config.screen_height)
        # action MainMenu(confirm=False, save=False)
        action [ Hide("press_to_start_game") ,ToggleScreen("main_menu"), With(Dissolve(0.5))]
        # action [Hide("press_to_start_game") ,Show("main_menu")]
        # action ShowMenu("main_menu")
        # action Show("main_menu", transition="dissolve")

screen press_to_start_button():

    imagebutton idle "gui/MainMenu/press_to_start_button.png" action NullAction():
        anchor(0.5, 0.5)
        pos(0.5, 0.85)

screen press_to_start_game_overlay():
    zorder 60
    add "gui/MainMenu/start_screen_overlay.png"

## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    # Count current savefiles
    $ cur_saves = 0
    for i in range(gui.file_slot_cols * gui.file_slot_rows):
        $ slot = i + 1
        if FileLoadable(slot):
                $ cur_saves += 1

    # add gui.main_menu_background
    add "gui/MainMenu/background.png" at fit_screen

    ## This empty frame darkens the main menu.
    frame:
        style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation_main_menu(cur_saves)

    # if gui.show_name:

    #     vbox:
    #         style "main_menu_vbox"

    #         # text "[config.name!t]":
    #         #     style "main_menu_title"

    #         # text "[config.version]":
    #         #     style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 662
    yfill True
    # color "#141414"
    background "gui/MainMenu/frame.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    if main_menu:
        use navigation_menu
    else:
        use navigation_game

    
    # textbutton _("Return"):
    #     style "return_button"

    #     action Return()
    # use ReturnButton("Return", xpos = 150, ypos = -50)

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/menu_background.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos 1002
    yalign 1.0
    yoffset -45

## Chapters Screen #############################################################
##
##
define chapters = [
    {
        "name" : "Глава 1",
        "description" : "На безмолвном берегу реки обнаружено тело молодой девушки. Новость потрясшая тихий городок.",
        "image_path" : "chapter_1.png",
        "jump_label" : "chapter_1"
    },
    {
        "name" : "Chapter 2",
        "description" : "Some Description",
        "image_path" : "chapter_2.png",
        "jump_label" : "chapter_2"
    },
    {
        "name" : "Chapter 3",
        "description" : "Some Description",
        "image_path" : "chapter_2.png",
        "jump_label" : "chapter_3"
    },
    {
        "name" : "Chapter 4",
        "description" : "Some Description",
        "image_path" : "chapter_2.png",
        "jump_label" : "chapter_4"
    },
]
define n_chapters = len(chapters)

# define chapters = ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4"]
# define chapters_description = ["Some description", "Some description", "Some description", "Description of chapter 4"]
# define chapters_image = ["chapter_1.png", "chapter_2.png", "chapter_2.png", "chapter_2.png"]
# define chapter_label = ["chapter_1", "chapter_2", "chapter_3", "chapter_4"]

default cur_sel_chapter = "asdasdas"

screen chapter(title, description, image_path, chapter_label, do_jump):

    frame:
        ypos 50
        xsize 475
        ysize 813
        background "gui/chaptersScreen/transparent.png"
        
        button:
            xsize 475
            ysize 813
            idle_background "gui/chaptersScreen/chapter_frame.png"
            hover_background "gui/chaptersScreen/chapter_frame_selected.png"
            hovered [Play("sound", button_menu_hovered)]
            if cur_sel_chapter == title:
                selected_background "gui/chaptersScreen/chapter_frame_selected.png"
            if do_jump: # Jump to chapter label if chapter is unlocked by the player, else do not add button
                action [Play("sound", button_click), SetVariable("cur_sel_chapter", title), Show("StartChapterConfirm", chapter_label=chapter_label, cur_sel_chapter=cur_sel_chapter), With(dissolve)]
                # action Confirm("Желаете повторить данную главу?", yes = Start(chapter_label))
                # action Start(chapter_label)
            else:
                hover_background "gui/chaptersScreen/chapter_frame.png"
                action NullAction()

        vbox:
            xsize 475
            image "images/chapters/" + image_path:
                pos(20, 20)
            text _(title):
                # pos(15, 20)
                ypos 20
                xalign 0.5
                # bold(True)
                color "#D9D9D9"
                size(60)
            text _(description):
                size(30)
                color "#D9D9D9"
                pos(19, 20)

screen chapters_holder():

    frame:
        background "gui/chaptersScreen/transparent.png"
        xalign 0.9
        yalign 0.5
        xsize 1346
        ysize 990
        has viewport id "MyScroller":
            draggable True
            scrollbars "horizontal"

        hbox:
            null width 0
            spacing 50
            # yalign 0.5
            # xalign 1.0
            $ j = 0
            for i, _ in enumerate(persistent.chapters):
                use chapter(chapters[i]["name"], chapters[i]["description"], chapters[i]["image_path"], chapters[i]["jump_label"], do_jump = True)
                # use chapter(chapters[i], chapters_description[i], chapters_image[i], chapter_label[i], do_jump = True)
                $ j += 1
            for i in range(j, n_chapters):
                use chapter("???", "Глава еще недоступна.", "locked.png", "", do_jump = False)
            null width 0

            # use chapter(chapters[0]["name"], chapters[0]["description"], chapters[0]["image_path"], chapters[0]["jump_label"], do_jump = True)
            # use chapter(chapters[1]["name"], chapters[1]["description"], chapters[1]["image_path"], chapters[1]["jump_label"], do_jump = True)


            #     for i in range(n_chapters):
            #         use chapter(chapters[i], chapters_description[i], chapters_image[i], chapter_label[i])
            #     null width 0
            # else:
            #     for i in range(n_chapters):
            #         use chapter("???", "You have not unlocked that chapter yet.", "None", "")
            #     null width 0
    # hbar value XScrollValue

screen chapters():
    tag menu

    add "gui/menu_background.png"
    # add "gui/overlay/game_menu.png"

    if main_menu:
        use navigation_menu
    else:
        use navigation_game

    use chapters_holder

## Achievements Screen #############################################################
##
##

screen notifyAchieve(message, title, currentImage):

    zorder 100
    style_prefix "notify"

    frame at notify_achieve_appear:
        background Frame("#756762")
        text "{size=+10}[title]{/size}\n[message!tq]\n{image=[currentImage]}"

    timer 3.25 action Hide('notifyAchieve')


transform notify_achieve_appear:
    on show:
        xalign 0.5
        yalign -0.5
        alpha 1
        linear .5 yalign 0
    on hide:
        linear .5 yalign -0.5

default achievements_category_to_rus = {
    "acquaintances" : "Знакомства",
    "objects" : "Предметы",
    "case" : "Дела",
    "locations" : "Места",
    "leadership" : "Лидерство"
}

default persistent.allAchivments = {
    "acquaintances": [
        {"id": "1.1","name": "Дела любовные", "image": "images/achievements/ach1.png", "type": "standard", "obtained": False, "description":"допросить свидетеля, состоявшего в отношениях с жертвой. "},
        {"id": "1.2","name": "Ты — убийца!", "image": "images/achievements/ach2.png", "type": "rare", "obtained": False, "description":"Обвинить настоящего преступника."},
        {"id": "1.3","name": "Фальстарт", "image": "images/achievements/ach3.png", "type": "rare", "obtained": False, "description":"Обвинить невиновного персонажа."},
    ],
    "objects": [
        {"id": "2.1","name": "Переодевание", "image": "images/achievements/ach2_1.png", "type": "standard", "obtained": False, "description":"осмотреть одежду жертвы."},
        {"id": "2.2","name": "Коллекция", "image": "images/achievements/ach2_2.png", "type": "standard", "obtained": False, "description":"собрать 5 улик за главу."},
        {"id": "2.3","name": "Дорогой дневник…", "image": "images/achievements/ach2_3.png", "type": "rare", "obtained": False, "description":"получить личный предмет жертвы."},
    ],
    "case": [
        {"id": "3.1","name": "Один шанс", "image": "images/achievements/ach3_1.png", "type": "legend", "obtained": False, "description":"сделать правильный вывод с первой попытки."},
        {"id": "3.2","name": "Вдоль и поперек", "image": "images/achievements/ach3_2.png", "type": "rare", "obtained": False, "description":"Обвинить невиновного персонажа."},
        {"id": "3.3","name": "Допрос", "image": "images/achievements/ach3_3.png", "type": "rare", "obtained": False, "description":" лично допросить всех персонажей главы. "},
    ],
    "locations": [
        {"id": "4.1","name": "Примерный семьянин", "image": "images/achievements/ach4_1.png", "type": "standard", "obtained": False, "description":"побывать в доме родственников жертвы."},
        {"id": "4.2","name": "Вечный студент", "image": "images/achievements/ach4_2.png", "type": "standard", "obtained": False, "description":" побывать в учебном заведении с допросом."},
        {"id": "4.3","name": "Праздник желудка", "image": "images/achievements/ach4_3.png", "type": "standard", "obtained": False, "description":" побывать в кафе или ресторане с допросом."},
        {"id": "4.4","name": "Внеплановое обследование", "image": "images/achievements/ach4_4.png", "type": "standard", "obtained": False, "description":" побывать в медицинском учреждении с допросом."}

    ],
    "leadership": [
        {"id": "5.1","name": "Давление с толком", "image": "images/achievements/ach5_1.png", "type": "rare", "obtained": False, "description":"выбрать вариант диалога с насмешкой"},
        {"id": "5.2","name": "Секретное оружие - сарказм", "image": "images/achievements/ach5_2.png", "type": "standard", "obtained": False, "description":"получить информацию, надавив на подозреваемого. "},
        {"id": "5.3","name": "Время - деньги", "image": "images/achievements/ach5_3.png", "type": "rare", "obtained": False, "description":"не упустить возможность опросить еще свидетелей. "},
        {"id": "5.4","name": "Вдох, выдох", "image": "images/achievements/ach5_4.png", "type": "standard", "obtained": False, "description":"получить информацию, надавив на подозреваемого. "},
        {"id": "5.5","name": "Психотерапия", "image": "images/achievements/ach5_5.png", "type": "legend", "obtained": False, "description":"разблокировать воспоминание.  "},
    ]
    # "Category 6": [
    # ],
    # "Category 7": [ 
    # ],
    # "Category 8": [
    # ],
    # "Category 9": [
    # ],
}

init python:
    import time

    def unlock_achievement(category, ach_id, message):
        for ach in persistent.allAchivments[category]:
            if ach["id"] == ach_id:
                if not ach["obtained"]:
                    ach["obtained"] = True
                    ach["obtained_time"] = time.time()
                    # renpy.show_screen("notifyAchieve", message, ach["name"], ach["image"])
                    renpy.show_screen("unlock_notification_achievement", message, ach["name"], ach["image"])
    
    def check_clues_count():
        collected = 0
        for clue in clues.values():
            if not clue["locked"]:
                collected += 1
        if collected >= 5:
            unlock_achievement("objects", "2.2", "Вы получили достижение!")
        for clue in clues.values():
            if clue["locked"]:
                return
        unlock_achievement("case", "3.2", "Вы получили достижение!")
    

    def get_achievements_by_category(category, filter_type=None, all=False):
        if category not in persistent.allAchivments:
            return []

        newachievements = persistent.allAchivments[category]

        if filter_type:
            newachievements = [ach for ach in newachievements if ach["type"] == filter_type]

        if all:
            return [ach for ach in newachievements]
        else:    
            return [ach for ach in newachievements if ach["obtained"]]


define ach_grid_cols = 3
define ach_grid_rows = 3

screen folders_grid():
    vbox:
        xsize 1346
        spacing 90
        # ysize 990

        text "Всего Достижений " + str(sum(1 for category in persistent.allAchivments.values() for ach in category if ach["obtained"])) + "/" + str(sum(len(category) for category in persistent.allAchivments.values())):
            size(48)
            xalign 0.5
            ypos 25
    
        grid ach_grid_cols ach_grid_rows:
            xalign 0.5
            # yalign 0.5
            spacing 30
            for i, category in enumerate(list(persistent.allAchivments.keys())[:5]):
                frame:
                    style "folder_style"
                    
                    imagebutton:
                        idle "gui/achievementsScreen/ach_folders/folder_" + str(i+1) + ".png"
                        action [Play("sound", button_click), ShowMenu("achievements", category=category)]

                    text str(sum(1 for ach in persistent.allAchivments[category] if ach["obtained"])) + "/" + str(len(persistent.allAchivments[category])):
                        size 24
                        color "#D9D9D9"
                        # outline (1, "#000000")
                        xpos 0.9
                        ypos 0.9

style folder_style:
    xsize 343
    ysize 191
    right_padding 22
    bottom_padding 10
    background None

screen achievements_types():
    tag menu

    add "gui/menu_background.png"

    if main_menu:
        use navigation_menu
    else:
        use navigation_game

    frame:
        xsize 1346
        ysize 990
        yalign 0.5
        xalign 0.9
        background None

        
        use folders_grid


### Screens for achievements

screen achievement(name, ach_image_path, ach_type, desc):
    frame:
        xsize 1171
        ysize 309
        xpos 80
        if ach_type == "standard":
            background "gui/achievementsScreen/ach_rarity_frame/ach_standard.png"
        elif ach_type == "rare":
            background "gui/achievementsScreen/ach_rarity_frame/ach_rare.png"
        else:
            background "gui/achievementsScreen/ach_rarity_frame/ach_legend.png"

        hbox:
            image str(ach_image_path):
                pos(25, 25)
            vbox:
                pos(50, 50)
                xmaximum 750

                text _(name):
                    size 48
                    xmaximum 750
                    # layout "subtitle"

                text _(desc):
                    ypos 20
                    xmaximum 750
                    # layout "subtitle"

default cur_sel_ach_type = "all"

screen filter_frame(category):
    frame:
        xsize 1171
        ysize 67
        xpos 80
        background "gui/achievementsScreen/filter_frame.png"

        hbox:
            xpos 20
            spacing 10
            yalign 0.5

            imagebutton:
                # selected If(category == "standard")
                idle "gui/achievementsScreen/standard.png"
                hover "gui/achievementsScreen/standard_selected.png"
                hovered [Play("sound", button_menu_hovered)] 
                if cur_sel_ach_type == "standard":
                    selected_idle "gui/achievementsScreen/standard_selected.png"
                    # selected_hover "gui/achievementsScreen/standard.png"              
                    action [Play("sound", button_click), SetVariable("cur_sel_ach_type", "all"), ShowMenu("achievements", category=category)]
                else:              
                    action [Play("sound", button_click), SetVariable("cur_sel_ach_type", "standard"), ShowMenu("achievements", category=category, filter_type="standard")]
                    
                       
            imagebutton:
                # selected If(category == "rare")
                idle "gui/achievementsScreen/rare.png"
                hover "gui/achievementsScreen/rare_selected.png"
                hovered [Play("sound", button_menu_hovered)]  
                if cur_sel_ach_type == "rare":
                    selected_idle "gui/achievementsScreen/rare_selected.png"
                    # selected_hover "gui/achievementsScreen/rare.png"
                    action [Play("sound", button_click), SetVariable("cur_sel_ach_type", "all"), ShowMenu("achievements", category=category)]
                else:
                    action [Play("sound", button_click), SetVariable("cur_sel_ach_type", "rare"), ShowMenu("achievements", category=category, filter_type="rare")]
                
            imagebutton:
                # selected If(category == "legend")
                idle "gui/achievementsScreen/legend.png"
                hover "gui/achievementsScreen/legend_selected.png"
                hovered [Play("sound", button_menu_hovered)] 
                if cur_sel_ach_type == "legend":
                    selected_idle "gui/achievementsScreen/legend_selected.png"
                    # selected_hover "gui/achievementsScreen/legend.png"
                    action [Play("sound", button_click), SetVariable("cur_sel_ach_type", "all"), ShowMenu("achievements", category=category)]
                else:
                    action [Play("sound", button_click), SetVariable("cur_sel_ach_type", "legend"), ShowMenu("achievements", category=category, filter_type="legend")]


screen achievements(category, filter_type = None):
    tag menu

    add "gui/menu_background.png"

    if main_menu:
        use navigation_menu
    else:
        use navigation_game

    frame:
        xsize 1346
        ysize 990
        yalign 0.5
        xalign 0.9
        background None

        has viewport:
            draggable True
            scrollbars "vertical"
            
            
        vbox:
            xsize 1300
            spacing 20

            text achievements_category_to_rus[str(category)]:
                size(48)
                xalign 0.5

            use filter_frame(category)

            $ achievements_obtained = get_achievements_by_category(category, filter_type=filter_type, all=False)
            $ achievements_all = get_achievements_by_category(category, filter_type=filter_type, all=True)

            $ achievements_all = sorted(
                achievements_all,
                key=lambda ach: (
                    not ach["obtained"],
                    -(ach.get("obtained_time", 0))
                )
            )
            $ n_achievements = len(achievements_all)

            $ n_ach_obtained = len(achievements_obtained)

            for ach in achievements_all:
                if ach["obtained"]:
                    use achievement(ach["name"], ach["image"], ach["type"], ach["description"])
                else:
                    if ach["type"] == "rare":
                        use achievement(ach["name"], "gui/achievementsScreen/locked_rare.png", ach["type"], "Вы еще не октрыли данное достижение")
                    elif ach["type"] == "legend":
                        use achievement(ach["name"], "gui/achievementsScreen/locked_legend.png", ach["type"], "Вы еще не октрыли данное достижение")
                    else: # standard
                        use achievement(ach["name"], "gui/achievementsScreen/locked_standard.png", ach["type"], "Вы еще не октрыли данное достижение")



## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():
    tag menu
    add "gui/menu_background.png"

    use file_slots(_("Save"), do_load=False)


screen load():
    tag menu
    add "gui/menu_background.png"

    use file_slots(_("Load"), do_load=True)

screen file_slot(slot, do_load):
    button:
        style "slot_capsule_button"
        idle_background "gui/saveLoadMenu/capsule_frame.png"
        hover_background "gui/saveLoadMenu/capsule_frame_selected.png"
        if cur_sel_save == slot:
            selected_background "gui/saveLoadMenu/capsule_frame_selected.png"
        
        if do_load:
            if FileLoadable(slot):
                hovered [Play("sound", button_menu_hovered)]
                action [
                    Play("sound", button_click),
                    SetVariable("cur_sel_save", slot), 
                    Show("LoadSaveConfirm", slot=slot, chapter=FileJson(slot, key="chapter", missing = "Unknown Chapter", empty=""), location=FileJson(slot, key="location", missing="Unknown Location", empty=""), cur_sel_save=cur_sel_save, do_load=do_load), 
                    With(dissolve)
                ]
            else:
                hover_background "gui/saveLoadMenu/capsule_frame.png"
                action NullAction()
        else:  
            hovered [Play("sound", button_menu_hovered)]
            action [
                Play("sound", button_click),
                SetVariable("cur_sel_save", slot),
                Show("LoadSaveConfirm", slot=slot, chapter=FileJson(slot, key="chapter", missing = "Unknown Chapter", empty=""), location=FileJson(slot, key="location", missing="Unknown Location", empty=""), cur_sel_save=cur_sel_save, do_load=do_load), 
                With(dissolve)
            ]

        has hbox

        # Скриншот сохранения
        add FileScreenshot(slot, empty="gui/saveLoadMenu/empty_save.png") xsize 326 ysize 195 xalign 0.0 # Empty.png !!!!

        # Информация о сохранении
        hbox:
            xsize 1171

            vbox:
                xpos 20
                spacing 5
                hbox:
                    text FileTime(slot, format=_("{#file_time}%d/%m/%Y    %H:%M:%S"), empty=_("Empty slot")):
                        style "slot_time_text"
                    text FileSaveName(slot):
                        style "slot_time_text"
                
                null height 20

                hbox:
                    text str(FileJson(slot, key="chapter", missing = "Unknown chapter", empty = "")):
                        style "slot_time_text"
                        size(48)
                hbox:
                    text str(FileJson(slot, key="location", missing = "Unkown location", empty = "")):
                        style "slot_time_text"
            
            # Delete save button
            if FileLoadable(slot):
                imagebutton:
                    # ypos 10
                    xpos 10
                    # xalign 0.95
                    idle "gui/overlay/close_idle.png"
                    hover "gui/overlay/close_hover.png"
                    hovered [Play("sound", button_menu_hovered), SetVariable("cur_sel_save", slot)]
                    unhovered SetVariable("cur_sel_save", "")
                    action [Play("sound", button_click), SetVariable("cur_sel_save", slot), Show("DeleteSaveConfirm", slot=slot, cur_sel_save=cur_sel_save), With(dissolve)]
                    # action NullAction()

        if FileLoadable(slot):
            key "save_delete" action [SetVariable("cur_sel_save", slot), Show("DeleteSaveConfirm", slot=slot, cur_sel_save=cur_sel_save), With(dissolve)]


default cur_sel_save = "asasd;adm"

screen file_slots(title, do_load):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    if main_menu:
        use navigation_menu
    else:
        use navigation_game

    frame:
        style "window_background"

        hbox:
            spacing 0

            frame:
                style "slot_frame"
                yfill True
                has viewport:
                    draggable True
                    mousewheel True
                    scrollbars "vertical"

                vbox:
                    xsize 1300
                    spacing 56

                    # Count current savefiles
                    $ cur_saves = 0
                    for i in range(gui.file_slot_cols * gui.file_slot_rows):
                        $ slot = i + 1
                        if FileLoadable(slot):
                                $ cur_saves += 1

                    text "ВСЕГО СОХРАНЕНИЙ {}/{}".format(cur_saves, gui.file_slot_cols * gui.file_slot_rows):
                            style "page_name_text"
                    
                    for i in range(gui.file_slot_cols * gui.file_slot_rows):
                        $ slot = i + 1

                        if do_load:
                            use file_slot(slot, do_load)
                        else:
                            use file_slot(slot, do_load=False)
                    
                    null height 10
                        

# Стили
style window_background:
    xalign 0.9
    yalign 0.5
    top_padding 21
    bottom_padding 26
    xsize 1334
    ysize 1000
    background "gui/chaptersScreen/transparent.png"



style slot_capsule_button:
    xsize 1171
    ysize 237
    top_padding 21  
    bottom_padding 21
    left_padding 18
    left_margin 63
    right_margin 57



style slot_capsule_button_text:
    textalign 0.5

style slot_time_text:

    size 40
    color "#D9D9D9"

style page_name_text:

    size 60
    color "#D9D9D9"
    xalign 0.5


style page_name_frame:
    left_margin 100
    xsize 897
    ysize 71
    xalign 0.5


style slot_chapter_text:
    font gui.text_font
    size 40
    color "#D9D9D9"

style slot_frame:
    background None

style vscrollbar:
    xsize 13


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

default persistent.bright_value = 0.0

init:
    transform bright:
        pass
        # matrixcolor BrightnessMatrix(persistent.bright_value)

screen bar(pref_value):

    bar value pref_value:
        # ysize 13
        # thumb_offset 36
        # left_bar Frame("gui/slider/left_bar.png", 100, 10)
        # right_bar Frame("gui/slider/right_bar.png", bottom=100)
        left_bar Frame("gui/slider/left_bar.png")
        right_bar Frame("gui/slider/right_bar.png")
        thumb "gui/slider/thumb.png"
        yalign 0.5

screen sound_bars():
    vbox:
        # xsize 1346
        xalign 0.5
        spacing 20

        # label _("Music Volume")

        hbox:
            xsize 1043
            spacing 10
            
            image "gui/preferencesMenu/music.png"
            use bar(Preference("music volume"))
            # bar value Preference("music volume"):
            #     yalign 0.5

        # label _("Sound Volume")

        hbox:
            xsize 1043
            spacing 10

            image "gui/preferencesMenu/sound.png"
            use bar(Preference("sound volume"))
            # bar value Preference("sound volume"):
            #     yalign 0.5

        # hbox:
        #     xsize 1043
        #     spacing 10

        #     image "gui/preferencesMenu/brightness.png"
        #     use bar(FieldValue(persistent, "bright_value", range=0.8, offset=-0.5, style="slider"))
            # bar value FieldValue(persistent, "bright_value", range=0.8, offset=-0.5, style="slider")

        # if config.has_music or config.has_sound or config.has_voice:
        #     null height gui.pref_spacing

            # textbutton _("Mute All"):
            #     action Preference("all mute", "toggle")

screen auto_text():
    frame:
        xsize 1205
        ysize 88
        xpos 30
        
        background "gui/preferencesMenu/auto_text_frame.png"

        hbox:
            spacing 20

            text _("Скорость проигрывания текста"):
                size(40)
                # bold(True)
                xpos 20
                ypos 13
        
            null width 20

        hbox:
            ypos 13
            spacing 20
            xalign 0.93

            imagebutton:
                idle "gui/preferencesMenu/auto_1x.png"
                hover "gui/preferencesMenu/auto_1x_selected.png"
                selected_idle "gui/preferencesMenu/auto_1x_selected.png"
                selected_hover "gui/preferencesMenu/auto_1x_selected.png" 
                hovered [Play("sound", button_menu_hovered)]                
                action [Play("sound", button_click), Preference("text speed", value=15)]
                # action NullAction()
            imagebutton:
                idle "gui/preferencesMenu/auto_1.5x.png"
                hover "gui/preferencesMenu/auto_1.5x_selected.png"
                selected_idle "gui/preferencesMenu/auto_1.5x_selected.png"
                selected_hover "gui/preferencesMenu/auto_1.5x_selected.png"
                hovered [Play("sound", button_menu_hovered)]                
                action [Play("sound", button_click), Preference("text speed", value=25)]
                # action NullAction()
            imagebutton:
                idle "gui/preferencesMenu/auto_2x.png"
                hover "gui/preferencesMenu/auto_2x_selected.png"
                selected_idle "gui/preferencesMenu/auto_2x_selected.png"
                selected_hover "gui/preferencesMenu/auto_2x_selected.png"
                hovered [Play("sound", button_menu_hovered)]                
                action [Play("sound", button_click), Preference("text speed", value=35)]
                # action NullAction()
            # text _("1X")
            # text _("1.5X")
            # text _("2X")

screen display_options():
    frame:
        xsize 1205
        ysize 88
        xpos 30

        background "gui/preferencesMenu/auto_text_frame.png"

        hbox:
            spacing 20

            text _("Отображение игры"):
                size(40)
                # bold(True)
                xpos 20
                ypos 13            

            null width 20

        hbox:
            ypos 5
            spacing 20
            xalign 0.95

            imagebutton:
                idle "gui/preferencesMenu/fullscreen.png"
                hover "gui/preferencesMenu/fullscreen_selected.png"
                selected_idle "gui/preferencesMenu/fullscreen_selected.png"
                selected_hover "gui/preferencesMenu/fullscreen_selected.png"
                hovered [Play("sound", button_menu_hovered)]                
                action [Play("sound", button_click), Preference("display", "fullscreen")]
                # action NullAction()
            imagebutton:
                idle "gui/preferencesMenu/windowed.png"
                hover "gui/preferencesMenu/windowed_selected.png"
                selected_idle "gui/preferencesMenu/windowed_selected.png"
                selected_hover "gui/preferencesMenu/windowed_selected.png"
                hovered [Play("sound", button_menu_hovered)]                
                action [Play("sound", button_click), Preference("display", "window")]
            # image "gui/preferencesMenu/display.png"

screen printer_toggle:
    frame:
        xsize 1205
        ysize 88
        xpos 30
        background "gui/preferencesMenu/auto_text_frame.png"

        hbox:
            spacing 20

            text _("Эффект печатной машинки"):
                xpos 20
                ypos 13
                size(40)
                # bold(True)

            null width 20
        
        hbox:
            ypos 13
            xalign 0.9

            imagebutton:
                # idle "gui/preferencesMenu/ToggleOn.png"
                # selected_idle "gui/preferencesMenu/ToggleOff.png"
                # selected_hover "gui/preferencesMenu/ToggleOff.png"
                idle "gui/preferencesMenu/ToggleOnBig.png"
                selected_idle "gui/preferencesMenu/ToggleOffBig.png"
                selected_hover "gui/preferencesMenu/ToggleOffBig.png"
                action [Play("sound", button_click), Preference("text speed", value=0)]

screen skip_options(skip_option):
    frame:
        xsize 1205
        ysize 88
        xpos 30
        background "gui/preferencesMenu/auto_text_frame.png"

        hbox:
            spacing 20
            
            if skip_option == "skip":
                $ txt = "Пропускать неувиденный текст"
            elif skip_option == "after choices":
                $ txt = "Пропускать после выбора"

            text _(txt):
                xpos 20
                ypos 13
                size(40)
                # bold(True)
            
            null width 20

        hbox:
            ypos 13
            xalign 0.9

            imagebutton:
                idle "gui/preferencesMenu/ToggleOffBig.png"
                selected_idle "gui/preferencesMenu/ToggleOnBig.png"
                selected_hover "gui/preferencesMenu/ToggleOnBig.png"
                action [Play("sound", button_click), Preference(skip_option, "toggle")]

define languages = ["Русский", "English"]
default curr_lang = 0

screen language_options():
    frame:
        xsize 1205
        ysize 88
        xpos 30

        background "gui/preferencesMenu/auto_text_frame.png"

        hbox:
            spacing 20

            text _("Язык"):
                size(40)
                # bold(True)
                xpos 20
                ypos 13
            
            null width 20

        hbox:
            ypos 10
            xalign 0.9
            spacing 20
            
            imagebutton:
                idle "gui/preferencesMenu/arrow_back.png"
                action Language(None)
            
            frame:
                ypos 5
                xsize 832
                ysize 45
                background "gui/preferencesMenu/language_name_holder.png"

                text _("Русский"):
                    color "#372620"
                    xalign 0.5
                    yalign 0.5
                    size(40)

            imagebutton:
                idle "gui/preferencesMenu/arrow_forward.png"
                action NullAction()
                # action Language("english")

# screen skip_options():
#     frame:
#         xsize 1205
#         ysize 88
#         xpos 30

#         background "gui/preferencesMenu/auto_text_frame.png"

#         hbox:
#             spacing 20

#             text _("Настройки пропуска"):
#                 size(40)
#                 bold(True)
#                 xpos 20
#                 ypos 13

#             null width 20

#             hbox:
#                 ypos 10
#                 spacing 20

#                 text _("Не увиденный текст")
#                 text _("После выбора")
#                 # text _("Переходы")



# screen skip_time_options():
#     frame:
#         xsize 1257
#         ysize 88
#         xpos 30
        
#         background "gui/preferencesMenu/auto_text_frame.png"

#         hbox:
#             spacing 20

#             text _("Скорость пропуска текста"):
#                 size(40)
#                 bold(True)
#                 xpos 20
#                 ypos 13
        
#             null width 20

#         hbox:
#             ypos 13
#             spacing 20
#             xalign 0.95

#             imagebutton:
#                 idle "gui/preferencesMenu/auto_1x.png"
#                 hover "gui/preferencesMenu/auto_1x_selected.png"
#                 selected_idle "gui/preferencesMenu/auto_1x_selected.png"
#                 selected_hover "gui/preferencesMenu/auto_1x_selected.png"
#                 action Preference("auto-forward time", value = 1)
#                 # action NullAction()
#             imagebutton:
#                 idle "gui/preferencesMenu/auto_1.5x.png"
#                 hover "gui/preferencesMenu/auto_1.5x_selected.png"
#                 selected_idle "gui/preferencesMenu/auto_1.5x_selected.png"
#                 selected_hover "gui/preferencesMenu/auto_1.5x_selected.png"
#                 action Preference("auto-forward time", value = 120)
#             imagebutton:
#                 idle "gui/preferencesMenu/auto_2x.png"
#                 hover "gui/preferencesMenu/auto_2x_selected.png"
#                 selected_idle "gui/preferencesMenu/auto_2x_selected.png"
#                 selected_hover "gui/preferencesMenu/auto_2x_selected.png"
#                 action Preference("auto-forward time", value = 800)
#             # text _("1X")

screen hotkey_button(text):
    button:
        frame:
            xsize 251
            ysize 67
            background "gui/preferencesMenu/hotkey_button.png"

            text _(text):
                color "#372620"
                size(30)
                bold(True)
                xalign 0.5
                yalign 0.5

        action NullAction()

screen hotkey_row(text, text_desc):
    hbox:
        spacing 20
        
        use hotkey_button(text)

        text _(text_desc):
            ypos 15


screen hotkeys():
    frame:
        xsize 1205
        ysize 772
        xpos 30

        background "gui/preferencesMenu/hotkeys_frame.png"

        text _("Горячие клавиши игрового процесса"):
            size(40)
            # bold(True)
            xalign 0.5
               
        vbox:
            yalign 0.5
            xpos 20
            spacing 10

            use hotkey_row("ESC", "Выход в меню")
            use hotkey_row("Пробел", "Продвижение по игре, не активирует выборы")
            use hotkey_row("CTRL", "Пропуск текста пока кнопка нажата")
            use hotkey_row("TAB", "Запустить/выключить пропуск текста")
            use hotkey_row("F", "Переключить полноэкранный режим")
            use hotkey_row("S", "Сделать скриншот")
            use hotkey_row("Delete", "Удалить выбранное сохранение")
            # use hotkey_row("PageUp", "Предыдущая фраза")
            # use hotkey_row("PageDown", "Следующая фраза")


screen preferences_holder():
    frame:
        xsize 1346
        ysize 990
        yalign 0.5
        xalign 0.9
        background "gui/chaptersScreen/transparent.png"
        # background "gui/preferencesMenu/preferences_holder.png"

        has viewport:
            draggable True
            scrollbars "vertical"

        vbox:
            spacing 15
            null height 10

            use sound_bars
            null height 20

            use auto_text
            null height 20

            use printer_toggle
            null height 20

            use skip_options("skip")
            null height 20

            use skip_options("after choices")
            null height 20

            use display_options
            null height 20

            use language_options
            null height 20

            use hotkeys
            null height 20

screen vanilla_preferences:
    use game_menu(_("Preferences"), scroll="viewport"):
        vbox:
            frame:
                style "preferences"
                
                vbox:
                    hbox:
                        box_wrap True

                        if renpy.variant("pc") or renpy.variant("web"):

                            vbox:
                                style_prefix "radio"
                                label _("Display")
                                textbutton _("Window") action Preference("display", "window")
                                textbutton _("Fullscreen") action Preference("display", "fullscreen")

                        vbox:
                            style_prefix "check"
                            label _("Skip")
                            textbutton _("Unseen Text") action Preference("skip", "toggle")
                            textbutton _("After Choices") action Preference("after choices", "toggle")
                            textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                        ## Additional vboxes of type "radio_pref" or "check_pref" can be
                        ## added here, to add additional creator-defined preferences.

                    null height (4 * gui.pref_spacing)

                    hbox:
                        style_prefix "slider"
                        # box_wrap True

                        vbox:

                            label _("Text Speed")
                            bar:
                                value Preference("text speed")
                                left_bar "gui/slider/left_bar.png"
                                right_bar "gui/slider/right_bar.png"
                                thumb "gui/slider/thumb.png"

                            label _("Auto-Forward Time")
                            bar value Preference("auto-forward time")

                            label _("Brightness")
                            bar value FieldValue(persistent, "bright_value", range=0.8, offset=-0.5, style="slider")
                            text _("Will apply after the scene will change..")

                        vbox:

                            if config.has_music:
                                label _("Music Volume")

                                hbox:
                                    bar value Preference("music volume")

                            if config.has_sound:

                                label _("Sound Volume")

                                hbox:
                                    bar value Preference("sound volume")

                                    if config.sample_sound:
                                        textbutton _("Test") action Play("sound", config.sample_sound)


                            if config.has_voice:
                                label _("Voice Volume")

                                hbox:
                                    bar value Preference("voice volume")

                                    if config.sample_voice:
                                        textbutton _("Test") action Play("voice", config.sample_voice)

                            if config.has_music or config.has_sound or config.has_voice:
                                null height gui.pref_spacing

                                textbutton _("Mute All"):
                                    action Preference("all mute", "toggle")
                                    style "mute_all_button"

screen preferences():
    tag menu
    
    add "gui/menu_background.png"

    if main_menu:
        use navigation_menu
    else:
        use navigation_game

    use preferences_holder

    # use vanilla_preferences

        


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style preferences:
    padding (20, 10)

    background "gui/overlay/settings.png"

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    # yalign 0.5
    # left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm_bg.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/overlay/confirm.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    color "#FFFFFF"
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    xpos gui.skip_xpos
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip(confirm=False) alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()
            


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
