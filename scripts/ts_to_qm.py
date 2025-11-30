#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal .ts to .qm compiler
Based on Qt's QM file format specification
"""
import struct
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path

class QMCompiler:
    """Compile .ts files to .qm format."""

    # QM file format constants
    QM_MAGIC = 0x3CB86418

    # Section tags
    Tag_End = 1
    Tag_SourceText16 = 2
    Tag_Translation = 3
    Tag_Context16 = 4
    Tag_Obsolete1 = 5
    Tag_SourceText = 6
    Tag_Context = 7
    Tag_Comment = 8
    Tag_Obsolete2 = 9

    def __init__(self):
        self.messages = []

    def add_message(self, context, source, translation, comment=''):
        """Add a message to compile."""
        self.messages.append({
            'context': context,
            'source': source,
            'translation': translation,
            'comment': comment
        })

    def parse_ts(self, ts_file):
        """Parse a .ts file and extract messages."""
        tree = ET.parse(ts_file)
        root = tree.getroot()

        for context_elem in root.findall('context'):
            context_name = context_elem.find('name')
            context_name = context_name.text if context_name is not None else ''

            for message_elem in context_elem.findall('message'):
                source_elem = message_elem.find('source')
                translation_elem = message_elem.find('translation')
                comment_elem = message_elem.find('comment')

                source = source_elem.text if source_elem is not None and source_elem.text else ''
                translation = translation_elem.text if translation_elem is not None and translation_elem.text else ''
                comment = comment_elem.text if comment_elem is not None and comment_elem.text else ''

                # Skip empty translations
                if translation:
                    self.add_message(context_name, source, translation, comment)

    def write_string(self, data, text):
        """Write a length-prefixed UTF-8 string."""
        text_bytes = text.encode('utf-8')
        data.append(struct.pack('>I', len(text_bytes)))
        data.append(text_bytes)

    def write_tag(self, data, tag, value=''):
        """Write a tag with optional value."""
        data.append(struct.pack('B', tag))
        if value:
            value_bytes = value.encode('utf-8')
            data.append(struct.pack('>I', len(value_bytes)))
            data.append(value_bytes)

    def compile_to_qm(self, output_file):
        """Compile messages to .qm format."""
        data = []

        # Write magic number
        data.append(struct.pack('>I', self.QM_MAGIC))

        # Group messages by context
        contexts = {}
        for msg in self.messages:
            ctx = msg['context']
            if ctx not in contexts:
                contexts[ctx] = []
            contexts[ctx].append(msg)

        # Write each context
        for context, messages in contexts.items():
            # Write context tag
            self.write_tag(data, self.Tag_Context, context)

            for msg in messages:
                # Write source text
                self.write_tag(data, self.Tag_SourceText, msg['source'])

                # Write translation
                self.write_tag(data, self.Tag_Translation, msg['translation'])

                # Write comment if present
                if msg['comment']:
                    self.write_tag(data, self.Tag_Comment, msg['comment'])

        # Write end tag
        data.append(struct.pack('B', self.Tag_End))

        # Write to file
        with open(output_file, 'wb') as f:
            for chunk in data:
                f.write(chunk)

        return True


def compile_ts_file(ts_path, qm_path):
    """Compile a .ts file to .qm."""
    compiler = QMCompiler()
    compiler.parse_ts(ts_path)
    compiler.compile_to_qm(qm_path)
    print(f"✓ Compiled {ts_path.name} -> {qm_path.name}")
    print(f"  Messages: {len(compiler.messages)}")
    print(f"  Size: {qm_path.stat().st_size} bytes")


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    i18n_dir = script_dir.parent / 'i18n'

    # Compile all .ts files
    for ts_file in i18n_dir.glob('*.ts'):
        qm_file = ts_file.with_suffix('.qm')
        print(f"\nCompiling {ts_file.name}...")
        try:
            compile_ts_file(ts_file, qm_file)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
