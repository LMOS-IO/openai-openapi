from pathlib import Path
from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator import DataModelType, PythonVersion
import json
import warnings

from ruamel.yaml import YAML
from ruamel.yaml.error import ReusedAnchorWarning

# fix errors from ruamel.yaml
warnings.simplefilter("ignore", ReusedAnchorWarning)

# convert the yaml into json
yaml = YAML(typ="safe", pure=True)

with open("openapi.yaml") as stream:
    data = yaml.load(stream)

openapi_json = json.dumps(data)

# create a path for the new package
release_pkg_dir = Path('openai_types/')
release_pkg_dir.mkdir(parents=True, exist_ok=True)

# create types
output = Path(release_pkg_dir / '__init__.py')
generate(
    input_=openapi_json,
    input_file_type=InputFileType.OpenAPI,
    output=output,
    output_model_type=DataModelType.PydanticV2BaseModel,
    target_python_version=PythonVersion.PY_310,
    field_constraints=True,
    reuse_model=True,
    treat_dots_as_module=True,
    use_subclass_enum=True,
    enum_field_as_literal="one",
    use_field_description=True
)