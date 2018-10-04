# ne-markingmenu

install to:
$HOUDINI_USER_PREF_DIR/python2.7libs/

directory should match this:

$HOUDINI_USER_PREF_DIR/

    python2.7libs/

        houdini_markingmenu/

            widgets/
                menuitembutton.py
                mousepath.py

            editor/

                widgets/
                    detailspane.y
                    editortaskbar.py
                    managecollectionstoolbar.py
                    modifiercomboboxes.py
                    referenceview.py

                    subwidgets/
                        labelcombobox.py
                        referencebuttons.py
            buttonfunctions.py
            markingmenu.py
            menueditor.py
            nodegraphactivewire.py
            reservefunctions.py
            utils.py

        nodegraphhooks.py


special care should be taken if you already have custom event handling in your own nodegraphhooks.py


