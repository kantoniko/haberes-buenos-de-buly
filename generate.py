import os
import pathlib
import shutil
from jinja2 import Environment, FileSystemLoader

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

    render('index.html', '_site/index.html',
        title = "Haberes Buenos de Buly",
        pages = pages,
    )
    for page in pages:
        render('page.html', f'_site/{page["id"]}.html',
            title = f"{page['id']} - {page['titulo']}",
            page = page,
        )

def collect_pages():
    pages = []
    md_files = os.listdir('text')
    for md_file in md_files:
        print(md_file)
        with open(os.path.join('text', md_file)) as fh:
            fh.readline()
            page = {}
            page['id'] = int(md_file[0:-3])
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
    return pages

def main():
    os.makedirs('_site', exist_ok=True)

    for filename in os.listdir('sound'):
        shutil.copy(os.path.join('sound', filename), os.path.join('_site', filename))
    shutil.copy('front.jpeg', '_site/front.jpeg')

    pages = collect_pages()
    generate(pages)



main()
