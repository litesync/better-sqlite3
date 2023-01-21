# ===
# This is the main GYP file, which builds better-sqlite3 with SQLite3 itself.
# ===

{
  'includes': ['deps/common.gypi'],
  'targets': [
    {
      'target_name': 'better_sqlite3',
      'sources': ['src/better_sqlite3.cpp'],
      'cflags_cc': ['-std=c++17'],
      'xcode_settings': {
        'OTHER_CPLUSPLUSFLAGS': ['-std=c++17', '-stdlib=libc++'],
      },
      'msvs_settings': {
        'VCCLCompilerTool': {
          'AdditionalOptions': [
            '/std:c++17',
          ],
        },
      },
      'conditions': [
        ['OS=="linux"', {
          'ldflags': [
            '-Wl,-Bsymbolic',
            '-Wl,--exclude-libs,ALL',
          ],
        }],
      ],
      # link to pre-built sqlite3 library
      'include_dirs': ['<(sqlite3_include_dir)'],
      'libraries': ['-l<(sqlite3_lib_name)'],
      'conditions': [ [ 'OS=="linux"', {'libraries+':['-Wl,-rpath=<@(sqlite3_lib_path)']} ] ],
      'conditions': [ [ 'OS!="win"', {'libraries+':['-L<@(sqlite3_lib_path)']} ] ],
      'msvs_settings': {
        'VCLinkerTool': {
          'AdditionalLibraryDirectories': [
            '<(sqlite3_lib_path)'
          ],
        },
      },
    },
    {
      'target_name': 'test_extension',
      # link to pre-built sqlite3 library
      'include_dirs': ['<(sqlite3_include_dir)'],
      'libraries': ['-l<(sqlite3_lib_name)'],
      'conditions': [ [ 'OS=="linux"', {'libraries+':['-Wl,-rpath=<@(sqlite3_lib_path)']} ] ],
      'conditions': [ [ 'OS!="win"', {'libraries+':['-L<@(sqlite3_lib_path)']} ] ],
      'msvs_settings': {
        'VCLinkerTool': {
          'AdditionalLibraryDirectories': [
            '<(sqlite3_lib_path)'
          ],
        },
      },
      'sources': ['deps/test_extension.c']
    },
  ],
}
