 # frac-comp

Scientific Programming I exam project: Fraction comparison between different final states of e+e- collision

[![ReadTheDocs](https://readthedocs.org/projects/docs/badge/?version=latest)](https://cmepda-pikclassifier.readthedocs.io/en/latest/index.html)

## Authors

- [@lorenzopunzi](https://github.com/LorenzoPunzi)
- [@rubenforti](https://github.com/rubenforti)


## Documentation

[Documentation](https://cmepda-pikclassifier.readthedocs.io/en/latest/index.html)


## Install

Clone the project

```bash
  git clone https://github.com/LorenzoPunzi/cmepda-PiKclassifier.git
```

Install dependencies from inside the project directory

```bash
  pip install -r cmepda-PiKclassifier/requirements.txt
```
_PLEASE NOTE_ : ROOT is not in requirements.txt file but is needed to run the template fit module. The package works as of ROOT v6.26/10.
Also, the requirements are NOT strict, meaning that former versions could potentially work.

To run the project as a package, add the following code in the .bashrc (or .bash_profile, for MAC users):
```bash
  export PYTHONPATH="/path/to/cmepda-PiKclassifier"
```


## Run

The package can be run as a whole using the main with parser:

```bash
  python cmepda-Pikclassifier [generic options] <subparser name> [subparser options]
```

### Datasets generation
To generate the MC and data sets for the analysis use the "gen" subparser, for exaple:
```bash
  python cmepda-Pikclassifier gen -f 0.42
```

### Perform the analysis
The analysis can be done by using the "analysis" subparser, once that the MC and data sets are generated. For example, a command that covers all the analyses and saves the figure in an apposite folder in the current directoty is:
```bash
  python cmepda-Pikclassifier -fig analysis -m all -ld -err
```

## Running Tests

To run tests, run the following command inside the project directory

```bash
  python -m unittest discover -s tests
```
