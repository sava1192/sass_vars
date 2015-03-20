import sublime, sublime_plugin, os, re

extensions = '.scss', '.sass'
re_line = re.compile(r'(\$[\w\-]+)\s*:\s*([^\n;]+)', re.I)
re_var = re.compile(r'\$[\w\-]*')
variables = []
nice_path = True

class SassVarsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.clean().build_index().show_panel()

  def clean(self):
    del variables[:]
    return self

  def build_index(self):
    self.process_folder(self.get_current_folder())
    for var in variables:
      self.process_variable(var, 100)
    return self

  def show_panel(self):
    window = self.view.window()
    rezult = [self.get_panel_item(var) for var in variables]
    window.show_quick_panel(rezult, self.show_var_declaration)

  def show_var_declaration(self, index):
    var = variables[index]
    view = self.view.window().open_file(var.get('file'))
    point = view.text_point(var.get('line') - 1, 0)
    view.sel().clear()
    # if view == self.view.window().active_view():
    #   print('good')
    view.sel().add(sublime.Region(point))
    print(point, var.get('line'))
    view.show(point)

  def get_panel_item(self, var):
    path = var.get('file')
    if nice_path:
      dir = os.path.dirname(path)
      grand_parent = os.path.join(dir, os.pardir)
      path = ''.join([
        os.path.relpath(path,grand_parent),
        ' : ',
        str(var.get('line'))])
    else:
      path = str(var.get('line')) + ' : ' + path
    return [var.get('name'), var.get('value'), path]

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
              'line': i + 1})
        # variant without reading each line, but need some
        # very cool regex but maybe it is not faster?
        # or regex for custom number of groups cant
        # be done?
        # line_num = 1
        # prev_end = 0
        # for match in re_var.finditer(file.read()):
        #   line_num += match.string.count('\n', prev_end, match.start())
        #   prev_end = match.end()
        #   print(line_num, ':', match.groups())
  def process_variable (self, var, max):
    #recursive realization should be here
    pass


# for future use
# all that staff is unaavaibale on 3065 build

def get_selected_variable(view):
  sel = view.sel()[0]
  line = view.line(sel.begin())
  line_str = view.substr(line)
  sel_pos = sel.begin() - line.begin()
  matches = re_var.finditer(line_str)
  for m in matches:
    if m.start()-1 <= sel_pos and m.end() >= sel_pos:
      return m.group()

class Events(sublime_plugin.EventListener):
  def on_modified_async(self, view):
    return#!!!remove this
    var = get_selected_variable(view)
    print(var)
    if var:
      show_popup(var, view)
