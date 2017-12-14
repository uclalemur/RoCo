"""The library package.

This package contains prebuilt components that can be loaded by roco
to create output.

"""

import os, os.path
import glob
import traceback
import logging
import os
import sqlite3 as db

from pprint import pprint

from roco.api.component import Component
from roco.utils.utils import try_import, to_camel_case



py_components = [os.path.basename(f)[:-3] for f in glob.glob(
   os.path.dirname(__file__) + "/*.py") if os.path.basename(f)[0] != "_"]
yaml_components = [os.path.basename(
   f)[:-5] for f in glob.glob(os.path.dirname(__file__) + "/*.yaml")]
all_components = list(set(py_components + yaml_components))


def get_lib_dir():
    return os.path.abspath(os.path.dirname(__file__))

def update_component_lists():
    py_components = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py") if os.path.basename(f)[0] != "_"]
    yaml_components = [os.path.basename(f)[:-5] for f in glob.glob(os.path.dirname(__file__) + "/*.yaml")]
    all_components = list(set(py_components + yaml_components))
    # print "\n\n\n\n\nUpdated Components\n", allComponents, "\n\n\n\n"
    return all_components


def instance_of(comp, composable_type):
    try:
        return composable_type in comp.composables.keys() or composable_type is "all"
    except:
        return False


# when no arguments are passed in all components are returned
def filter_components(composable_type=["all"], verbose=False):
    """
    Creates all the components in the allComponents list, looks through them for
    components which have the specified composable type, and returns a list of those
    Arguments.
        composable_type: An array of keywords corresponding to specific composable
                        types.
                         ex: "code" for "CodeComposable"
                         To view the possible strings for composable_type, call
                         filterComponents with its default parameter and look at
                         the key values of Component.composables for all the
                         Component objects in the array the function returns.
                         Default value is "all". This populates the array with
                         ComponentQueryItems of related to all composables.
    Return.
        Array of Component objects which have the specified composable type
    """
    
    comps = []
    for comp in all_components:
        try:
            a = get_component(comp, name=comp)
            for ctype in composable_type:
                code_instance = instance_of(a, ctype)
                if code_instance is True and a not in comps:
                    comps.append(a)
            if not verbose:
                print a.get_name()
        except Exception as err:
            if verbose is False:
                #print "-------------------------------------------------{}".format(comp)
                logging.error(traceback.format_exc())
    return comps


# when no arguments are passed in all components are returned
def filter_database(composable_type=["all"], verbose=False):
    """
    Looks through database for components which have the specified composable type
    Arguments.
        composable_type: The keyword corresponding to a specific composable type.
                         ex: "code" for "CodeComposable"
                         Default value is "all". This populates the array with
                         ComponentQueryItems of related to all composables.
    Return.
        Array of ComponentQueryItems populated with all the components in the
        database which had the specified composable type
    """
    comps = []
    b = update_component_lists()

    for comp in b:
        try:
            a = query_database(comp)
            for ctype in composable_type:
                code_instance = instance_of(a, ctype)
                if code_instance is True and a not in comps:
                    comps.append(a)
        except Exception as err:
            logging.error(traceback.format_exc())

    return comps


def get_component(c, **kwargs):
    # import pdb; pdb.set_trace()
    try:
        mod = __import__(c, fromlist=[c, "library." + c], globals=globals())
        obj = getattr(mod, to_camel_case(c))()
    except AttributeError:
        try:
            obj = getattr(mod, c)()
        except AttributeError :
            obj = Component(os.path.abspath(os.path.dirname(__file__)) + "/" + c + ".yaml")
    except ImportError:
        if "baseclass" in kwargs:
            bc = try_import(kwargs["baseclass"],kwargs["baseclass"])
            obj = bc(os.path.abspath(os.path.dirname(__file__)) + "/" + c + ".yaml")
        else:
            obj = Component(os.path.abspath(os.path.dirname(__file__)) + "/" + c + ".yaml")

    for k, v in kwargs.iteritems():
        if k == 'name':
           obj.set_name(v)
        elif k == 'baseclass':
            pass
        else:
            obj.set_parameter(k, v)

    if 'name' not in kwargs:
        obj.set_name(c)

    return obj


def build_database(components, username="root", password=""):
    """
    Saves critical data about the passed in components in the database.
    Use with filterComponents()
    Arguments.
        components: An array of Component objects that will be saved to the
                    database
        username: Username for the MySQL server. Default is "root" (STRING)
        password: Password for the MySQL server. Default is empty string "" (STRING)
    Return.
        Nothing
    """
    # con = db.connect(user=username, passwd=password)

    # dbPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'compDatabase.db')
    db_path = os.path.join(os.getcwd(), 'compDatabase.db')
    con = db.connect(db_path)
    c = con.cursor()

    init_database(c)

    for comp in components:
        comp_id = 0
        c.execute('SELECT * FROM components WHERE type LIKE "{}"'.format(comp.get_name()))
        x = c.fetchall()
        if len(x) == 0:
            c.execute('INSERT INTO components VALUES (NULL, "{}")'.format(comp.get_name()))
            c.execute('SELECT LAST_INSERT_ROWID()')
            comp_id = c.fetchall()[0][0]
        else:
            comp_id = x[0][0]


        write_interfaces(comp, comp_id, c)
        write_parameters(comp, comp_id, c)
        write_composables(comp, comp_id, c)
    # c.close()
    # con.commit()

    con.commit()
    con.close()


