import multiprocessing
import multiprocessing.pool


class NonDaemonicProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonicProcessPool(multiprocessing.pool.Pool):
    # Process = NonDaemonicProcess
    def Process(self, *args, **kwds):
        proc = super(NonDaemonicProcessPool, self).Process(*args, **kwds)

        class NonDaemonProcess(proc.__class__):
            """Monkey-patch process to ensure it is never daemonized"""
            @property
            def daemon(self):
                return False

            @daemon.setter
            def daemon(self, val):
                pass

        proc.__class__ = NonDaemonicProcess
        return proc
