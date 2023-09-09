 # frac-comp

Scientific Programming I exam project: Fraction comparison between different final states of e+e- collision

[![ReadTheDocs](https://readthedocs.org/projects/docs/badge/?version=latest)](https://frac-comp.readthedocs.io/en/latest/index.html)

## Authors

- [@lorenzopunzi](https://github.com/LorenzoPunzi)

## Documentation

[Documentation](https://frac-comp.readthedocs.io/en/latest/index.html)

## Install

Clone the project

```bash
  git clone https://github.com/LorenzoPunzi/frac-comp.git
```

To install dependencies from inside the project directory

```bash
  pip install -r frac-comp/requirements.txt
```

The requirements are NOT strict, meaning that former versions probably work just fine.

To run the project as a package, add the following code in the .bashrc (or .bash_profile, for MAC users):
```bash
  export PYTHONPATH="/path/to/frac-comp"
```

## Run

The package can be run as a whole using the main with parser:

```bash
  python frac-comp  <variable >  <input> [options]
```

### Variable Choice
In order to use the program, a variable must be chosen by the user, between ``pi`` (to analyze in ``QQ_pipi``) and ``mu`` (to analyze in ``QQ_mumu``). For example
```bash
  python frac-comp pi [options]
```

### Input Files
In order to use the program, some form of input must be given by the user in order to locate the fraction files to compare. 
The input files can be given directly, by entering two paths to the files separated by a space following the variable,
```bash
  python frac-comp pi inputfile1.txt dir/inputfile2.txt [options]
```
or they can be selected from those in a given directory by using ``search`` mode
```bash
  python frac-comp mu -search dir/of/files/ [options]
```


### Perform the analysis
The analysis can be done by using the "analysis" subparser, once that the MC and data sets are generated. For example, a command that covers all the analyses and saves the figure in an apposite folder in the current directoty is:
```bash
  python frac-comp -fig analysis -m all -ld -err
```

