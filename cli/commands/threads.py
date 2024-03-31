from cli.command import CommandConfig, Command, Context
from utils.thread_wrapper import ThreadWrapper
import threading
from multiprocessing import active_children


class ThreadsCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        self.__get_all_threads()
        main_thread = self.all_threads[0]
        self.__recursively_print_tree([main_thread])
        self.__print_multiprocess_list()

    def __get_all_threads(self):
        threads = threading.enumerate()
        wrapper_threads = [threading.current_thread()]

        for thread in threads:
            if not isinstance(thread, ThreadWrapper):
                continue

            wrapper_threads.append(thread)

        self.all_threads = wrapper_threads

    def __recursively_print_tree(self, threads: list[ThreadWrapper], indent: int = 0):
        for thread in threads:
            print(f"{indent * ' '}{thread.name}")

            children = self.__get_children(thread)
            self.__recursively_print_tree(children, indent=indent+4)

    def __get_children(self, parent_thread: ThreadWrapper) -> list[ThreadWrapper]:
        children = []
        for thread in self.all_threads:
            if not isinstance(thread, ThreadWrapper):
                continue

            if thread.parent == parent_thread:
                children.append(thread)

        return children

    def __print_multiprocess_list(self):
        active_child_processes = active_children()
        if len(active_child_processes) < 1:
            return

        print()
        print("There are also some processes created by this process running:")
        for index, process in enumerate(active_child_processes, start=1):
            print(f"{index}. Name: {process.name} PID: {process.pid} Daemon: {process.daemon}")
