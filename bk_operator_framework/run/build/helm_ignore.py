import os

helm_ignore = """# Patterns to ignore when building packages.
# This supports shell glob matching, relative path matching, and
# negation (prefixed with !). Only one pattern per line.
.DS_Store
# Common VCS dirs
.git/
.gitignore
.bzr/
.bzrignore
.hg/
.hgignore
.svn/
# Common backup files
*.swp
*.bak
*.tmp
*.orig
*~
# Various IDEs
.project
.idea/
*.tmproj
.vscode/
"""


def build_helm_ignore(version_helm_charts_dir):
    helm_ignore_path = os.path.join(version_helm_charts_dir, ".helmignore")
    with open(helm_ignore_path, "w") as f:
        f.write(helm_ignore)
