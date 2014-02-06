import os
import sublime
import sublime_plugin

ACTIVE = False
TEST_BUFFER = 'TestBuffer'
HIST_FILE = '.hist'
HIST_MARK = r'#history\n'
MSG_MARK = r'#message\n'
USER_MARK = r'\s*#user\s*'
NEWLINE = '\n'

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


class ChatClient(sublime_plugin.TextCommand):
    def find_region(self, mark):
        regions = self.view.find_all(mark)
        if len(regions) == 2:
            return sublime.Region(regions[0].end(), regions[1].begin())
        else:
            return sublime.Region(0, 0)

    def load_hist(self, f, n=10):
        text = ''
        lines = []
        with open(f, 'r') as g:
            lines = [x.rstrip() for x in g.readlines()]
        if len(lines) > n:
            lines = lines[-n:]
        return NEWLINE.join(lines) + NEWLINE

    def update_hist(self, f, m, u):
        if m:
            with open(f, 'a') as g:
                g.write(u + ': ' + m + NEWLINE)

    def run(self, edit):
        message = ''
        m = self.find_region(MSG_MARK)
        h = self.find_region(HIST_MARK)
        u = self.find_region(USER_MARK)
        user = self.view.substr(u)
        print user
        if not m.empty():
            message = self.view.substr(m).rstrip()
            self.update_hist(HIST_FILE, message, user)
            self.view.replace(edit, m, NEWLINE)
            self.view.replace(edit, h, self.load_hist(HIST_FILE))
            print message

    def is_active(self):
        if os.path.splitext(self.view.file_name())[1].strip('.') in ['chat']:
            return True


class ChatPollUpdate(ChatClient):
    n = 0
    def callback(self):
        sublime.run_command('chat_poll_update', {})

    def run(self, edit):
        print self.n
        self.n += 1
        sublime.set_timeout(self.callback, 1)

    def is_active(self):
        return True
