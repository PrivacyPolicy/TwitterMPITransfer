#include <Python.h>
#include "tweet_struct.h"

#define PYFILENAME "python_scrape"    // python file being called
#define PYFUNCNAME "scrape"           // python function being called

#define ID_LENGTH 18
#define DELIM ";"

struct Tweet* getTweets(char* term, long int min, long int max, int* count)
{
    PyObject *pName, *pModule, *pDict, *pFunc, *pArgs, *pValue, *pListItem, *pString;
    
    // start python interpreter
    Py_Initialize();
    
    // import python libraries
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(\".\")");
    //PyRun_SimpleString("");
    
    // load python file
    pName = PyString_FromString(PYFILENAME);
    if (pName == NULL) return NULL;
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    
    if (pModule == NULL) {
        PyErr_Print();
        fprintf(stderr, "Could not load file \"%s\".\n", PYFILENAME);
        return NULL;
    }
    
    // get a reference to the python function
    pFunc = PyObject_GetAttrString(pModule, PYFUNCNAME);
    if (!pFunc || !PyCallable_Check(pFunc)) {
        if (PyErr_Occurred()) PyErr_Print();
        fprintf(stderr, "Cannot find function %s.\n", PYFUNCNAME);
        return NULL;
    }
    
    // prepare arguments for python call (actually kind of a pain)
    pArgs = PyTuple_New(3);
    pValue = PyString_FromString(term);
    if (!pValue) {
        Py_DECREF(pArgs);
        Py_DECREF(pModule);
        fprintf(stderr, "Cannot convert argument term.\n");
        return NULL;
    }
    PyTuple_SetItem(pArgs, 0, pValue);
    
    pValue = PyLong_FromLong(min);
    if (!pValue) {
        Py_DECREF(pArgs);
        Py_DECREF(pModule);
        fprintf(stderr, "Cannot convert argument min.\n");
        return NULL;
    }
    PyTuple_SetItem(pArgs, 1, pValue);
    
    pValue = PyLong_FromLong(max);
    if (!pValue) {
        Py_DECREF(pArgs);
        Py_DECREF(pModule);
        fprintf(stderr, "Cannot convert argument max.\n");
        return NULL;
    }
    PyTuple_SetItem(pArgs, 2, pValue);
    
    // moment of truth! make python call
    pValue = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);
    if (pValue == NULL || !PyList_Check(pValue)) {
        Py_DECREF(pFunc);
        Py_DECREF(pModule);
        PyErr_Print();
        fprintf(stderr, "Call failed.\n");
        return NULL;
    }
    
    int tweetCount = PyList_Size(pValue);
    struct Tweet* tweets = malloc(sizeof(struct Tweet) * tweetCount);
    int j;
    for (j = 0; j < tweetCount; j++) {
        char* str = PyString_AsString(PyList_GetItem(pValue, j));
        // printf("Raw data: %s.\n", str);
        // id;sentiment;retweets;favorites;username;text
        tweets[j].id = atol(strsep(&str, DELIM));
        tweets[j].sentiment = atof(strsep(&str, DELIM));
        tweets[j].retweets = atol(strsep(&str, DELIM));
        tweets[j].favorites = atol(strsep(&str, DELIM));
        tweets[j].user = strsep(&str, DELIM);
        tweets[j].text = strsep(&str, DELIM);
    }
    
    *count = tweetCount;
    
    Py_Finalize();
    return tweets;
}

int main(int argc, char* argv) {
    printf("Downloading Tweets...\n");
    int count;
    struct Tweet* tweets = getTweets("donald trump", 0*600000000000000000, 0*890000000000000000, &count);
    int i;
    for (i = 0; i < count; i++) {
        struct Tweet tweet = tweets[i];
        char* text = tweet.text;
        char* user = tweet.user;
        printf("Tweet number %d: %s, %s, %ld, %ld, %f, %ld.\n", i, text, user, tweet.retweets, tweet.favorites, tweet.sentiment, tweet.id);
    }
}




