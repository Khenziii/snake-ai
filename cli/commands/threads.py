from cli.command import CommandConfig, Command, Context
from utils.thread_wrapper import ThreadWrapper
from threading import enumerate, current_thread


class ThreadsCommand(Command):
    def __init__(self, config: CommandConfig):
        super().__init__(config=config)

    def __call__(self, context: Context | None):
        if super().__call__(context=context):
            return

        self.__get_all_threads()
        main_thread = self.all_threads[0]
        self.__recursively_print_tree([main_thread])

    def __get_all_threads(self):
        threads = enumerate()
        wrapper_threads = [current_thread()]

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
