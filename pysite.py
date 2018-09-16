import json
import sys
import mistune
import string
import os
from types import SimpleNamespace

args = sys.argv


class TemplateFormatter(string.Formatter):
	# More Advanced Template Formatter. source: https://github.com/ebrehault/superformatter
	def format_field(self, value, spec):
		if spec == "do":
			return value()

		elif spec.startswith("loop"):
			template = spec.partition(":")[-1]
			if type(value) == dict:
				value = value.items()

			return ''.join([template.format(item = item)for item in value])

		else:
			return super(TemplateFormatter, self).format_field(value, spec)


tf = TemplateFormatter()


markdown = mistune.Markdown()

def get_file_name(raw_name):
	split_file = raw_name.split("-")

	template_type = split_file[0]
	file_name = '-'.join(split_file[1:])
	file_extension = file_name.split(".")

	file_name_noext = "".join(file_extension[:-1])

	return {
		"template": template_type,
		"name": file_name_noext
	}

def for_md_files(function_name):
	for subdir, dirs, files in os.walk("."):
		for file in files:
			if file.endswith(".md") and file != "index.md" and file.lower() != "readme.md":
				print("file: " + file)

				with open(file, "r") as f:
					file_content = f.read()
					file_md = markdown(file_content)
				function_name(subdir, dirs, files, file, file_md, file_content)


try:
	with open("_config.json") as cfg:
		config_file = cfg.read()
		cfg.close()
except FileNotFoundError:
	print("""Error: No config file found. Please create an _config.json file and try again. 
	For more information please see the PySite Docs.""")

# Reads config file and sets it to a dict
config_raw = json.loads(config_file)

# Makes file accessible via dot notation, eg config.title
config = SimpleNamespace(**config_raw)

print("Loaded config file at _config.json:")
print (config)
print("\n")

# Opens all the files and gives them vars

try:
	with open("index.md") as index:
		md_index = index.read()
		index.close()
except FileNotFoundError:
	print("Error: No index file found. Please create an index.md file and try again.")

try:
	with open("./_template/index.html") as index_html:
		template_index = index_html.read()
		index_html.close()
except FileNotFoundError:
	print("Error: No index template file found. Please create an index.html file and try again.")


def write_public (file_content, file_path):
	try:
		with open("." + os.sep + "public" + os.sep + file_path, "w+") as f:
			f.write(file_content)
			f.close()
	except FileNotFoundError:
		print("Create a public directory to continue")

# Uses Mistune to compile the markdown.


formatted_index = markdown(md_index)
truncated_index = formatted_index[:30] + "..."
print("Compiled `index.md` as \n" + truncated_index)

post_info = []

@for_md_files
def create_list_of_pages(subdir, dirs, files, file, file_md, file_content):
	file_name = get_file_name(file)['name']
	file_url = "/" + file_name + ".html"
	post_info.append({
		'name': file_name,
		'url': file_url
	})


print(post_info)
tf.format(template_index, pages = post_info, site = config, index = formatted_index)
# pub_index = template_index.format(index = formatted_index, site = config)

write_public(pub_index, "index.html")

# Writing `/_template/static/` folder to public
# TODO: add compilation for pre-processers (SASS, LESS, COFFEE)

static_dir = os.path.join("_template", "static")

for subdir, dirs, files in os.walk(static_dir):
	for file in files:
		print(os.path.join(subdir, file))
		filepath = subdir + os.sep + file

		with open(filepath, "r") as f:
			file_content = f.read()
			print(filepath)
			print(file)
			print("." + os.sep + "public" + os.sep + "static" + os.sep + file)
			write_public(file_content, "static" + os.sep + file)
			f.close()

# Reads each .md file, looks for a template with same name before -
print("\n")


@for_md_files
def compile_all(subdir, dirs, files, file, file_md, file_content):
	
	file_name = get_file_name(file)
		
	with open("_template" + os.sep + file_name.template + ".html", "r") as t:
		template = t.read()
		formatted = template.format(page = file_md, site = config)

	write_public(formatted, file_name.name + ".html")
	print(str(file_name_noext))



