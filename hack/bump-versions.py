#!/usr/bin/python

import xml.etree.ElementTree as et
import argparse
import re

POM_NS = "http://maven.apache.org/POM/4.0.0"
DEFAULT_ENCONDING = "UTF-8"

parser = argparse.ArgumentParser(description="Bootstrap JBPM Version Bumper")
parser.add_argument('--product', action="store",
                    type=str, help="Product JAR version")
parser.add_argument('--enterprise', action="store",
                    type=str, help="Enterprise Product version")
parser.add_argument('--community', action="store", type=str,
                    help="Community JAR version", required=True)


def update_poms(poms):
    for pom in poms:
        # parse the file
        tree = et.parse(pom)

        # updates pom
        process_pom(tree)

        # writes back
        new_tree = et.ElementTree(tree.getroot())
        new_tree.write(pom, xml_declaration=True,
                       default_namespace=POM_NS, encoding=DEFAULT_ENCONDING)


def process_pom(pom_xml):
    for prop in pom_xml.findall(".//{%s}properties/" % POM_NS):
        if prop.tag == "{%s}kie.version" % POM_NS:
            prop.text = args.community


def update_java_files(files):
    for file in files:
        with open(file, "rt") as file_handler:
            data = file_handler.read()
            data = re.sub(r'DEFAULT_VERSION = \".+"',
                          "DEFAULT_VERSION = \"%s\"" % args.community, data)

        with open(file, "wt") as file_handler:
            file_handler.write(data)


def update_project_map(file):
    if not is_update_product():
        return

    with open(file, "rt") as file_handler:
        data = file_handler.read()
        item = "        this.mappedVersions.put(\"Enterprise %s\", \"%s\");\n" % (args.enterprise, args.product)
        data = append_to_list(data, r'\s{8}this\.mappedVersions\.put.*\n', item, r'\s{4}public Project\(\) {\s',  "    public Project() {\n%s")

    with open(file, "wt") as file_handler:
        file_handler.write(data)


def update_html(file):
    with open(file, "rt") as file_handler:
        data = file_handler.read()
        # enterprise
        if is_update_product():
            item = "                                <option value=\"%s\">Enterprise %s</option>" % (args.product, args.enterprise)
            data = append_to_list(
                data,
                r'\s*<option value=.*>Enterprise .*</option>\n', item,
                r'<option .*>Enterprise</option>', "<option value=\"\" disabled>Enterprise</option>%s\n")
        # community
        item = "                                <option value=\"%s\">%s</option>" % (args.community, args.community)
        data = append_to_list(data, 
        r'\s*<option value=.*>[^Eterprs]*.</option>\n', item,
        r'<option .*>Community</option>', "<option value=\"\" disabled>Community</option>%s\n")

        data = re.sub(r'\$\(\'\#kieVersion\'\)\.val\(.*', "$('#kieVersion').val('%s');" % args.community, data)


    with open(file, "wt") as file_handler:
        file_handler.write(data)


def append_to_list(data, item_pattern, item, reference_pattern, reference_fmt):
    items = re.findall(item_pattern, data)
    items.append(item)
    data = re.sub(item_pattern, "", data)
    data = re.sub(reference_pattern, reference_fmt % "".join(items), data)
    return data

def is_update_product():
    if args.enterprise == None and args.product == None:
        print("Skipping Enterprise/Product bump")
        return False
    else:
        return True


args = parser.parse_args()

# all files that need to be updated are in here. the bump logic is in the functions.

update_poms(['jbpm-bootstrap-kjar/pom.xml', 'jbpm-bootstrap-service/pom.xml'])
update_java_files(
    ['jbpm-bootstrap-service/src/main/java/org/jbpm/bootstrap/service/util/BuildComponent.java'])
update_project_map(
    'jbpm-bootstrap-model/src/main/java/org/jbpm/bootstrap/model/Project.java')
update_html('jbpm-bootstrap-service/src/main/resources/templates/index.html')
