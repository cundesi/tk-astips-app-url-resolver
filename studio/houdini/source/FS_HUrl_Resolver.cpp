/*

Author  :   astips

Github  :   https://github.com/astips

*/


#include <PY/PY_CPythonAPI.h>
#include <UT/UT_DSOVersion.h>
#include <OP/OP_Director.h>
#include <PY/PY_InterpreterAutoLock.h>
#include <FS/FS_Utils.h>

#include "FS_HUrl_Resolver.h"


#define PY_MODULE_NAME "hurl_resolver"
#define HURL_IS_VALID_METHOD "hurl_checker"
#define HURL_REAL_PATH_METHOD "hurl_helper"


UT_StringArray HurlResolver::sourceCache = UT_StringArray();
UT_StringArray HurlResolver::realPathCache = UT_StringArray();

UT_String HurlResolver::realPath( const UT_String source )
{
    UT_String realPath;

    fpreal index = sourceCache.find( source );
    if( index < 0 ) index = cachePath( source );
    realPath = realPathCache( index );
    return realPath;
}


bool HurlResolver::isValid( const UT_String source )
{
    return realPath( source ).isstring();
}

fpreal HurlResolver::cachePath( const UT_String source )
{
    UT_String realPath;
    fpreal sourceIndex, realPathIndex;

    pyConvertExecution( source, realPath );

    sourceIndex = sourceCache.append( source );
    realPathIndex = realPathCache.append( realPath );

    if( sourceIndex == realPathIndex )
        return realPathIndex;
    else
    {
        sourceCache.clear();
        realPathCache.clear();
        return cachePath( source );
    }
}


bool HurlResolver::pyConvertExecution( UT_String source, UT_String &realPath )
{
    // Stop calling Python if it haven't initialized.
    static bool has_loaded_python_library = false;
    if( has_loaded_python_library || OPgetDirector() ) has_loaded_python_library = true;
    if( !has_loaded_python_library ) return false;

    // Simply return false if source is invalid.
    if( !source.isstring() ) return false;

    // Ask for a GIL before execute Py functions.
    PY_InterpreterAutoLock interpreter_auto_lock;

    // Declare local variables.
    fpreal isValid;
    PY_PyObject *pModule, *pDict, *pFunc, *pArgs, *pValue;

    // Initialize the python module and its dictionary.
    pModule = PY_PyImport_ImportModule( PY_MODULE_NAME );
    pDict = PY_PyModule_GetDict( pModule );

    pArgs = PY_PyTuple_New( 1 );
    PY_PyTuple_SetItem( pArgs, 0, PY_PyString_FromString( source ) );

    pFunc = PY_PyDict_GetItemString( pDict, HURL_IS_VALID_METHOD );

    if( PY_PyCallable_Check( pFunc ) )
        pValue = PY_PyObject_CallObject( pFunc, pArgs );
    else
        return false;

    if( pValue != NULL )
        isValid = PY_PyInt_AsLong( pValue );
    else
        return false;

    // Convert URL to real path if it's valid.
    if( isValid )
    {
        pFunc = PY_PyDict_GetItemString( pDict, HURL_REAL_PATH_METHOD );

        if( PY_PyCallable_Check(pFunc) )
            pValue = PY_PyObject_CallObject( pFunc, pArgs );
        else
            return false;

        if( pValue != NULL )
            realPath = PY_PyString_AsString( pValue );
        else
            return false;
    }

    return isValid;
}


bool FS_HurlInfoHelper::canHandle( const char *source )
{
    return HurlResolver::isValid( source );
}


bool FS_HurlInfoHelper::hasAccess( const char *source, int mode )
{
    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        FS_Info info( realPath );
        return info.hasAccess( mode );
    }

    return false;
}


bool FS_HurlInfoHelper::getIsDirectory( const char *source )
{
    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        FS_Info info( realPath );
        return info.getIsDirectory();
    }

    return false;
}


int FS_HurlInfoHelper::getModTime( const char *source )
{
    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        FS_Info info( realPath );
        return info.getModTime();
    }

    return 0;
}


int64 FS_HurlInfoHelper::getSize( const char *source )
{
    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        FS_Info info( realPath );
        return info.getFileDataSize();
    }

    return 0;
}


UT_String FS_HurlInfoHelper::getExtension( const char *source )
{
    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        return FS_InfoHelper::getExtension( realPath );
    }

    return FS_InfoHelper::getExtension( source );
}


bool FS_HurlInfoHelper::getContents( const char *source, 
                                     UT_StringArray &contents, 
                                     UT_StringArray *dirs )
{
    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        FS_Info info( realPath );
        return info.getContents( contents, dirs );
    }

    return false;
}


FS_ReaderStream* FS_HurlReaderHelper::createStream( const char *source, const UT_Options * )
{
    FS_ReaderStream *stream = nullptr;

    if( HurlResolver::isValid( source ) )
    {
        UT_String realPath = HurlResolver::realPath( source );
        stream = new FS_ReaderStream( realPath );
    }

    return stream;
}


bool FS_HurlReaderHelper::splitIndexFileSectionPath( const char *source_section_path, 
                                                     UT_String &index_file_path, 
                                                     UT_String &section_name )
{
    if( HurlResolver::isValid( source_section_path ) )
    {
        index_file_path = source_section_path;
        return true;
    }
    else
        return false;
}


bool FS_HurlReaderHelper::combineIndexFileSectionPath( UT_String &source_section_path, 
                                                       const char *index_file_path, 
                                                       const char *section_name )
{
    return HurlResolver::isValid( source_section_path );
}


void installFSHelpers()
{
    new FS_HurlInfoHelper();
    new FS_HurlReaderHelper();
}
