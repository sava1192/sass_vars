import sublime, sublime_plugin, os, re

extensions = '.sass', '.scss'
re_var = re.compile(r'(\$[\w\-]+)\s*:\s*([^\n;]+)', re.IGNORECASE)
# re_val = re.compile()

class SassVarsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.edit = edit
    self.create_index()

  def create_index (self):
    max = -1
    file_name = self.view.file_name()
    for folder in self.view.window().folders():
      if file_name.find(folder) > max:
        current_folder = folder

    for root, dirs, files in os.walk(current_folder):
      # print(root, dirs, files)
      for file in files:
        if file.endswith(extensions):
          self.process_file(os.path.join(root, file))

  def process_file(self, file):
    print(re_var.findall(open(file).read()))



