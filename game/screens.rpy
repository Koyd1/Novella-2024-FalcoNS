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
    xsize 324
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
            yalign 0.9
            spacing gui.choice_spacing + 30
            for i in items:
                textbutton i.caption action i.action

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


style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick_left"

            xpos 5
            yalign 0.006

            imagebutton:
                auto "gui/quickMenu/settings_%s.png" action ShowMenu("preferences")
        
        hbox:
            style_prefix "quick_right"
            spacing 7
            ypos 10
            xalign 0.995

            imagebutton:
                auto "gui/quickMenu/back_%s.png" action Rollback()
            imagebutton:
                ypos -2
                selected_idle "gui/quickMenu/stop_hover.png"
                selected_hover "gui/quickMenu/stop_hover.png"
                auto "gui/quickMenu/stop_%s.png" action Preference("auto-forward", "toggle")
            imagebutton:
                auto "gui/quickMenu/forward_%s.png" action RollForward()
            imagebutton:
                auto "gui/quickMenu/skip_%s.png" action Skip(fast=False, confirm=False)


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
        if cur_saves:
            action [Show("ContinueOrNewGame"), With(dissolve)]
        else:
            action Start()
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
        action Continue(confirm=False)

screen NewGameButton():
    imagebutton:
        auto "gui/menuButtons/new_game/%s.png"
        action Start()

screen ContinueGameButton():
    imagebutton:
        auto "gui/menuButtons/continue_game/%s.png"
        action Return()

screen LoadButton():
    imagebutton:
        selected_idle "gui/menuButtons/load/selected.png"
        selected_hover "gui/menuButtons/load/selected.png"
        auto "gui/menuButtons/load/%s.png"
        action ShowMenu("load")

screen SaveButton():
    imagebutton:
        selected_idle "gui/menuButtons/save/selected.png"
        selected_hover "gui/menuButtons/save/selected.png"
        auto "gui/menuButtons/save/%s.png"
        action ShowMenu("save")

screen SettingsButton():
    imagebutton:
        selected_idle "gui/menuButtons/settings/selected.png"
        selected_hover "gui/menuButtons/settings/selected.png"
        auto "gui/menuButtons/settings/%s.png"
        action ShowMenu("preferences")

screen ChaptersButton():
    imagebutton:
        selected_idle "gui/menuButtons/chapters/selected.png"
        selected_hover "gui/menuButtons/chapters/selected.png"
        auto "gui/menuButtons/chapters/%s.png"
        action ShowMenu("chapters")

screen AchievementsButton():
    imagebutton:
        selected_idle "gui/menuButtons/achievements/selected.png"
        selected_hover "gui/menuButtons/achievements/selected.png"
        auto "gui/menuButtons/achievements/%s.png"
        action ShowMenu("achievements_types")

screen MainMenuButton():
    imagebutton:
        auto "gui/menuButtons/quit/%s.png"
        action [Show("ToMainScreenConfirm"), With(dissolve)]
        # action MainMenu()

screen QuitButton():
    imagebutton:
        selected_idle "gui/menuButtons/quit/selected.png"
        selected_hover "gui/menuButtons/quit/selected.png"
        auto "gui/menuButtons/quit/%s.png"
        action [Show("QuitConfirm"), With(dissolve)]
        # action Quit(confirm=True)