def init_database(c):
    """
    Initalizes the database and populates it with the necessary tables.
    Arguments.
        c: cursor object of python database connection object
    Return.
        Nothing
    """
    # c.execute('CREATE DATABASE IF NOT EXISTS component_info')
    # c.execute('USE component_info')
    c.execute('CREATE TABLE IF NOT EXISTS components(id INTEGER PRIMARY KEY AUTOINCREMENT, type VARCHAR(45) NOT NULL DEFAULT "Component")')
    c.execute('CREATE TABLE IF NOT EXISTS interfaces(id INTEGER PRIMARY KEY AUTOINCREMENT, var_name VARCHAR(45) NOT NULL, port_type MEDIUMBLOB NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS params(id INTEGER PRIMARY KEY AUTOINCREMENT, var_name VARCHAR(45) NOT NULL, default_value MEDIUMBLOB NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS composables(id INTEGER PRIMARY KEY AUTOINCREMENT, var_name VARCHAR(45) NOT NULL, composable_obj MEDIUMBLOB NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS component_interface_link(component_id INTEGER NOT NULL, interface_id INTEGER NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS component_parameter_link(component_id INTEGER NOT NULL, parameter_id INTEGER NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS component_composable_link(component_id INTEGER NOT NULL, composable_id INTEGER NOT NULL)')


def write_interfaces(comp, comp_id, c, verbose=False):
    """
    Writes all the interfaces of a component to the database. If a component is
    composite, recursion is used to link the interfaces of subcomponents with
    the one passed in as an argument.
    Arguments.
        comp: Component object
        comp_id: Primary key id of the component object in the database (INTEGER)
        c: cursor object of python database connection object
    Return.
        Nothing
    """
    try:
        # delete existing component interface links and interfaces

        c.execute('SELECT * FROM component_interface_link WHERE component_id LIKE {}'.format(comp_id))
        x = c.fetchall()
        if len(x) > 0:
            c.execute('DELETE FROM component_interface_link WHERE component_id LIKE {}'.format(comp_id))
    except Exception as err:
        logging.error(traceback.format_exc())
    for k, v in comp.interfaces.iteritems():
        try:
            
            value = ""
            if isinstance(v, dict):
                composite_comp = v["subcomponent"]
                value = comp.subcomponents[composite_comp]["component"].interfaces[v["interface"]].__class__.__name__
            else:
                value = v.ports[0].__class__.__name__

            c.execute('SELECT * FROM interfaces WHERE var_name LIKE "{}" AND port_type LIKE "{}"'.format(k, value))
            x = c.fetchall()
            if_id = 0
            if len(x) == 0:
                c.execute('INSERT INTO interfaces VALUES (NULL, "{}", "{}")'.format(k, value))
                c.execute('SELECT LAST_INSERT_ROWID()')
                if_id = c.fetchall()[0][0]
            else:
                if_id = x[0][0]

            # Link the interfaces to the component if necessary
            c.execute('SELECT * FROM component_interface_link WHERE component_id LIKE {} AND interface_id LIKE {}'.format(comp_id, if_id))
            x = c.fetchall()
            if len(x) == 0:
                c.execute('INSERT INTO component_interface_link VALUES ({}, {})'.format(comp_id, if_id))

        except Exception as err:
            if verbose is True:
                logging.error(traceback.format_exc())


def write_parameters(comp, comp_id, c):
    """
    Writes all the parameters of a component to the database.
    Arguments.
        comp: Component object
        comp_id: Primary key id of the component object in the database (INTEGER)
        c: cursor object of python database connection object
    Return.
        Nothing
    """
    try:
        # delete existing component interface links and interfaces
        c.execute('SELECT * FROM component_parameter_link WHERE component_id LIKE {}'.format(comp_id))
        x = c.fetchall()
        if len(x) > 0:
            c.execute('DELETE FROM component_parameter_link WHERE component_id LIKE {}'.format(comp_id))
    except Exception as err:
        logging.error(traceback.format_exc())

    for k, v in comp.parameters.iteritems():
        c.execute('SELECT * FROM params WHERE var_name LIKE "{}" AND default_value LIKE "{}"'.format(str(k), str(v)))
        x = c.fetchall()
        param_id = 0
        if len(x) == 0:
            c.execute(
                'INSERT INTO params VALUES (NULL, "{}", "{}")'.format(str(k), str(v)))
            c.execute('SELECT LAST_INSERT_ROWID()')
            param_id = c.fetchall()[0][0]
        else:
            param_id = x[0][0]

        c.execute('SELECT * FROM component_parameter_link WHERE component_id LIKE {} AND parameter_id LIKE {}'.format(comp_id, param_id))
        x = c.fetchall()
        if len(x) == 0:
            c.execute('INSERT INTO component_parameter_link VALUES ({}, {})'.format(comp_id, param_id))


