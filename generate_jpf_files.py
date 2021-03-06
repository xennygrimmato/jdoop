#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Marko Dimjašević
#
# This file is part of JDoop.
#
# JDoop is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# JDoop is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JDoop.  If not, see <http://www.gnu.org/licenses/>.


import re, os

class GenerateConfFile:

    def __init__(self, packagename, classpath):

        self.class_name = None
        self.package_name = packagename
        self.classpath = classpath

    def generate_jpf_conf_file(self, input_file_name, output_file_name):

        method_counter = 1
        output_file = open(output_file_name, 'w')

        output_file.write("# This is an automatically generated configuration file\n\n")

        with open(input_file_name, 'r') as f:
            for line_nl in f:
                # Remove the newline character
                line = line_nl[:-1]

                # If this is not a class definition line nor a method
                # definition line, move on to the next line
                if not re.search("public class", line) and not re.search("public void", line):
                    continue

                if re.search("public class", line):
                    # Extract the class name
                    class_name = line.lstrip().split(" ")[2]
                    output_file.write("target=" + self.package_name + "." + class_name + "\n\n")
                    top_level_class = False
                    continue

                # Since we got to this point, this is a method definition line

                # Extract the method name
                method_name = line.lstrip().split(" ")[2][:-2]
                output_file.write("concolic.method=%s\n" % method_name)
                output_file.write("concolic.method.%s=%s.%s.%s()\n" % (method_name, self.package_name, class_name, method_name))
                method_counter += 1

            output_file.write("\n")
            output_file.write("concolic.values_file=%s\n" % "concrete-values-jdart.txt")
            output_file.write("\n")
            output_file.write("classpath+=,%s\n" % self.classpath)
            output_file.write("\n")
            output_file.write("shell=gov.nasa.jpf.jdart.JDart\n")
            output_file.write("symbolic.dp=NativeZ3\n")
            output_file.write("jdart.configs.all_fields_symbolic.symbolic.include=this.*\n")
            output_file.write("\n")

            # possible log levels: servere, warning, info, config, fine,
            # finer, finest
            output_file.write("log.config=jdart\n")
            output_file.write("log.config=constraints\n")

        output_file.close()

class CoordinateConfFileGeneration:
    def __init__(self, packagename, classes_to_analyze, classpath):
        self.packagename = packagename
        self.classes_to_analyze = classes_to_analyze
        self.classpath = classpath
        self.location = packagename.replace(".", os.sep)

    def run(self):
        with open(os.path.normpath(os.path.join(self.location, self.classes_to_analyze)), 'r') as f:
            for line_nl in f:
                class_name = line_nl[:-1]

                whole_path = os.path.join(self.location, class_name + ".java")

                # g = GenerateConfFile('randooped', self.classpath)
                g = GenerateConfFile(self.packagename, self.classpath)
                g.generate_jpf_conf_file(whole_path, os.path.join(self.location, class_name + ".jpf"))