screen ReturnButton():
    imagebutton:
        auto "gui/menuButtons/return/%s.png"
        action Return()


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
                action [Hide("ContinueOrNewGame"), With(dissolve)]
        
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
                action [Hide("QuitConfirm"), With(dissolve)]

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
                action [Hide("QuitConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/quit_confirm_quit/%s.png"
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
                action [SetVariable("cur_sel_chapter", ""), Hide("StartChapterConfirm"), With(dissolve)]

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
                action [SetVariable("cur_sel_chapter", ""), Hide("StartChapterConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/replay_chapter/%s.png"
                action [SetVariable("cur_sel_chapter", ""), Start(label=str(chapter_label))]

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
                action [SetVariable("cur_sel_save", ""), Hide("LoadSaveConfirm"), With(dissolve)]

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
                action [SetVariable("cur_sel_save", ""), Hide("LoadSaveConfirm"), With(dissolve)]

            if do_load:
                imagebutton:
                    auto "gui/menuButtons/load_confirm/%s.png"
                    action FileLoad(slot, confirm=False)
            else:
                imagebutton:
                    auto "gui/menuButtons/save_confirm_save/%s.png"
                    action [FileSave(slot, confirm=False), SetVariable("cur_sel_save", ""), Hide("LoadSaveConfirm"), With(dissolve)]

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
                action [SetVariable("cur_sel_save", ""), Hide("DeleteSaveConfirm"), With(dissolve)]

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
                action [SetVariable("cur_sel_save", ""), Hide("DeleteSaveConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/delete_save/%s.png"
                action [FileDelete(slot, confirm=False), SetVariable("cur_sel_save", ""), Hide("DeleteSaveConfirm"), With(dissolve)]

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
                action [Hide("ToMainScreenConfirm"), With(dissolve)]

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
                action [Hide("ToMainScreenConfirm"), With(dissolve)]

            imagebutton:
                auto "gui/menuButtons/quit_confirm_quit/%s.png"
                action MainMenu(confirm=False, save=False)

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
screen press_to_start_game():
    zorder 100
    add "gui/MainMenu/background.png"

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
    add "gui/MainMenu/background.png"

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
            if cur_sel_chapter == title:
                selected_background "gui/chaptersScreen/chapter_frame_selected.png"
            if do_jump: # Jump to chapter label if chapter is unlocked by the player, else do not add button
                action [SetVariable("cur_sel_chapter", title), Show("StartChapterConfirm", chapter_label=chapter_label, cur_sel_chapter=cur_sel_chapter), With(dissolve)]
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

default persistent.allAchivments = {
    "acquaintances": [
        {"id": "1.1","name": "Achievement 1.1", "image": "images/achievements/ach1.png", "type": "standard", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit.asdasdasdasdasdasd"},
        {"id": "1.2","name": "Achievement 1.2", "image": "images/achievements/ach1.png", "type": "rare", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
        {"id": "1.3","name": "Achievement 1.3", "image": "images/achievements/ach1.png", "type": "legend", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    ],
    "objects": [
        {"id": "2.1","name": "Achievement 2.1", "image": "images/achievements/ach2_1.png", "type": "standard", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
        {"id": "2.2","name": "Achievement 2.2", "image": "images/achievements/ach2_2.png", "type": "rare", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
        {"id": "2.3","name": "Achievement 2.3", "image": "images/achievements/ach2_3.png", "type": "standard", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    ],
    "locations": [
        {"id": "3.1","name": "Achievement 3.1", "image": "images/achievements/ach3_1.png", "type": "legend", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
        {"id": "3.2","name": "Achievement 3.2", "image": "images/achievements/ach3_2.png", "type": "rare", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
        {"id": "3.3","name": "Achievement 3.3", "image": "images/achievements/ach3_3.png", "type": "standard", "obtained": False, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. "},
    ],
    "Case": [
    ],
    "Category 5": [
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
    def unlock_achievement(category, ach_id, message):
        for ach in persistent.allAchivments[category]:
            if ach["id"] == ach_id:
                if ach["obtained"] == False:
                    ach["obtained"] = True
                    renpy.show_screen("notifyAchieve", message, ach["name"], ach["image"])
    
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
                        action ShowMenu("achievements", category=category)

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

        # text "Всего Достижений " + str(sum(1 for category in persistent.allAchivments.values() for ach in category if ach["obtained"])) + "/" + str(sum(len(category) for category in persistent.allAchivments.values())):
        #     size(48)
        #     xalign 0.5
        #     ypos 25
        
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
            # image "images/achievements/" + str(ach_image_path):
                pos(25, 25)
            vbox:
                pos(25, 25)
                text _(name):
                    xpos 30
                    size(48)
                text _(desc):
                    xpos 30
                    ypos 30

# screen achievement_filter()

# screen standard_button:
#     imagebutton:
#         idle "gui/achievementsScreen/standard.png"
#         action NullAction()

# screen rare_button:
#     imagebutton:
#         idle "gui/achievementsScreen/rare.png"
#         action NullAction()

# screen legend_button:
#     imagebutton:
#         idle "gui/achievementsScreen/legend.png"
#         action NullAction()

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
                if cur_sel_ach_type == "standard":
                    selected_idle "gui/achievementsScreen/standard_selected.png"
                    # selected_hover "gui/achievementsScreen/standard.png"
                    action [SetVariable("cur_sel_ach_type", "all"), ShowMenu("achievements", category=category)]
                else:
                    action [SetVariable("cur_sel_ach_type", "standard"), ShowMenu("achievements", category=category, filter_type="standard")]
                       
            imagebutton:
                # selected If(category == "rare")
                idle "gui/achievementsScreen/rare.png"
                hover "gui/achievementsScreen/rare_selected.png"
                if cur_sel_ach_type == "rare":
                    selected_idle "gui/achievementsScreen/rare_selected.png"
                    # selected_hover "gui/achievementsScreen/rare.png"
                    action [SetVariable("cur_sel_ach_type", "all"), ShowMenu("achievements", category=category)]
                else:
                    action [SetVariable("cur_sel_ach_type", "rare"), ShowMenu("achievements", category=category, filter_type="rare")]
                
            imagebutton:
                # selected If(category == "legend")
                idle "gui/achievementsScreen/legend.png"
                hover "gui/achievementsScreen/legend_selected.png"
                if cur_sel_ach_type == "legend":
                    selected_idle "gui/achievementsScreen/legend_selected.png"
                    # selected_hover "gui/achievementsScreen/legend.png"
                    action [SetVariable("cur_sel_ach_type", "all"), ShowMenu("achievements", category=category)]
                else:
                    action [SetVariable("cur_sel_ach_type", "legend"), ShowMenu("achievements", category=category, filter_type="legend")]


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

            text _(str(category)):
                size(48)
                xalign 0.5

            use filter_frame(category)

            $ achievements_obtained = get_achievements_by_category(category, filter_type=filter_type, all=False)
            $ achievements_all = get_achievements_by_category(category, filter_type=filter_type, all=True)
            $ n_achievements = len(achievements_all)

            $ n_ach_obtained = len(achievements_obtained)

            for i, ach in enumerate(achievements_all):
                if i < n_ach_obtained and achievements_obtained[i]["id"] == ach["id"]:
                    use achievement(ach["name"], ach["image"], ach["type"], ach["description"])
                else:
                    if ach["type"] == "rare":
                        use achievement(ach["name"], "gui/achievementsScreen/locked_rare.png", ach["type"], "Вы еще не октрыли данное достижение")
                    elif ach["type"] == "legend":
                        use achievement(ach["name"], "gui/achievementsScreen/locked_legend.png", ach["type"], "Вы еще не октрыли данное достижение")
                    else: # standard
                        use achievement(ach["name"], "gui/achievementsScreen/locked_standard.png", ach["type"], "Вы еще не октрыли данное достижение")

                    
# screen achievements_1():
#     tag menu

#     add "gui/menu_background.png"

#     if main_menu:
#         use navigation_menu
#     else:
#         use navigation_game

#     frame:
#         xsize 1346
#         ysize 990
#         yalign 0.5
#         xalign 0.9
#         background "gui/achievementsScreen/achievements_holder.png"

#         has viewport:
#             draggable True
#             scrollbars "vertical"

#         vbox:
#             spacing 20

#             use filter_frame

#             for i in range(achs_1_num):
#                 use achievement(achs_1_name[i], achs_1_desc[i], achs_1_image[i], achs_1_rarity[i])



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
                action [
                    SetVariable("cur_sel_save", slot), 
                    Show("LoadSaveConfirm", slot=slot, chapter=FileJson(slot, key="chapter", missing = "Unknown Chapter", empty=""), location=FileJson(slot, key="location", missing="Unknown Location", empty=""), cur_sel_save=cur_sel_save, do_load=do_load), 
                    With(dissolve)
                ]
            else:
                hover_background "gui/saveLoadMenu/capsule_frame.png"
                action NullAction()
        else:  
            action [
                SetVariable("cur_sel_save", slot),
                Show("LoadSaveConfirm", slot=slot, chapter=FileJson(slot, key="chapter", missing = "Unknown Chapter", empty=""), location=FileJson(slot, key="location", missing="Unknown Location", empty=""), cur_sel_save=cur_sel_save, do_load=do_load), 
                # Show("LoadSaveConfirm", slot=slot, time=FileTime(slot, format=_("{#file_time}%d/%m/%Y %H:%M:%S"), empty=_("Empty slot")), cur_sel_save=cur_sel_save, do_load=do_load), 
                With(dissolve)
            ]
        # action Confirm("Хотите загрузить данное сохранение?", yes = FileAction(slot))

        has hbox

        # Скриншот сохранения
        add FileScreenshot(slot, empty="gui/saveLoadMenu/empty_save.png") xsize 326 ysize 195 xalign 0.0 # Empty.png !!!!
        ## Here should be None.png

        # frame:
        #     background "gui/mask/mask_image.png"
        #     add FileScreenshot(slot) xsize 326 ysize 195

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
                    hovered SetVariable("cur_sel_save", slot)
                    unhovered SetVariable("cur_sel_save", "")
                    action [SetVariable("cur_sel_save", slot), Show("DeleteSaveConfirm", slot=slot, cur_sel_save=cur_sel_save), With(dissolve)]
                    # action NullAction()

        if FileLoadable(slot):
            key "save_delete" action [SetVariable("cur_sel_save", slot), Show("DeleteSaveConfirm", slot=slot, cur_sel_save=cur_sel_save), With(dissolve)]
        
        # key "save_delete" action FileDelete(slot)

default cur_sel_save = "asasd;adm"

screen file_slots(title, do_load):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    # use game_menu(title):

    #     fixed:
    #         order_reverse True
    #         button:
    #             style "page_label"

    #             key_events True
    #             xalign 0
    #             action page_name_value.Toggle()

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
    # background "gui/saveLoadMenu/save_holder.png"
    # background "gui/slot_capsule/window_background.png"
    # right_padding 30


style slot_capsule_button:
    xsize 1171
    ysize 237
    top_padding 21  
    bottom_padding 21
    left_padding 18
    left_margin 63
    right_margin 57
    # background "gui/slot_capsule/slot_capsule_background.png"


style slot_capsule_button_text:
    textalign 0.5

style slot_time_text:
    # font "gui/Philosopher-Regular.ttf"
    size 40
    color "#D9D9D9"

style page_name_text:
    # font "gui/Philosopher-Bold.ttf"
    size 60
    color "#D9D9D9"
    xalign 0.5


style page_name_frame:
    left_margin 100
    xsize 897
    ysize 71
    xalign 0.5
    # background "gui/saveLoadMenu/page_name_frame.png"
    # background "gui/slot_capsule/slot_page_name_back.png"

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
                action Preference("text speed", value=15)
                # action NullAction()
            imagebutton:
                idle "gui/preferencesMenu/auto_1.5x.png"
                hover "gui/preferencesMenu/auto_1.5x_selected.png"
                selected_idle "gui/preferencesMenu/auto_1.5x_selected.png"
                selected_hover "gui/preferencesMenu/auto_1.5x_selected.png"
                action Preference("text speed", value=25)
                # action NullAction()
            imagebutton:
                idle "gui/preferencesMenu/auto_2x.png"
                hover "gui/preferencesMenu/auto_2x_selected.png"
                selected_idle "gui/preferencesMenu/auto_2x_selected.png"
                selected_hover "gui/preferencesMenu/auto_2x_selected.png"
                action Preference("text speed", value=35)
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
                action Preference("display", "fullscreen")
                # action NullAction()
            imagebutton:
                idle "gui/preferencesMenu/windowed.png"
                hover "gui/preferencesMenu/windowed_selected.png"
                selected_idle "gui/preferencesMenu/windowed_selected.png"
                selected_hover "gui/preferencesMenu/windowed_selected.png"
                action Preference("display", "window")
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
                action Preference("text speed", value=0)

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
                action Preference(skip_option, "toggle")

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
