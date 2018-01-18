from made.controllers.inputs import input_manager_factory
import os

def test_create_folder_path():
    folder_path = input_manager_factory.create_folder_path(project_folder_name="my_project"
                                             ,source_id=45, source_label="customer", version ="05")

    assert folder_path == os.path.join("projects","my_project","inputs",str(45)+"_customer","05","raw","data")