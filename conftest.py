def pytest_collection_modifyitems(config, items):
    """
    Custom pytest hook to modify the collection of test items.
    This function sorts test items to execute specific tests first.
    """

    def test_order(test_name):
        # Define the desired order of execution for specific test names
        order_mapping = {
            'test_write': 1,
            'test_write_multiple': 2,
            'test__load_config_no_file': 3,
            'test__load_config_skip_space_check': 4,
            'test__load_config_debug': 5,
            'test__load_config_invalid': 6,
            'test__select_output_button_callback': 7,
            'test__new_callback': 8,
            'test__exit_callback_download_thread_running': 9,
            'test__exit_callback_download_thread_not_running': 10,
            'test__help_callback': 11,
            'test_disable_controls': 12,
            'test_enable_controls': 13
        }
        return order_mapping.get(test_name, float('inf'))  # Default to infinity for tests not in the mapping

    items.sort(key=lambda item: (test_order(item.nodeid.split("::")[-1]), item.fspath, item.originalname))
