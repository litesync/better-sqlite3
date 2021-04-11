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
      'conditions': [
        ['sqlite3 != "internal" and sqlite3_libname != ""', {
          # link to pre-built sqlite3 library
          'include_dirs': ['<(sqlite3)'],
          'libraries': ['-l<(sqlite3_libname)'],
          'conditions': [ [ 'OS=="linux"', {'libraries+':['-Wl,-rpath=<@(sqlite3_libpath)']} ] ],
          'conditions': [ [ 'OS!="win"', {'libraries+':['-L<@(sqlite3_libpath)']} ] ],
          'msvs_settings': {
            'VCLinkerTool': {
              'AdditionalLibraryDirectories': [
                '<(sqlite3_libpath)'
              ],
            },
          }
        },{
          # build internal / custom amalgamation
          'dependencies': ['deps/sqlite3.gyp:sqlite3']
        }]
      ]
    },
    {
      'target_name': 'test_extension',
      'conditions': [
        ['sqlite3 != "internal" and sqlite3_libname != ""', {
          # link to pre-built sqlite3 library
          'include_dirs': ['<(sqlite3)'],
          'libraries': ['-l<(sqlite3_libname)'],
          'conditions': [ [ 'OS=="linux"', {'libraries+':['-Wl,-rpath=<@(sqlite3_libpath)']} ] ],
          'conditions': [ [ 'OS!="win"', {'libraries+':['-L<@(sqlite3_libpath)']} ] ],
          'msvs_settings': {
            'VCLinkerTool': {
              'AdditionalLibraryDirectories': [
                '<(sqlite3_libpath)'
              ],
            },
          }
        },{
          # build internal / custom amalgamation
          'dependencies': ['deps/sqlite3.gyp:sqlite3']
        }]
      ],
      'sources': ['deps/test_extension.c']
    },
  ],
}
