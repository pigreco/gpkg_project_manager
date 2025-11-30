#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proper Qt .qm file compiler
Based on Qt's QM file format specification
"""
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from io import BytesIO


class QMWriter:
    """Write Qt .qm files in the correct binary format."""

    # Magic number for .qm files
    QM_MAGIC = bytes([0x3c, 0xb8, 0x64, 0x18, 0xca, 0xef, 0x9c, 0x95])

    # Section tags
    TAG_END = 0x01
    TAG_SOURCE_TEXT = 0x02
    TAG_TRANSLATION = 0x03
    TAG_CONTEXT = 0x04
    TAG_HASH = 0x05
    TAG_SOURCE_TEXT_UTF8 = 0x06
    TAG_CONTEXT_UTF8 = 0x07
    TAG_COMMENT_UTF8 = 0x08
    TAG_DEPENDENCIES = 0x09

    def __init__(self):
        self.data = BytesIO()

    def write_byte(self, value):
        """Write a single byte."""
        self.data.write(struct.pack('B', value))

    def write_uint32(self, value):
        """Write a 32-bit unsigned integer (big-endian)."""
        self.data.write(struct.pack('>I', value))

    def write_string(self, text):
        """Write a UTF-8 string with length prefix."""
        if text:
            encoded = text.encode('utf-8')
            self.write_uint32(len(encoded))
            self.data.write(encoded)
        else:
            self.write_uint32(0)

    def write_tag_string(self, tag, text):
        """Write a tag followed by a string."""
        self.write_byte(tag)
        self.write_string(text)

    def compile(self, messages):
        """Compile messages to QM format."""
        # Write magic number
        self.data.write(self.QM_MAGIC)

        # Group by context
        contexts = {}
        for msg in messages:
            ctx = msg.get('context', '')
            if ctx not in contexts:
                contexts[ctx] = []
            contexts[ctx].append(msg)

        # Write each context with its messages
        for context_name, msgs in sorted(contexts.items()):
            # Write context
            self.write_tag_string(self.TAG_CONTEXT_UTF8, context_name)

            for msg in msgs:
                source = msg.get('source', '')
                translation = msg.get('translation', '')
                comment = msg.get('comment', '')

                # Write source text
                if source:
                    self.write_tag_string(self.TAG_SOURCE_TEXT_UTF8, source)

                # Write translation
                if translation:
                    self.write_tag_string(self.TAG_TRANSLATION, translation)

                # Write comment if present
                if comment:
                    self.write_tag_string(self.TAG_COMMENT_UTF8, comment)

        # Write end tag
        self.write_byte(self.TAG_END)

        return self.data.getvalue()


def parse_ts_file(ts_path):
    """Parse .ts file and extract messages."""
    tree = ET.parse(ts_path)
    root = tree.getroot()
    messages = []

    for context_elem in root.findall('context'):
        context_name = context_elem.find('name')
        context_name = context_name.text if context_name is not None else ''

        for message_elem in context_elem.findall('message'):
            source_elem = message_elem.find('source')
            translation_elem = message_elem.find('translation')
            comment_elem = message_elem.find('comment')

            source = source_elem.text if source_elem is not None else ''
            translation = translation_elem.text if translation_elem is not None else ''
            comment = comment_elem.text if comment_elem is not None else ''

            # Skip obsolete or unfinished translations
            if translation_elem is not None:
                trans_type = translation_elem.get('type', '')
                if trans_type in ('obsolete', 'unfinished'):
                    continue

            # Only include if we have a translation
            if translation:
                messages.append({
                    'context': context_name,
                    'source': source,
                    'translation': translation,
                    'comment': comment
                })

    return messages


def compile_ts_to_qm(ts_path, qm_path):
    """Compile a .ts file to .qm format."""
    messages = parse_ts_file(ts_path)

    if not messages:
        print(f"⚠️  No translations found in {ts_path.name}")
        return False

    writer = QMWriter()
    qm_data = writer.compile(messages)

    with open(qm_path, 'wb') as f:
        f.write(qm_data)

    print(f"✓ Compiled {ts_path.name} -> {qm_path.name}")
    print(f"  Messages: {len(messages)}")
    print(f"  Size: {len(qm_data)} bytes")

    return True


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    i18n_dir = script_dir.parent / 'i18n'

    print("=" * 50)
    print("Qt .qm Compiler v2")
    print("=" * 50)
    print()

    for ts_file in sorted(i18n_dir.glob('*.ts')):
        qm_file = ts_file.with_suffix('.qm')
        print(f"Compiling {ts_file.name}...")
        try:
            compile_ts_to_qm(ts_file, qm_file)
            print()
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()
