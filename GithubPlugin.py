"""
@author Yaakov Sokolik
@since Jan 18, 2017
"""

from datetime import datetime

import pytz
from dateutil.tz import tzoffset
from github3 import login, GitHubError
from pytz import utc


class GithubPlugin:
    """
    @:param
    """
    def __init__(self, username, token, repoName, name, email):
        self.name = name
        self.email = email
        self.username = username
        self.token = token
        self.gh = login(username, token)
        self.repo = self.gh.repository(username, repoName)

    def recursiveFileSearch(self, path):
        files = self.repo.contents(path)
        for f in files:
            try:
                contents = self.repo.contents(path + f)
                if isinstance(contents, dict):
                    self.recursiveFileSearch(path + f + "/")
                else:
                    # this is a single file
                    #TODO: now operates only on java files
                    if contents.name.endswith(".java"):
                        file_content = contents.decoded.decode("utf-8")

                        #TODO: add real javadoc comment
                        new_file_content = file_content + "\nMulti-file commit via the GitHub API!\n"
                        new_file_blob = self.repo.create_blob(new_file_content, encoding="utf-8")
                        branch = self.repo.branch(self.repo.default_branch)
                        tree_sha = branch.commit.commit.tree.sha

                        #Creating a new tree is done with the Repository.create_tree method.
                        tree_data = [{"path": path.lstrip("/") + f, "mode": "100644", "type": "blob", "sha": new_file_blob}]
                        tree = self.repo.create_tree(tree_data, tree_sha)

                        #And finally I can make a new commit with this new tree. The current branch"s commit is used as the parent of the new commit.
                        message = "add doc comment to file:" + path + f
                        tz = pytz.timezone("Asia/Jerusalem")
                        now = (tz.localize(datetime.now()).replace(microsecond=0)).isoformat()
                        print(now)
                        commitor = {"name": self.name, "email": self.email, "date": str(now)}
                        c = self.repo.create_commit(message, tree.sha, [branch.commit.sha], commitor, commitor)

                        #At this point I"ve made the commit but the "master" branch reference is still pointed at the previous commit. I"ll need to make another API call to update where the branch is pointed.
                        ref = self.repo.ref("heads/{}".format(self.repo.default_branch))
                        ref.update(c.sha)

            except GitHubError:
                continue