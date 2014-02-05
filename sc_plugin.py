import sublime_plugin

ACTIVE = False
TEST_BUFFER = 'TestBuffer'
BACK_FILE = '.history' 

class CopyModifications(sublime_plugin.EventListener):
    def on_modified(self, view):
        if not ACTIVE:
            return
        if view.name() == TEST_BUFFER:
            return
        v2 = None
        w = view.window()
        for v in w.views():
            if v.name() == TEST_BUFFER:
                v2 = v
                break
        else:
            v2 = w.new_file()
            v2.set_name(TEST_BUFFER)
            w.focus_view(view)
        c = view.command_history(0, True)
        print c
        v2.run_command(c[0], c[1])

        # with open(BACK_FILE, 'w') as f:
        #     f.write(view.substr())
