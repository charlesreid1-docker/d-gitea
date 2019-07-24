import os, re, sys
import glob
import subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape

"""
Apply Default Values to Jinja Templates


This script applies default values to 
templates in this folder.

The templates are used by Ansible,
but this script uses the same template
engine as Ansible to apply template
variable values to the template files
and make real files.

variables are:
- `gitea_app_name` - name of gitea app (?)
- `server_name_default` - name of server (e.g., charlesreid1.com)
- `gitea_secret_key` - secret key for gitea
- `gitea_internal_token` - internal token for gitea
"""


# Where templates live
TEMPLATEDIR = '.'

# Where rendered templates will go
OUTDIR = '.'

# Should existing (destination) files 
# be overwritten if they exist?
OVERWRITE = True

# Template variables
TV = {
        'gitea_app_name':       'charlesreid1.red',
        'server_name_default':  'charlesreid1.red',
        'gitea_secret_key':     'abc123',
        'gitea_internal_token': '123abc'
}



def apply_templates(template_dir, output_dir, template_vars, overwrite=False):
    """Apply the template variables 
    to the template files.
    """

    if not os.path.exists(output_dir):
        msg = "Error: output dir %s does not exist!"%(output_dir)
        raise Exception(msg)

    if not os.path.exists(template_dir):
        msg = "Error: template dir %s does not exist!"%(output_dir)
        raise Exception(msg)

    # Jinja env
    env = Environment(loader=FileSystemLoader('.'))

    # Render templates
    tfile = 'app.ini.j2'
    rfile = 'app.ini'

    # Get rendered template content
    content = env.get_template(tfile).render(**template_vars)

    # Write to file
    dest = os.path.join(output_dir,rfile)
    if os.path.exists(dest) and overwrite is False:
        msg = "Error: template rendering destination %s already exists!"%(dest)
        raise Exception(msg)

    with open(dest,'w') as f:
        f.write(content)

    print("Rendered the following templates:%s\nOutput files:%s\n"%(
            "\n- "+os.path.join(output_dir,tfile),
            "\n- "+os.path.join(output_dir,rfile)
    ))


if __name__=="__main__":
    apply_templates(TEMPLATEDIR,OUTDIR,TV,OVERWRITE)

