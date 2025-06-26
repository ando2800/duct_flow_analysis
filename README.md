## Using the Project Template Generator
Open a terminal in the project root(./duct_flow_analysis).
Run the following command:

```
 python templates/new_project.py
```
Select the template you want to use:
```
1. Test template
2. Experiment template
Enter the number [1/2]:
```
A new directory such as test01 or exp01 will be created under test/ or experiments/, based on your selection.

### Template Contents
1. Each new folder is initialized from either:

- templates/project_template/

- templates/project_template/

2. These templates can include files like:
  
- README.md
- data/raw, data/processed
- results/

You can freely customize these templates.

### Notes
Existing folders like exp01, exp02, ... will be automatically detected, and the next available number is used.

