import os, argparse, re, sys, subprocess, datetime, glob, ast


regex_comments = re.compile(r'<!--(.*?)-->(.*?)<!---->', re.DOTALL)
regex_input = re.compile(r'.*\\input{(.*?)}.*')
regex_input_parse = re.compile(r'(.*)=(.*)')


def rem_spaces(text, numDel):

    def aux(line, numDel=numDel, white=' '*numDel):
        if line[:numDel] != white:
            return line
        return line[numDel:]
    return ''.join(map(aux, text.splitlines(1)))


def num_spaces(text):

    s = os.linesep.join([s for s in text.splitlines() if s.strip()])
    return [len(line) - len(line.lstrip()) for line in s.splitlines()]


def unindent(text):      

    text = text.replace('\t', ' '*4)
    return rem_spaces(text, min(num_spaces(text)))


def get_funpos(tree, name, num_lines):

    pos = None

    for i, node in enumerate(tree.body):
        if isinstance(node, ast.FunctionDef) and node.name == name:        
            start = node.lineno
            end = tree.body[i+1].lineno-1 if i+1 < len(tree.body) else num_lines
            pos = (start-1, end-1)

    return pos


def get_funcode(tree, name, lines):

    start, end = get_funpos(tree, name, len(lines))
    
    return '\n'.join(lines[start:end]).strip()


def parse_input_params(text):

    params = {'path' : None, 'lines' : None, 'function' : None, 'type' : '' }

    for line in text.split(';'):
        m = regex_input_parse.match(line)        
        if m and m[1] in params:            
            params[m[1]] = eval(m[2]) if m[1] == 'lines' else m[2]

    return params

    
def parse_input(text, dir, name):

    params = parse_input_params(text)
    path = (os.path.join(dir, params['path']) if params['path'] else os.path.join(dir, name) + '.py')
    code = None

    if os.path.exists(path):

        with open(path, encoding='utf-8-sig') as fp:
            content = fp.read()
        lines = content.split('\n')                

        if params['function']:
            tree = ast.parse(content)
            code = get_funcode(tree, params['function'], lines)
        elif params['lines']:
            code = '\n'.join(lines[i] for i in params['lines'])            
        else:            
            code = content             

    return code, params['type']


def replace_input(text, dir, name):

    try:

        lines = text.split('\n')

        new_lines = []
        for i, line in enumerate(lines):
            m = regex_input.match(line)
            if m:    
                code, type = parse_input(m[1].strip(), dir, name)
                if code:
                    new_lines.append('``` {}\n{}\n```\n\n'.format(type, unindent(code).strip()))
            else:
                new_lines.append(line)

        return '\n'.join(new_lines)

    except Exception as ex:

        print()
        print(ex)
        
        return text


def convert(args, path):

    name, _ = os.path.splitext(os.path.basename(path))    
    dir = os.path.dirname(path)
    name_pipe = name + '.pipeline'
    path_pipe = os.path.join(dir, name_pipe)
    name_html = name + '.html'
    path_html = os.path.join(dir, name_html)
    name_md = name + '.md'
    path_md = os.path.join(dir, name_md)
    name_cmd = name + '.cmd'
    path_cmd = os.path.join(dir, name_cmd)
    
    match = re.match(r'(\d+).(.*)', os.path.basename(dir))
    tutorial_num = int(match[1]) if match else ''
    tutorial_name = (match[2] if match else os.path.basename(dir)).replace('_', ' ')
    match = re.match(r'(\d+).(.*)', name)
    example_num = int(match[1]) if match else ''
    example_name = (match[2] if match else name).replace('_', ' ')        

    print('{}: {}'.format(dir, name_pipe), end='')

    with open(path_pipe, 'r')  as fp_pipe, open(path_md, 'w') as fp_md:

        fp_md.write('% Tutorial {}: {}\n% Example {}: {}\n% [![]({})](http://openssi.net)\n\n'.format(tutorial_num, tutorial_name, example_num, example_name, args.logo.replace('\\', '/')))

        pipe = fp_pipe.read()                
        matches = [m.groups() for m in regex_comments.finditer(pipe)]
        for m in matches:            
            if m[0].strip():
                text = replace_input(unindent(m[0]).strip(), dir, name)
                fp_md.write('{}\n\n'.format(text)  )      
            if m[1].strip():                
                fp_md.write('``` xml\n{}\n```\n\n'.format(unindent(m[1]).strip()))                        
        
    print(' > {}'.format(name_md), end='')    

    p = subprocess.Popen('pandoc -o {} -s -f markdown --number-sections --template ../templates/standalone.html --css ../templates/template.css --toc --toc-depth=4 {}'.format(name_html, name_md), cwd=dir)
    p.wait()

    print(' > {}'.format(name_html), end='')    

    with open(path_cmd, 'w') as fp:
        fp.write('@echo off\n')
        fp.write(r'{}\xmlpipe -log ssi.log {}'.format(args.bin, name))

    print(' > {}'.format(name_cmd), end='\n')    

    os.remove(path_md)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert pipeline to a html document.')
    parser.add_argument('path', metavar='path', type=str, help='path to pipeline or a folder with pipelines')
    parser.add_argument('--logo', metavar='logo', type=str, help='path to logo', default=r'..\pics\ssi.png')
    parser.add_argument('--bin', metavar='bin', type=str, help='path to binaries', default=r'..\bin')    
    args = parser.parse_args()

    if os.path.isdir(args.path):
        for path in glob.glob(os.path.join(args.path, '*.pipeline')):
            convert(args, path)
    else:
        convert(args, args.path)