#include "orderbook.h"


static void Orderbook_dealloc(Orderbook *self)
{
    Py_XDECREF(self->bids);
    Py_XDECREF(self->asks);
    Py_TYPE(self)->tp_free((PyObject *) self);
}


static PyObject *Orderbook_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Orderbook *self;
    self = (Orderbook *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->bids = PyDict_New();
        if (!self->bids) {
            Py_DECREF(self);
            return NULL;
        }

        self->asks = PyDict_New();
        if (!self->asks) {
            Py_DECREF(self->bids);
            Py_DECREF(self);
            return NULL;
        }

        self->max_depth = 0;

    }
    return (PyObject *) self;
}


static int Orderbook_init(Orderbook *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"max_depth", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, &self->max_depth)) {
        return -1;
    }

    return 0;
}


static PyMemberDef Orderbook_members[] = {
    {"bids", T_OBJECT_EX, offsetof(Orderbook, bids), 0, "bids"},
    {"asks", T_OBJECT_EX, offsetof(Orderbook, asks), 0, "asks"},
    {"max_depth", T_INT, offsetof(Orderbook, max_depth), 0, "Maximum book depth"},
    {NULL}
};


static PyObject* Orderbook_placeholder(Orderbook *self, PyObject *Py_UNUSED(ignored))
{
    return PyUnicode_FromString("Hello!");
}


static PyMethodDef Orderbook_methods[] = {
    {"placeholder", (PyCFunction) Orderbook_placeholder, METH_NOARGS,
     "Placeholder"
    },
    {NULL}
};


static PyTypeObject OrderbookType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "orderbook.orderbook",
    .tp_doc = "An Orderbook data structure",
    .tp_basicsize = sizeof(Orderbook),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Orderbook_new,
    .tp_init = (initproc) Orderbook_init,
    .tp_dealloc = (destructor) Orderbook_dealloc,
    .tp_members = Orderbook_members,
    .tp_methods = Orderbook_methods,
};

/* Sorted Dictionary */
static void SortedDict_dealloc(SortedDict *self)
{
    Py_XDECREF(self->data);
    if (self->keys && self->iterator_index != -1) {
        Py_DECREF(self->keys);
    }
    Py_TYPE(self)->tp_free((PyObject *) self);
}


static PyObject *SortedDict_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    SortedDict *self;
    self = (SortedDict *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->data = PyDict_New();
        if (!self->data) {
            Py_DECREF(self);
            return NULL;
        }
        // 0 means it hasnt been set
        self->ordering = 0;
        // -1 means uninitalized
        self->iterator_index = -1;
        self->keys = NULL;
        self->dirty = false;
    }
    return (PyObject *) self;
}


static int SortedDict_init(SortedDict *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"ordering", NULL};
    char *ordering = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|z", kwlist, &ordering)) {
        return -1;
    }

    if (ordering) {
        if (strcmp(ordering, "DESC") == 0) {
            self->ordering = -1;
        } else if (strcmp(ordering, "ASC") == 0) {
            self->ordering = 1;
        } else {
            PyErr_SetString(PyExc_ValueError, "ordering must be one of ASC or DESC");
            return -1;
        }
    } else {
        // default is ascending
        self->ordering = 1;
    }

    return 0;
}


static PyMemberDef SortedDict_members[] = {
    {"__data", T_OBJECT_EX, offsetof(SortedDict, data), READONLY, "internal data"},
    {"__ordering", T_INT, offsetof(SortedDict, ordering), 0, "ordering flag"},
    {NULL}
};


static PyObject* SortedDict_keys(SortedDict *self, PyObject *Py_UNUSED(ignored))
{
    if (!self->dirty && self->keys) {
        Py_INCREF(self->keys);
        return self->keys;
    }

    PyObject *keys = PyDict_Keys(self->data);
    if (!keys) {
        return NULL;
    }

    if (PyList_Sort(keys) < 0) {
        return NULL;
    }

    if (self->ordering == -1) {
        if (PyList_Reverse(keys) < 0) {
            return NULL;
        }
    }

    if (self->keys) {
        Py_DECREF(self->keys);
    }

    Py_INCREF(keys);
    self->keys = keys;
    self->dirty = false;
    return keys;
}


