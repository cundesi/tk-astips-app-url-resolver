/*

Author  :   astips

Github  :   https://github.com/astips

*/


#ifndef __FS_Helper_Converter__
#define __FS_Helper_Converter__


#include <UT/UT_StringArray.h>
#include <UT/UT_String.h>
#include <FS/FS_Info.h>
#include <FS/FS_Reader.h>


class HurlResolver
{
public:
    HurlResolver();
    ~HurlResolver();

    static UT_String realPath( const UT_String source );
    static bool isValid( const UT_String source );
    static fpreal cachePath( const UT_String source );
    static bool pyConvertExecution( const UT_String source, UT_String &realPath );

    static UT_StringArray sourceCache, realPathCache;
};


class FS_HurlInfoHelper : public FS_InfoHelper
{
public:
    FS_HurlInfoHelper() {};
    ~FS_HurlInfoHelper() {};

    virtual bool canHandle( const char *source );
    virtual bool hasAccess( const char *source, int mode );
    virtual bool getIsDirectory( const char *source );
    virtual int getModTime( const char *source );
    virtual int64 getSize( const char *source );
    virtual UT_String getExtension( const char *source );
    virtual bool getContents( const char *source, UT_StringArray &contents, UT_StringArray *dirs );
};


class FS_HurlReaderHelper : public FS_ReaderHelper
{
public:
    FS_HurlReaderHelper() {};
    ~FS_HurlReaderHelper() {};

    virtual FS_ReaderStream *createStream( const char *source, const UT_Options *options );
    virtual bool splitIndexFileSectionPath( const char *source_section_path, UT_String &index_file_path, UT_String &section_name );
    virtual bool combineIndexFileSectionPath( UT_String &source_section_path, const char *index_file_path, const char *section_name );
};

#endif
