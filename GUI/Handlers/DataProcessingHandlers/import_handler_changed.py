def import_handler_changed(import_widget):
    if import_widget.ds_combobox.currentIndex() >= 0:
        new_widget_class = import_widget.ds_combobox.currentData()
        index = import_widget.horizontalLayout.indexOf(import_widget.current_import_widget)
        new_widget = new_widget_class(import_widget.main_window)
        import_widget.current_import_widget.deleteLater()
        import_widget.groupBox.layout().insertWidget(index, new_widget)
        import_widget.current_import_widget = new_widget
