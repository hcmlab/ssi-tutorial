import os, argparse, re, sys, subprocess, datetime


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


def convert(args):

    name, _ = os.path.splitext(os.path.basename(args.path))    
    dir = os.path.dirname(args.path)
    name_pipe = name + '.pipeline'
    path_pipe = os.path.join(dir, name_pipe)
    name_html = name + '.html'
    path_html = os.path.join(dir, name_html)
    name_md = name + '.md'
    path_md = os.path.join(dir, name_md)

    regex = re.compile(r'<!--(.*?)-->(.*?)<!-->', re.DOTALL)    

    print('{}: {}'.format(dir, name_pipe), end='')

    with open(path_pipe, 'r')  as fp_pipe, open(path_md, 'w') as fp_md:

        fp_md.write('% {}\n% {}\n% {}\n\n'.format(os.path.join(dir, name), args.author, datetime.datetime.today().strftime('%Y-%m-%d')))

        pipe = fp_pipe.read()                
        matches = [m.groups() for m in regex.finditer(pipe)]
        for m in matches:
            fp_md.write('{}\n\n``` xml\n{}\n```\n\n'.format(unindent(m[0]).strip(), unindent(m[1]).strip()))        
        
    print(' > {}'.format(name_md), end='')    

    p = subprocess.Popen('pandoc -o {} -s -f markdown --number-sections --template ../templates/standalone.html --css ../templates/template.css --toc --toc-depth=4 {}'.format(name_html, name_md), cwd=dir)
    p.wait()

    print(' > {}'.format(name_html))    

    os.remove(path_md)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert pipeline to a html document.')
    parser.add_argument('path', metavar='path', type=str, help='path to pipeline')
    parser.add_argument('--author', metavar='author', type=str, help='name of author', default='Unkown')
    args = parser.parse_args()

    convert(args)