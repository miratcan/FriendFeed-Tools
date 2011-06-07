import sys
sys.path.append("..")

try:
    from jinja2 import Environment, PackageLoader
except ImportError:
    raise ImportError("You need to install Jinja2 template system to run this application.")

class FriendFeedHtmlMigration(object):
    def __init__(self):
        self.environment = Environment(loader=PackageLoader('ffmigration', 'templates'))
        self.template = self.environment.get_template("base.html")

    def run(self, feed_data, output_file_path=None):
        render = self.template.render(feed_data).encode("UTF-8")
        if output_file_path:
            output_stream = file(output_file_path, "w")
        else:
            output_stream = file(feed_data['id'] + ".html", "w")
        output_stream.write(render)
        output_stream.close()
        return render

                                       
