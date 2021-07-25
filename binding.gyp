# ===
# This is the main GYP file, which builds better-sqlite3 with SQLite3 itself.
# ===

{
  'includes': ['deps/common.gypi'],
  'targets': [
    {
      'target_name': 'better_sqlite3',
      'sources': ['src/better_sqlite3.cpp'],
      'cflags': ['-std=c++14'],
      'xcode_settings': {
        'OTHER_CPLUSPLUSFLAGS': ['-std=c++14', '-stdlib=libc++'],
      },
      # link to pre-built sqlite3 library
      'include_dirs': ['<(sqlite3_include)'],
      'libraries': ['-l<(sqlite3_libname)'],
      'conditions': [ [ 'OS=="linux"', {'libraries+':['-Wl,-rpath=<@(sqlite3_libpath)']} ] ],
      'conditions': [ [ 'OS!="win"', {'libraries+':['-L<@(sqlite3_libpath)']} ] ],
      'msvs_settings': {
        'VCLinkerTool': {
          'AdditionalLibraryDirectories': [
            '<(sqlite3_libpath)'
          ],
        },
      },
    },
    {
      'target_name': 'test_extension',
      # link to pre-built sqlite3 library
      'include_dirs': ['<(sqlite3_include)'],
      'libraries': ['-l<(sqlite3_libname)'],
      'conditions': [ [ 'OS=="linux"', {'libraries+':['-Wl,-rpath=<@(sqlite3_libpath)']} ] ],
      'conditions': [ [ 'OS!="win"', {'libraries+':['-L<@(sqlite3_libpath)']} ] ],
      'msvs_settings': {
        'VCLinkerTool': {
          'AdditionalLibraryDirectories': [
            '<(sqlite3_libpath)'
          ],
        },
      },
      'sources': ['deps/test_extension.c']
    },
  ],
}
