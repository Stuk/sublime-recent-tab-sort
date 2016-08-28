import sublime, sublime_plugin

IS_TRANSIENT = "sublime_recent_sort_is_transient"

class SortRecentFiles(sublime_plugin.EventListener):
    # AFAICT there's no way to find out if a certain view is transient (doesn't
    # appear as an open file/tab) through the Sublime API. Instead we keep track
    # of any modifications. This can result in some false positives.
    def on_modified_async(self, view):
        view.settings().set(IS_TRANSIENT, False)

    # There's also no way to know when a view gets permanently focused at the
    # end of Ctrl+Tab (instead of "activated" which happens for each press of
    # Ctrl+Tab). Instead we bring to top on any selectiong modification.
    #
    # If there are multiple views into the same file, this event gets called
    # with the view of the first one that was open, instead of the one where the
    # modification actually happened. So we find the active view and indexes
    # ourselves in `get_active_view_index`.
    def on_selection_modified_async(self, view):
        self.move_active_to_top()

    def move_active_to_top(self):
        window, group, index, view = self.get_active_view_index()

        # If there's no group, index, or the view is transient then don't try to
        # position it at the top
        if group == -1 or index == -1 or view.settings().get(IS_TRANSIENT, True):
            return

        if index != 0:
            window.set_view_index(view, group, 0)

    def get_active_view_index(self):
        window = sublime.active_window()
        group = window.active_group()
        view = window.active_view_in_group(group)

        # print(dir(view))

        # If get_view_index appears to have bugs then the following code might
        # be useful
        # index = -1
        # views = window.views_in_group(group)
        # for i, v in enumerate(views):
        #     if v.id() == view.id():
        #         index = i
        #         break

        _, index = window.get_view_index(view)

        return window, group, index, view
