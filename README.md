# yppm
Yingshaoxo Python Package Manager

## Install
```bash
sudo su
curl -sSL https://raw.githubusercontent.com/yingshaoxo/yppm/main/Install.sh | bash
curl -sSL https://bootstrap.pypa.io/get-pip.py | python3

# Use github on care, you may get banned(404) by saying the 'fuck' word: https://yingshaoxo.xyz/pictures/github/index.html
```
<!--

or

```bash
python3 -m pip install yppm --break-system-packages
alias yppm="python3 -m yppm" && echo "alias yppm='python3 -m yppm'" >> ~/.bashrc && source ~/.bashrc

yppm about
```
-->

or

```bash
git clone https://gitlab.com/yingshaoxo/yppm.git
cd yppm/yppm
python3 ./main.py

echo "alias yppm='python3 $(pwd)/main.py'" >> ~/.bashrc && source ~/.bashrc
```

## Usage
### Init a project
```bash
cd <your_project_folder>
yppm init

or

yppm create_a_new_project
```

### Install a package
```bash
yppm install auto_everything
```

### Install all package
```bash
yppm install
```

### Uninstall a package
```bash
yppm uninstall ?
```

### Run a script in package.json
```bash
yppm run ?
```

or 

```bash
yppm run <script_name>
```

### Build a project
```bash
yppm build
```

## Feature
### Finished
* npm package.json like syntax.
* Can compile a python project into a single binary file.
* Has a backend and frontend template built_in (similar to SpringBoot).
* File_path based relative import supporting for main.py file. (`import "./lib.py" as lib_module`)
### Not Finished
* Built in python binary files that will never upgrade, and free to use offline

## Based on
* venv: https://packaging.python.org/en/latest/key_projects/#standard-library-projects
* auto_everything: https://gitlab.com/yingshaoxo/auto_everything
