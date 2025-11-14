# TeamMate_Finder
Initial failure: render_template not defined.
Cause: missing import.
Action: added from flask import Flask, render_template.

Second failure: TemplateNotFound: index.html.
Cause: HTML file placed in project root instead of templates/.
Action: created templates directory and moved index.html inside.


