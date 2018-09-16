## Usage
PySite reads from `./_template/` for the source HTML files. Place an `index.html` file there for it to compile the home page to. Place your markdown files in the root directory, and name them `template page name-page name.md`. For the home page Markdown file, simply name it `index.md`. 

If you have a file called called `post.html` in `./_template/` and want a page with that layout, just create a markdown file in the root called `post-Page-Name.md`. 

Create a `_config.json` file in the root to provide site-specific info to the compiler. It is best practice to make all or most parameters in the template optional, so you don't get an error if that information is missing in the config. 