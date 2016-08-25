import sublime, sublime_plugin

VIEW_TIMEOUT = 1000

class SortRecentFiles(sublime_plugin.EventListener):
    # def on_activated(self, view):
    #     def is_still_active():
    #         window = view.window()
    #         if window.active_view() == view:
    #             self.move_to_top(window, view)

    #     sublime.set_timeout(is_still_active, VIEW_TIMEOUT)

    def on_selection_modified_async(self, view):
        self.move_to_top(view.window(), view)

    def move_to_top(self, window, view):
        group, index = window.get_view_index(view)

        if index != 0:
            window.set_view_index(view, group, 0)

    def on_hover(view, point, hover_zone):
        print("hover")
