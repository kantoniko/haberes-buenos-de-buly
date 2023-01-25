import os
import pathlib
import shutil
from jinja2 import Environment, FileSystemLoader

cwd = pathlib.Path.cwd()
sound = cwd.joinpath('sound')
site  = cwd.joinpath('_site')

def render(template, filename, **args):
    templates_dir = pathlib.Path(__file__).parent.joinpath('templates')
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    html_template = env.get_template(template)
    html_content = html_template.render(**args)
    with open(filename, 'w') as fh:
        fh.write(html_content)


def generate(pages):
    pages.sort(key=lambda page: page['id'])
    for ix in range(len(pages)):
        if ix == 0:
            pages[ix]['prev_message'] = pages[-1]['id']
        else:
            pages[ix]['prev_message'] = pages[ix - 1]['id']

        if ix == len(pages) - 1:
            pages[ix]['next_message'] = pages[0]['id']
        else:
            pages[ix]['next_message'] = pages[ix + 1]['id']

    render('index.html', site.joinpath('index.html'),
        title = "Haberes Buenos de Buly",
        pages = pages,
    )
    for page in pages:
        render('page.html', site.joinpath(f'{page["id"]}.html'),
            title = f"{page['id']} - {page['titulo']}",
            page = page,
        )

def collect_pages():
    pages = []
    md_files = os.listdir('text')
    for md_file in sorted(md_files, key=lambda filename: int(filename[:-3])):
        print(md_file, end="")
        with open(os.path.join('text', md_file)) as fh:
            fh.readline()
            page = {}
            page['id'] = int(md_file[0:-3])
            audio_file = os.path.join('sound', f"{page['id']}.mp3") 
            if not os.path.exists(audio_file):
                print("    missing audio", end="")
            page['audio'] = os.path.exists(audio_file)
            for row in fh:
                if row.startswith('---'):
                    break
                # print(row)
                field, value = row.split(':')
                page[field] = value

            page['text'] = fh.read()
            page['paragraphs'] = page['text'].split("\n")
            #print(page)
            pages.append(page)
        print("")
    return pages

def copy_audio():
    for file in sound.iterdir():
        shutil.copy(file, site.joinpath(file.name))
    shutil.copy(cwd.joinpath('front.jpeg'), site.joinpath('front.jpeg'))

def main():
    os.makedirs('_site', exist_ok=True)

    pages = collect_pages()
    generate(pages)
    copy_audio()



main()
