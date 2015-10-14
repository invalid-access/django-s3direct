import os
import json
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings


class S3DirectWidget(widgets.TextInput):
    html = (
        '<div class="s3direct" data-policy-url="{policy_url}">'
        '  <a class="file-link" target="_blank" href="{file_url}">{file_src_filename}</a>'
        '  <a class="file-remove" href="#remove">Remove</a>'
        '  <input class="file-url" type="hidden" value="{file_url}" id="{file_url_element_id}" name="{file_url_name}" />'
        '  <input class="file-src-filename" type="hidden" value="{file_src_filename}" id="{file_src_filename_element_id}" name="{file_src_filename_name}" />'
        '  <input class="file-dest" type="hidden" value="{dest}">'
        '  <input class="file-input" type="file" />'
        '  <div class="progress progress-striped active">'
        '    <div class="bar"></div>'
        '  </div>'
        '</div>'
    )

    src_filename_suffix = '-src-filename'

    class Media:
        js = (
            's3direct/js/scripts.js',
        )
        css = {
            'all': (
                's3direct/css/bootstrap-progress.min.css',
                's3direct/css/styles.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.dest = kwargs.pop('dest', None)
        super(S3DirectWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value:
            value_dict = json.loads(value)
            src_filename = value_dict['src_filename']
            dst_url = value_dict['dst_url']
        else:
            src_filename = ''
            dst_url = ''
        output = self.html.format(
            policy_url=reverse('s3direct'),
            file_url_element_id=self.build_attrs(attrs).get('id'),
            file_src_filename_element_id=self.build_attrs(attrs).get('id')+self.src_filename_suffix,
            file_src_filename=os.path.basename(src_filename),
            dest=self.dest,
            file_url=dst_url,
            file_url_name=name,
            file_src_filename_name=name+self.src_filename_suffix)

        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        dst_url = data[name]
        src_filename = data[name+self.src_filename_suffix]
        if dst_url != '' and src_filename != '':
            value_dict = {'src_filename': src_filename, 'dst_url': dst_url}
            value = json.dump
            return value
        return None
        #return super(S3DirectWidget, self).value_from_datadict(data, files, name)
