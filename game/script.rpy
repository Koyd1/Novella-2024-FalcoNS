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


define persistent.chapters = []

### Splash screen and start screen
image black = "#000"
image white = "#ffffff"
image logo = "gui/MainMenu/splash.png"

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

    scene bg room


    show eileen happy

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    e "Я заметила, что Х ведет себя странно, он уже два дня не разговаривает со мной. Сегодня он оставил свой бумажник на столе, при том что обычно не забывает свои вещи... Может у него что-то случилось и он боится сказать?"

    "Andrew added this text for initial commit in his branch."

    menu:
        "You have a choice!"
        "Choice 1":
            "Text for choice 1"
        "Choice 2":
            "Text for choice 2"

    jump chapter_1

label chapter_1:
    $ chapter = "Chapter One"
    $ location = "2nd Location"
    if "Chapter 1" not in persistent.chapters:
        $ persistent.chapters.append("Chapter 1")
    "This is chapter 1"
    "Congrats."
    
    jump chapter_2

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