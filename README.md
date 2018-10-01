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
        nodegraphhooks.py
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
                    
        
    scripts/
    
        python/
        
            nodegraphactivewire.py
special care should be taken if you already have custom event handling in your own nodegraphhooks.py


