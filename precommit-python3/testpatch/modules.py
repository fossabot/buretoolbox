#!/usr/bin/env python3

""" Define a module """

import logging
import os
import re
import utils
import timekeeper
import plugin

# pylint: disable=too-many-instance-attributes, too-few-public-methods
class Module():
    """  basic definition of a module """

    def __init__(self,path=None, parent=None):
        self.relpath = utils.relative_path(path)[1]

        self.parent = parent
        self.timer = None
        self.files = []
        self.status = None
        self.status_msg = None
        self.status_log = None
        self.compile_log = None
        self.index = 0

# ====

def file_fragment(dirfrag=None):
    """ take module and print the fragment """
    if not dirfrag:
        raise RuntimeError('ASSERT: No dirfrag given')

    if dirfrag in ('.', '@@@BASEDIR@@@'):
        return 'root'

    dirfrag = dirfrag.replace(str(os.sep), '_')
    dirfrag = dirfrag.replace(str(os.altsep), '_')
    return dirfrag

def argsubst(config, args=None, modname=None, filename=None):
    """ take module and print the fragment """
    if not args:
        return None

    newargs = []
    for arg in args:
        if arg:
            newarg = arg.replace('@@@MODULEFN@@@', filename).replace(
                '@@@MODULEDIR@@@',
                os.path.join(config.get('basedir'), modname))
            newargs.append(newarg)
    return newargs

def workerloop(coordinator,
               module=None,
               repostatus=None,
               testname=None,
               args=None):
    argv = args
    if not module:
        raise RuntimeError('No module defined for workerloop')
    fn = file_fragment(module.name)
    if module.software:
        ws = re.compile(r'\s+')
        for sw in list(module.software.keys()):
            sws = re.sub(ws, '', sw)
            fn = fn + sws + module.software.get(sws) \
                           .replace(os.sep,'_') \
                           .replace(os.altsep,'_')

    curdir = os.getcwd()
    moddir = module
    moddir = modname_conversion(config=coordinator.config, module=moddir)
    if not moddir:
        logging.error('WARNING: %s no longer exists; skipping' %
                    (module.name))
        return 0

    logf = '-'.join([repostatus, testname, fn + '.txt'])

    newargs = coordinator.pluginhandler['buildtools'].plugins[
        coordinator.config.get('buildtool')].executor()

    if argv:
        newargs2 = argsubst(config=coordinator.config, args=argv, filename=fn, modname=module.name)
        newargs = newargs + newargs2

    if module.extraparams:
        newargs3 = argsubst(config=coordinator.config,
                            args=module.extraparams,
                            filename=fn,
                            modname=module.name)
        newargs = newargs + newargs3

    os.chdir(moddir)
    timer = timekeeper()
    retval = utils.print_and_redirect(args=newargs,
                                      logfilename=os.path.join(
                                      coordinator.config.get('workdir'),
                                      logf))
    timer.stop()
    os.chdir(curdir)
    module.timer = timer.result()

    if testname == 'compile':
        module.compile_log = os.path.join(coordinator.config.get('workdir'),
                                          logf)

    if retval > 0:
        module.set_status('-1', logf)
        return retval

    module.set_status('+1', logf)
    return retval

def worker(coordinator, modules=None, repostatus=None, testname=None, args=None):
    #testname = kwargs.get('testname', None)
    #modules = kwargs.get('modules', None)
    #repostatus = kwargs.get('repostatus', 'patch')
    if coordinator.config.get('buildmode') == 'full':
        repo = 'the source'
    elif repostatus == 'branch':
        repo = coordinator.config.get('patch_branch')
    else:
        repo = 'the patch'

    result = 0
    for module in modules:

        suffix = file_fragment(module.name)

        result = result + workerloop(coordinator=coordinator,
                                    args=args,
                                          module=module,
                                          repostatus=repostatus,
                                          testname=testname)
        if result > 0:
            textresult = 'failed'
        else:
            textresult = 'passed'

        msg = '%s in %s %s' % (suffix, repo, textresult)

        if module.software:
            msg = msg + ' ['
            for sw in list(module.software.keys()):
                msg = msg + sw + '=' + module.software[sw]
            msg = msg + ']'

        module.message = msg

    return result

def modname_conversion(config, module=None, btcwd=None):
    if not btcwd:
        btcwd = config.get('buildtoolcwd', 'module')
    if btcwd in ('basedir', '.'):
        btcwd = '@@@BASEDIR@@@'
    elif btcwd == 'module':
        btcwd = '@@@MODULEDIR@@@'

    basedir = config.get('basedir')
    if module:
        btcwd = btcwd.replace('@@@MODULEDIR@@@', module.name)
    btcwd = btcwd.replace('@@@BASEDIR@@@', basedir)

    if not os.path.isabs(btcwd):
        btcwd = os.path.join(basedir, btcwd)

    return btcwd

def buildtool_cwd(coordinator, module=None, btcwd=None):
    dirabs = btcwd
    dirabs = modname_conversion(config=coordinator.config, module=module, btcwd=dirabs)

    if os.path.isabs(dirabs):
        if not os.path.exists(dirabs):
            try:
                os.makedirs(dirabs)
            except OSError as e:
                logging.error('ERROR: Unable to create %s: %s' % (dirabs, e))
                coordinator.fail_run()
                return False
        if os.chdir(dirabs):
            return True
    else:
        if os.chdir(dirabs):
            return True

    return False
