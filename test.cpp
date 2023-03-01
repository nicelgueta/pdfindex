#include <Python.h>

int main() {
    Py_Initialize();
    PyRun_SimpleString("import script");
    PyObject* module = PyImport_ImportModule("script");
    PyObject* function = PyObject_GetAttrString(module, "main");
    PyObject* result = PyObject_CallObject(function, NULL);
    Py_Finalize();
    return 0;
}