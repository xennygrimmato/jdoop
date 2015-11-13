# Introduction

JDoop (previously known as JPF-Doop) is a free software testing tool
for Java libraries. It is based on the [Java PathFinder][8]'s concolic
execution engine [JDart][0] and [Randoop][1], a feedback-directed
random testing engine. More detailed description of JDoop can be found
in an extended abstract by Marko Dimjašević and Zvonimir Rakamarić:
[JPF-Doop: Combining Concolic and Random Testing for Java][5].

# Dependencies

JDoop includes a few tools that ship independently of JDoop, but they
are bundled with JDoop for convenience: [JaCoCo][6], [JUnit][7]
version 4, and [Randoop][1].

The following need to be obtained and configured by the user:

* [Java PathFinder][8],
* [JDart][0],
* [Python][3], version 2.7.

If the user wishes to generate code coverage reports, [Apache Ant][4]
is needed too.

# Installation and Configuration

After you've cloned the repository, there is no installation of JDoop
because it consists of scripts written in Python. In other words, you
can run JDoop as soon as you obtained a copy of it (and you have all
the dependencies in place). In order to have all JDoop dependencies
easily installed, you might want to take a look at an installation
script `install-dep.sh` in the `env/` directory and possibly tweak a
few parameters at the very top of the script.

You can configure various parameters in `jpfdoop.ini`. Most
importantly, change `jpf-core` and `jpf-jdart` in the `jpfdoop`
section so that they point to the main directories of jpf-core and
JDart, respectively. Do not use `~` as a shorthand for your home
directory.

## Configuration file

JDoop uses a configuration file. By default, it is `jpfdoop.ini`. The
file is in the INI file format. It has 4 sections: `[jpfdoop]`,
`[sut]`, `[tests]`, and `[lib]`. For an example, see the contents of
`jpfdoop.ini`.

Section `[jpfdoop]` has two options. Option `jpf-core` specifies a
path to Java PathFinder (core module), while option `jpf-jdart`
specifies a path to JDart.

Section `[sut]` has one option: `compilation-directory` specifies a
directory where class files of the package being tested can be found.

Section `[tests]` has one option: `compilation-directory` specifies a
directory where should generated JUnit tests be compiled to.

Section `[lib]` has three options that specify where various libraries
can be found. Option `junit` is a path to a JUnit *jar*
archive. Option `randoop` is a path to a Randoop *jar*
archive. Finally, option `jacoco` is a path to a JaCoCo *jar* archive.


# Usage

To run JDoop, a few parameters need to be passed to it, including a
package name and where the package's source and class files are. Other
arguments are optional. For example, to test the
`org.apache.commons.collections` package from the Apache Commons
library from the [JDoop-examples][2] repository, assuming that
JDoop and `JDoop-examples` are on the same directory hierarchy
level, run the following:

```bash
python jpfdoop.py --package-name org.apache.commons.collections --root ../jdoop-examples/
```

A code coverage report will be generated and can be found in the
`jacoco-site/` directory. JDoop will generate two formats of the
report - HTML (to be found in `jacoco/site/html/index.html`) and XML
(to be found in `jacoco-site/report.xml`).

For further information on how to run JDoop, you can execute:

```bash
python jpfdoop.py --help
```

The user should make sure that files generated by previous executions
of JDoop are cleaned up before running JDoop again. In
particular, the following files and directories in JDoop's root
directory should be removed:

* `tests-round-*`
* `build/`
* `concrete-values*`
* `classlist.txt`
* `jacoco-site/`
* `jdart-regular-executions.txt`
* `randooped*`

There is a `bash` script in the repository that removes these files
and directories: `clean.sh`.


## Command line parameters

JDoop has several command line parameters:

* `--package-name` - a required parameter with the name of a package
  you want to test (e.g. `org.apache.commons.collections`).
* `--root` - a required parameter with a directory where source files
  of the package are.
* `--classlist` - an optional parameter (with the default value
  `classlist.txt`) where the list of classes from the package will be
  written to.
* `--timelimit`- an optional parameter (with the default value `120`)
  with a time limit for JDoop, in seconds. If `--generate-report`
  is provided too, after the time limit is reached, JDoop will
  compile generated JUnit tests and generate a code coverage
  report. In other words, compilation and report generation execution
  times are not included in the time limit.
* `--configuration-file` - an optional parameter (with the default
  value `jpfdoop.ini`) with a name of a configuration file in the INI
  file format. More about options within the configuration file are
  given in section *Configuration file*.
* `--randoop-only` - an optional parameter (with the default value
  false) that specifies if only Randoop should be executed.
* `--baseline` - an optional parameter (with the default value false)
  that specifies if only baseline JDoop should be executed. For
  more information on the baseline solution, see an
  [extended abstract][5] on JDoop.
* `--generate-report` - an optional parameter (with the default value
  false) that specifies if a code coverage report should be generated
  once JDoop is done with its execution. If the parameter is
  provided, [JaCoCo][6] will be executed to generate a code coverage
  report for JUnit tests that JDoop generated. If this option is
  not provided, the user can generate the code coverage report
  herself, as described in section *Generating code coverage reports*.

# Generating code coverage reports

JDoop has a script that generates a code coverage report for JUnit
tests that can be used without JDoop, i.e. unit tests can be
generated or obtained in some other way. The script is `report.py`,
and it has a few dependencies. First of all, clone this repository. In
addition, the following is needed:

- [Python][3], version 2.7,
- [Apache Ant][4].

To get help on how to run the code coverage script from the command
line, type:

```bash
python report.py --help
```

The script takes 6 arguments, where the `--jacocopath` argument is
optional. There is an example package named `branching` in the
`report-examples/` directory. If you build the example in such a way
that `.class` files are in the same directory where respective `.java`
files are, this is how you would generate a code coverage report for
the example:

```bash
python report.py --unittests TestBranching --classpath report-examples/:report-examples/branching/tests/ --sourcepath report-examples/ --packagepath branching --buildpath report-examples/
```

The `report.py` script will generate a code coverage report in two
formats - HTML and XML. Both can be found in the `jacoco-site/`
directory.

# Emulab

To thoroughly evaluate JDoop, we have been using [Emulab][9], a
network testbed developed and provided by the
[Flux Research Group][10] at the University of Utah.


# Copyright
Copyright 2015 Marko Dimjašević

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

JDoop dependencies, including those in the `lib/` directory, are free
software as well, each licensed under its own license. Follow links to
respective web pages listed in the *Dependencies* section to find out
more.


[0]: https://github.com/psycopaths/jdart
[1]: https://bitbucket.org/psycopaths/randoop
[2]: https://github.com/psycopaths/jdoop-examples
[3]: http://python.org
[4]: https://ant.apache.org/
[5]: http://dimjasevic.net/marko/wp-content/uploads/2013/10/jpf-workshop-2013.pdf
[6]: http://www.eclemma.org/jacoco/
[7]: http://junit.org/
[8]: http://babelfish.arc.nasa.gov/trac/jpf/wiki
[9]: http://www.emulab.net/
[10]: http://www.flux.utah.edu/