def write_composables(comp, comp_id, c):
    """
    Writes all the composables associated with a component to the database.
    Arguments.
        comp: Component object
        comp_id: Primary key id of the component object in the database (INTEGER)
        c: cursor object of python database connection object
    Return.
        Nothing
    """
    for k, v in comp.composables.iteritems():
        c.execute('SELECT * FROM composables WHERE var_name LIKE "{}" AND composable_obj LIKE "{}"'.format(str(k), str(v.__class__.__name__)))
        x = c.fetchall()
        compos_id = 0
        if len(x) == 0:
            c.execute('INSERT INTO composables VALUES (NULL, "{}", "{}")'.format(str(k), v.__class__.__name__))
            c.execute('SELECT LAST_INSERT_ROWID()')
            compos_id = c.fetchall()[0][0]
        else:
            compos_id = x[0][0]

        c.execute('SELECT * FROM component_composable_link WHERE component_id LIKE {} AND composable_id LIKE {}'.format(comp_id, compos_id))
        x = c.fetchall()
        if len(x) == 0:
            c.execute('INSERT INTO component_composable_link VALUES ({}, {})'.format(comp_id, compos_id))


class ComponentQueryItem:

    def __init__(self, name):
        """
        Initialize ComponentQueryItem
        Arguments.
            name: The name of the component. The value returned when
                  Component.getName() is called. (STRING)
        Return.
            ComponentQueryItem
        Attributes.
            name: The name of the component. The value returned when
                  Component.getName() is called. (STRING)
            interfaces: A dictionary containing the variable names of the
                        interfaces as its keys and the type of interface as its
                        values. All the data in the dict are strings
            parameters: A dictionary containing the variable names of the
                        parameters as its keys and the default values of the
                        parameters as its values. All the keys in the dict are
                        strings and all the values are string representations of
                        the default parameter values
            composables: A dictionary containing the types of the composables as
                         its keys and the names of the corresponding Composable
                         classes as its values. All the data in the dict are
                         strings
        """
        self.name = name

        # format: {interfaceName1 : interfaceType1, interfaceName2 :
        # interfaceType2}
        self.interfaces = {}

        # format: {parameterName1 : parameterValue1, parameterName2 :
        # parameterValue2}
        self.parameters = {}

        # format: {composableName1 : composableValue1, composableName2 :
        # composableValue2}
        self.composables = {}

    def gen_interface(self, rows):
        for i in rows:
            self.interfaces[i[3]] = i[4]

    def gen_parameters(self, rows):
        for i in rows:
            self.parameters[i[3]] = i[4]

    def get_name(self):
        return self.name

    def gen_composables(self, rows):
        for i in rows:
            self.composables[i[3]] = i[4]


def query_database(component, username="root", password="", verbose=False):
    """
    Look through the database and get a ComponentQueryItem that corresponds to
    component Object required
    Arguments.
        component: The name of the component. The value returned when
                   Component.getName() is called. (STRING)
        username: Username for the MySQL server. Default is "root" (STRING)
        password: Password for the MySQL server. Default is empty string "" (STRING)
        verbose: If True, the function outputs a more detailed error message when
                 a databse query fails. Default is False. (BOOLEAN)
    Return.
        ComponentQueryItem
    """
    # con = db.connect(user=username, passwd=password)

    db_path = os.path.join(os.getcwd(), 'compDatabase.db')
    con = db.connect(db_path)
    c = con.cursor()
    # c.execute('USE component_info')

    c.execute('SELECT * FROM components WHERE type LIKE "{}"'.format(component))
    exists = c.fetchall()


    # return with error message if the component doesn't exist in the database.
    if len(exists) == 0:
        if verbose:
            print "The component {} is not in the database.\n Call buildDatabase() with this component in the array to update the database. \nIf this message still persists, check if calling getComponent() on this string works.\n".format(component)
        
        con.commit()
        con.close()
        return None


    # gather interfaces
    item = ComponentQueryItem(component)
    x = c.execute('SELECT c.*, i.* FROM components c INNER JOIN component_interface_link ci ON ci.component_id = c.id INNER JOIN interfaces i ON i.id = ci.interface_id WHERE type LIKE "{}"'.format(component))
    y = c.fetchall()

    item.gen_interface(y)

    # gather parameters
    x = c.execute('SELECT c.*, p.* FROM components c INNER JOIN component_parameter_link cp ON cp.component_id = c.id INNER JOIN params p ON p.id = cp.parameter_id WHERE type LIKE "{}"'.format(component))
    y = c.fetchall()
    item.gen_parameters(y)
    # print y

    # gather composables
    x = c.execute('SELECT c.*, m.* FROM components c INNER JOIN component_composable_link cc ON cc.component_id = c.id INNER JOIN composables m ON m.id = cc.composable_id WHERE type LIKE "{}"'.format(component))
    y = c.fetchall()
    item.gen_composables(y)

    # c.close()
    # con.commit()

    con.commit()
    con.close()
    return item