static PyObject* SortedDict_index(SortedDict *self, PyObject *index)
{
    long i = PyLong_AsLong(index);
    if (PyErr_Occurred()) {
        return NULL;
    }



}

static PyMethodDef SortedDict_methods[] = {
    {"keys", (PyCFunction) SortedDict_keys, METH_NOARGS, "return a list of keys in the sorted dictionary"},
    {"index", (PyCFunction) SortedDict_index, METH_O, "Return a key, value tuple at index N"},
    {NULL}
};

/* Sorted Dictionary Mapping Functions */
Py_ssize_t SortedDict_len(SortedDict *self) {
	return PyDict_Size(self->data);
}

PyObject *SortedDict_getitem(SortedDict *self, PyObject *key) {
    PyObject *ret = PyDict_GetItemWithError(self->data, key);
    if (ret) {
        Py_INCREF(ret);
        return ret;
    }

    if (!PyErr_Occurred()) {
        PyErr_SetString(PyExc_KeyError, "key does not exist");
    }

    return ret;
}

int SortedDict_setitem(SortedDict *self, PyObject *key, PyObject *value) {
    self->dirty = true;

    if (value) {
        return PyDict_SetItem(self->data, key, value);
    } else {
        // setitem also called to for del (value will be null for deletes)
        return PyDict_DelItem(self->data, key);
    }
}

/* iterator methods */
PyObject *SortedDict_next(SortedDict *self) {
    if (self->iterator_index == -1) {
        self->iterator_index = 0;
        SortedDict_keys(self, NULL);

        Py_ssize_t size = PyList_Size(self->keys);
        if (size == 0){
            Py_DECREF(self->keys);
            return NULL;
        }
        return PyList_GetItem(self->keys, self->iterator_index);
    } else {
        self->iterator_index++;
        Py_ssize_t size = PyList_Size(self->keys);
        if (size == self->iterator_index) {
            self->iterator_index = -1;
            Py_DECREF(self->keys);
            return NULL;
        }
        return PyList_GetItem(self->keys, self->iterator_index);
    }
}


/* Sorted Dictionary Type Setup */
static PyMappingMethods SortedDict_mapping = {
	(lenfunc)SortedDict_len,
	(binaryfunc)SortedDict_getitem,
	(objobjargproc)SortedDict_setitem
};


static PyTypeObject SortedDictType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "sorteddict.sorteddict",
    .tp_doc = "An SortedDict data structure",
    .tp_basicsize = sizeof(SortedDict),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = SortedDict_new,
    .tp_init = (initproc) SortedDict_init,
    .tp_dealloc = (destructor) SortedDict_dealloc,
    .tp_members = SortedDict_members,
    .tp_methods = SortedDict_methods,
    .tp_as_mapping = &SortedDict_mapping,
    .tp_iter  = PyObject_SelfIter,
    .tp_iternext = (iternextfunc) SortedDict_next,
};


/* Module specific definitions and initilization */
static PyModuleDef orderbookmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "Orderbook",
    .m_doc = "Orderbook data structure",
    .m_size = -1,
};


PyMODINIT_FUNC PyInit_orderbook(void)
{
    PyObject *m;
    if (PyType_Ready(&OrderbookType) < 0 || PyType_Ready(&SortedDictType) < 0)
        return NULL;

    m = PyModule_Create(&orderbookmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&OrderbookType);
    if (PyModule_AddObject(m, "OrderBook", (PyObject *) &OrderbookType) < 0) {
        Py_DECREF(&OrderbookType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&SortedDictType);
    if (PyModule_AddObject(m, "SortedDict", (PyObject *) &SortedDictType) < 0) {
        Py_DECREF(&SortedDictType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}