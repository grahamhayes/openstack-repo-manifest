#! /usr/bin/env python
#
# Copyright (c) 2018 Verizon Wireless
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
import xml.etree.ElementTree as ET
import requests
import os_service_types
import os

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def main():
    projects = yaml.load(open('../../openstack-infra/project-config/gerrit/projects.yaml'))
    governance = yaml.load(open('../../openstack/governance/reference/projects.yaml'))
    service_types = os_service_types.ServiceTypes()
    tags = dict()
    full_group_list = set()

    manifest = ET.Element('manifest')
    github_remote = ET.SubElement(manifest, 'remote')
    github_remote.set('name', 'github')
    github_remote.set('fetch', 'ssh://git@github.com/')
    github_remote.set('review', 'https://review.openstack.org')
    git_o_o_remote = ET.SubElement(manifest, 'remote')
    git_o_o_remote.set('name', 'openstack')
    git_o_o_remote.set('fetch', 'https://git.openstack.org/')
    git_o_o_remote.set('review', 'https://review.openstack.org/')
    default = ET.SubElement(manifest, 'default')
    default.set('revision', 'master')
    default.set('remote', 'openstack')

    for project in governance:
        types = service_types.get_all_service_data_for_project(project)
        for deliverable in governance[project]['deliverables']:
            for repo in governance[project]['deliverables'][deliverable]['repos']:
                tags[repo] = [project.replace(' ', '-').lower(), 'offical']
                if types:
                    for i in types:
                        tags[repo].append(i['service_type'])
                if 'tags' in governance[project]['deliverables'][deliverable]:
                    for tag in governance[project]['deliverables'][deliverable]['tags']:
                        tags[repo].append(tag)


    for project in projects:
        groups = []
        if project['project'].split('/')[0] not in ["openstack-attic", "stackforge"]:
            project_fragment = ET.SubElement(manifest, 'project')
            project_fragment.set("path", project['project'])
            project_fragment.set("name", "%s.git" % project['project'])

            groups = groups + tags.get(project['project'], [])
            project_fragment.set("groups", "%s" % ','.join(groups))
            [full_group_list.add(item) for item in groups]

    try:
        os.remove("groups.rst")
    except OSError:
        pass

    with open("groups.rst", "a") as groups_file:
        for group in full_group_list:
            groups_file.write("* %s \n" % group)



    with open("default.xml", "wb") as manifest_file:
        indent(manifest)
        tree = ET.ElementTree(manifest)
        tree.write(manifest_file, xml_declaration=True,
            encoding='utf-8', method="xml")

if __name__ == '__main__':
    main()
