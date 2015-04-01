import sublime, sublime_plugin, os, re

extensions = '.scss', '.sass'
re_line = re.compile(r'(\$[\w\-]+)\s*:\s*([^\n;]+)', re.I)
re_var = re.compile(r'\$[\w\-]*')
variables = []
nice_path = True
#global dictionary for cross-file communication
goto = {}

class SassVarsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.clean().load_settings().build_index().show_panel()
    max

  def lala():
    return 'lala'

  def load_settings(self):
    # that should be rewritten, and added loading from settings
    # self.settings = {
    #   'show': {
    #     'value_only': False,
    #     'last_var': False,
    #     'all_vars': True
    #   }
    # }
    return self

  def clean(self):
    del variables[:]
    return self

  def build_index(self):
    self.process_folder(self.get_current_folder())
    self.process_variables()

    return self

  def show_panel(self):
    window = self.view.window()
    rezult = [[var.get('name'), var.get('value'), var.get('path')] for var in variables]
    print(rezult)
    window.show_quick_panel(rezult, self.show_var_declaration)

  def show_var_declaration(self, index):
    if index == -1:
      return

    var = variables[index]
    view = self.view.window().open_file(var.get('file'))
    goto['line'] = var.get('line')
    goto['file'] = var.get('file')

  def get_current_folder (self):
    cur_file = self.view.file_name()
    max = -1

    for folder in self.view.window().folders():
      if cur_file.find(folder) > max:
        cur_folder = folder
        max = len(folder)
    return cur_folder

  def process_folder (self, folder):
    for root, folders, files in os.walk(folder):
      for file in files:
        self.process_file(os.path.join(root, file))

  def process_file (self, file_name):
    if file_name.endswith(extensions):
      with open(file_name, 'r') as file:
        for i, line in enumerate(file.readlines()):
          var = re_line.findall(line)
          if len(var):
            variables.append({
              'name': var[0][0],
              'value': var[0][1],
              'file': file_name,
              'line': i + 1
            })

  def process_variables(self):
    for i, var in enumerate(variables):
      var['path']  = self.get_var_path(var)
      var['value'] = self.get_recursive_value(var, 100, i)

  def get_var_path(self, var):
    file = var.get('file')
    if nice_path:
      parent = os.path.join(os.path.dirname(file), os.pardir)
      return os.path.relpath(file, parent) + ' : ' + str(var.get('line'))
    else:
      return str(var.get('line')) + ' : ' + file

  def get_recursive_value (self, var, max, originalIndex):
    # if max:
    #   new_vars = re_var.findall(var.get('value'))
    #   paths = []
    #   if len(new_vars):
    #     for new_var in new_vars:

    #     return

    # max recursion depth, or var in variable not found
    # or whatever
    return var.get('value')


# def get_selected_variable(view):
#   sel = view.sel()[0]
#   line = view.line(sel.begin())
#   line_str = view.substr(line)
#   sel_pos = sel.begin() - line.begin()
#   matches = re_var.finditer(line_str)
#   for m in matches:
#     if m.start()-1 <= sel_pos and m.end() >= sel_pos:
#       return m.group()

class Events(sublime_plugin.EventListener):
  # def on_modified_async(self, view):
  #   var = get_selected_variable(view)
  #   print(var)
  #   if var:
  #     show_popup(var, view)

  def on_load(self, view):
    if view.file_name() == goto.get('file') and goto.get('line') > 1:
      point = view.text_point(goto.get('line') - 1, 0)
      view.sel().clear()
      view.sel().add(sublime.Region(point))
      view.show(point)
      #clean up
      goto['file'] = None
      goto['line'] = None
