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
If a variable is not given, the program will prompt the user to do so.

### Input Files
Furthermore, some form of input must be given by the user in order to locate the fraction files to compare. 
The input files can be given directly, by entering two paths to the files separated by a space following the variable,
```bash
  python frac-comp pi inputfile1.txt dir/inputfile2.txt [options]
```
or they can be selected from those in a given directory by using ``search`` mode
```bash
  python frac-comp mu -search dir/of/files/ [options]
```
In this case the program will list all files with ``.txt`` and ``.dat`` extensions in the given directory. The user will be then prompted to choose two options from the listed files.

### File Parsing Rules
The input files must both contain a header line with the respective variable (``QQ_pipi`` or ``QQ_mumu``), the four channels (``ppg,mmg,eeg,ppp``) and their errors (``dppg,dmmg,deeg,dppp``). The program then parses the following lines, looking for floats in the same colums as the respective names in the header. There can be extra columns in the header row and the number rows, as long as the ones necessary are present and the number columns are in the order of their respective channels in the header. The values in each row, header or number, must be separated by only one tab character, followed or preceded by any number of whitespaces.
As soon as the program encounters a row that is not correctly formatted as a numer row, it will stop looking for fractions to take as input. Therefore, if a file has multiple headers, only the first and its following data rows are recorded.
The two fraction files must have an identical number of data rows, or else the program will return an error.

### Other Options

There are multiple options to choose from to manipulate the fractions given as input. To find the commands for each option run

```bash
  python frac-comp --help
```
or 
```bash
  python frac-comp -h
```
#### Save Directory

By default, the program calculates the residuals of the fractions (differences between fractions of the same channels from the two files) as a function of the chosen variable. It also saves them, along with their errors calculated with standard error propagation, in an output file called ``residuals.dat`` in a directory called ``output``. The user can choose another directory with the ``-svdr,--savedir`` option, e.g.

```bash
  python frac-comp pi -search -svdr my/other/directory
```

#### Analyze Subrange

By default, the program performs its analysis between in the Q^2 range [0.32, 0.96]. If the ``-sbrg,--subrange`` option is given, the user can specify a subrange of the default range in which to perform the analysis. The program will insist that the user given ends of the subrange be within the default range, if that happended not to be the case. Here is an example of this option in use:

```bash
  python frac-comp pi -search -sbrg 0.36 0.48
```

#### Display Fractions and Residuals and Save the Figure

The user can ask the program to show a figure of the fractions and their residuals as a function of the chosen variable, using the ``-fig,--figure``. One figure is shown for each of the four channels.

If the ``-svfg,--savefig`` option is given, the four figures will be saved. If no argument follows the optionflag, the figures are saved to the current working directory. If, however, a path is specified after the flag, they will be saved in the provided directory:

```bash
  python frac-comp pi -search --savefig my/savefig/directory
```

#### Fit the Residuals with a Constant

The user can fit the residuals with a constant, assuming all fractions are independent. The fit is done minimizing the chi square of the residuals, which is then printed to command line, along with the fit results. If the residuals are displayed using ``-fig,--figure`` or ``-svfg,--savefig``, the best fit constant line will be depicted in the figures.
