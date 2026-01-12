from thonny import get_workbench
from tkinter.messagebox import showinfo, showerror


def fill_init():
    import ast
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if not editor:
        showerror("Fill class init", "No editor opened!")
        return
    text = editor.get_text_widget()
    programm = editor.get_content()
    programm_lines = programm.splitlines()
    cursor = text.index("insert")
    c_line, c_column = map(int, cursor.split("."))
    if c_line > len(programm_lines):
        showerror("Fill class init", "Cursor out of programm!")
        return
    if c_line < 2:
        showerror("Fill class init", "Cursor at beginning of programm!")
        return
    init_func = programm_lines[c_line-2].strip()
    init_dummy = init_func+"\n    pass"
    try:
        tree = ast.parse(init_dummy)
    except:
        showerror("Fill class init", "No valid func defition found above cursor!")
        return
    func = tree.body[0]
    self_a = func.args.args[0].arg
    definitions = []
    for arg in func.args.args[1:]:
        definitions.append(f"{self_a}.{arg.arg} = {arg.arg}")
    def_str = ("\n" + " "*c_column).join(definitions)
    text.insert(cursor, def_str)
    

def load_plugin():
    get_workbench().add_command(command_id="fill_class_init",
                                menu_name="tools",
                                command_label="Fill class init!",
                                handler=fill_init)