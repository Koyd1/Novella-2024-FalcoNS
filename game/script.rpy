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
#     python:
#         config.show = show

#     scene black 
#     $ renpy.pause(1, hard=True) 
    
#     show logo at transform_logo
#     $ renpy.pause(4, hard=True) 
    
#     hide logo 
#     $ renpy.pause(2, hard=True)
    
#     python:
#         config.show = ShowWithBrightness

#     return

label before_main_menu:

    call screen press_to_start_game with dissolve


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

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

    # This ends the game.

    "Test the brightness"
    scene bg room
    "Again test the brightness"
    show eileen happy:
        xalign 0.5
    scene bg room
    "Done"

    return

label chapter_1:
    "This is chapter 1"
    "Congrats."
    return 

label chapter_2:
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