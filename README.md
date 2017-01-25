# since-authorAdder
A GitHub plugin that adds since &amp; author and description notes to all code files that miss it in a project
Written originally by Raviv Rachmiel <ravivra@campus.technion.ac.il> & Yaakov Sokolik <yaakovs@gcampus.technion.ac.il>

##Working with the program:
### Working on a local repository:
    You can use the program in order to add the since,author, description convention to your java code files by
    calling main.py with the path of the local git repository.
    The program will add the right @since, @author and descriptions needed exactly where they are needed to each file
### Working on a Github repository:
    You can use the program in order to add the since,author, description convention to your java code files by
    calling main.py with the URL of the repo, your username and your mail.
    The program will add the right @since, @author and descriptions needed exactly where they are needed to each file.
    Also, the program will clone automatically the repo to a temp directory, make the changes, commit them and push to
    the github repository (so you have to have the right privileges for the repo).
    At the end, it will delete the temp folder it cloned


##Usage:
    ###For a local git repo:
        python3 main.py <local git repo path>
    ###for a Github:
        python3 main.py <github repo URL> <user.name> <user.mail>
        * the user.name has to be either 1 word, or a couple of words wrapped by ""
        * the <user.name> and <user.mail> are for the commit info
        * you have to have the right priviliges in order to push to the github repo of course


Enjoy :)



